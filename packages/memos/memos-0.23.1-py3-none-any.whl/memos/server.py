import os
import httpx
import uvicorn
import mimetypes
from fastapi import FastAPI, HTTPException, Depends, status, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from typing import List, Annotated
from pathlib import Path
import asyncio
import json
import cv2
from PIL import Image
import logging

from .config import get_database_path, settings
from memos.plugins.vlm import main as vlm_main
from memos.plugins.ocr import main as ocr_main
from . import crud
from .schemas import (
    Library,
    Folder,
    Entity,
    Plugin,
    NewLibraryParam,
    NewFoldersParam,
    NewEntityParam,
    UpdateEntityParam,
    NewPluginParam,
    NewLibraryPluginParam,
    UpdateEntityTagsParam,
    UpdateEntityMetadataParam,
    MetadataType,
    MetadataIndexItem,
    EntitySearchResult,
    SearchResult,
    SearchHit,
    RequestParams,
    EntityContext,
    BatchIndexRequest,
)
from .read_metadata import read_metadata
from .logging_config import LOGGING_CONFIG
from .models import load_extension

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure mimetypes for JavaScript files
# This is a workaround for the issue:
# https://github.com/python/cpython/issues/88141#issuecomment-1631735902
# Without this, the mime type of .js files will be text/plain and
# the browser will not render them correctly in some windows machines.
mimetypes.add_type("application/javascript", ".js")

app = FastAPI()

engine = create_engine(
    f"sqlite:///{get_database_path()}",
    pool_size=10,
    max_overflow=20,
    pool_timeout=60,
    pool_recycle=3600,
    connect_args={"timeout": 60},
)
event.listen(engine, "connect", load_extension)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


current_dir = os.path.dirname(__file__)

app.mount(
    "/_app", StaticFiles(directory=os.path.join(current_dir, "static/_app"), html=True)
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/favicon.png", response_class=FileResponse)
async def favicon_png():
    return FileResponse(os.path.join(current_dir, "static/favicon.png"))


@app.get("/favicon.ico", response_class=FileResponse)
async def favicon_ico():
    return FileResponse(os.path.join(current_dir, "static/favicon.png"))


@app.get("/")
async def serve_spa():
    return FileResponse(os.path.join(current_dir, "static/app.html"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/libraries", response_model=Library, tags=["library"])
def new_library(library_param: NewLibraryParam, db: Session = Depends(get_db)):
    # Check if a library with the same name (case insensitive) already exists
    existing_library = crud.get_library_by_name(library_param.name, db)
    if existing_library:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Library with this name already exists",
        )

    # Remove duplicate folders from the library_param
    unique_folders = []
    seen_paths = set()
    for folder in library_param.folders:
        if folder.path not in seen_paths:
            seen_paths.add(folder.path)
            unique_folders.append(folder)
    library_param.folders = unique_folders

    library = crud.create_library(library_param, db)
    return library


@app.get("/libraries", response_model=List[Library], tags=["library"])
def list_libraries(db: Session = Depends(get_db)):
    libraries = crud.get_libraries(db)
    return libraries


@app.get("/libraries/{library_id}", response_model=Library, tags=["library"])
def get_library_by_id(library_id: int, db: Session = Depends(get_db)):
    library = crud.get_library_by_id(library_id, db)
    if library is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )
    return library


@app.post("/libraries/{library_id}/folders", response_model=Library, tags=["library"])
def new_folders(
    library_id: int,
    folders: NewFoldersParam,
    db: Session = Depends(get_db),
):
    library = crud.get_library_by_id(library_id, db)
    if library is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    existing_folders = [folder.path for folder in library.folders]
    if any(str(folder.path) in existing_folders for folder in folders.folders):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Folder already exists in the library",
        )

    return crud.add_folders(library_id=library.id, folders=folders, db=db)


async def trigger_webhooks(
    library: Library, entity: Entity, request: Request, plugins: List[int] = None
):
    async with httpx.AsyncClient() as client:
        tasks = []
        for plugin in library.plugins:
            if plugins is None or plugin.id in plugins:
                if plugin.webhook_url:
                    location = str(
                        request.url_for("get_entity_by_id", entity_id=entity.id)
                    )
                    webhook_url = plugin.webhook_url
                    if webhook_url.startswith("/"):
                        webhook_url = str(request.base_url)[:-1] + webhook_url
                        logging.debug("webhook_url: %s", webhook_url)
                    task = client.post(
                        webhook_url,
                        json=entity.model_dump(mode="json"),
                        headers={"Location": location},
                        timeout=60.0,
                    )
                    tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for plugin, response in zip(library.plugins, responses):
            if plugins is None or plugin.id in plugins:
                if isinstance(response, Exception):
                    logging.error(
                        "Error triggering webhook for plugin %d: %s",
                        plugin.id,
                        response,
                    )
                elif response.status_code >= 400:
                    logging.error(
                        "Error triggering webhook for plugin %d: %d - %s",
                        plugin.id,
                        response.status_code,
                        response.text,
                    )


@app.post("/libraries/{library_id}/entities", response_model=Entity, tags=["entity"])
async def new_entity(
    new_entity: NewEntityParam,
    library_id: int,
    request: Request,
    db: Session = Depends(get_db),
    plugins: Annotated[List[int] | None, Query()] = None,
    trigger_webhooks_flag: bool = True,
    update_index: bool = False,
):
    library = crud.get_library_by_id(library_id, db)
    if library is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    entity = crud.create_entity(library_id, new_entity, db)
    if trigger_webhooks_flag:
        await trigger_webhooks(library, entity, request, plugins)

    if update_index:
        crud.update_entity_index(entity, db)

    return entity


@app.get(
    "/libraries/{library_id}/folders/{folder_id}/entities",
    response_model=List[Entity],
    tags=["entity"],
)
def list_entities_in_folder(
    library_id: int,
    folder_id: int,
    limit: Annotated[int, Query(ge=1, le=400)] = 10,
    offset: int = 0,
    path_prefix: str | None = None,
    db: Session = Depends(get_db),
):
    library = crud.get_library_by_id(library_id, db)
    if library is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    if folder_id not in [folder.id for folder in library.folders]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Folder not found in the specified library",
        )

    entities, total_count = crud.get_entities_of_folder(
        library_id, folder_id, db, limit, offset, path_prefix
    )
    return JSONResponse(
        content=jsonable_encoder(entities), headers={"X-Total-Count": str(total_count)}
    )


@app.get(
    "/libraries/{library_id}/entities/by-filepath",
    response_model=Entity,
    tags=["entity"],
)
def get_entity_by_filepath(
    library_id: int, filepath: str, db: Session = Depends(get_db)
):
    entity = crud.get_entity_by_filepath(filepath, db)
    if entity is None or entity.library_id != library_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found"
        )
    return entity


@app.post(
    "/libraries/{library_id}/entities/by-filepaths",
    response_model=List[Entity],
    tags=["entity"],
)
def get_entities_by_filepaths(
    library_id: int, filepaths: List[str], db: Session = Depends(get_db)
):
    entities = crud.get_entities_by_filepaths(filepaths, db)
    return [entity for entity in entities if entity.library_id == library_id]


@app.get("/entities/{entity_id}", response_model=Entity, tags=["entity"])
def get_entity_by_id(entity_id: int, db: Session = Depends(get_db)):
    entity = crud.get_entity_by_id(entity_id, db)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found"
        )
    return entity


@app.get(
    "/libraries/{library_id}/entities/{entity_id}",
    response_model=Entity,
    tags=["entity"],
)
def get_entity_by_id_in_library(
    library_id: int, entity_id: int, db: Session = Depends(get_db)
):
    entity = crud.get_entity_by_id(entity_id, db)
    if entity is None or entity.library_id != library_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entity not found"
        )
    return entity


@app.put("/entities/{entity_id}", response_model=Entity, tags=["entity"])
async def update_entity(
    entity_id: int,
    request: Request,
    updated_entity: UpdateEntityParam = None,
    db: Session = Depends(get_db),
    trigger_webhooks_flag: bool = False,
    plugins: Annotated[List[int] | None, Query()] = None,
    update_index: bool = False,
):
    entity = crud.find_entity_by_id(entity_id, db)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    if updated_entity:
        entity = crud.update_entity(entity_id, updated_entity, db)

    if trigger_webhooks_flag:
        library = crud.get_library_by_id(entity.library_id, db)
        if library is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
            )
        await trigger_webhooks(library, entity, request, plugins)

    if update_index:
        crud.update_entity_index(entity, db)

    return entity


@app.post(
    "/entities/{entity_id}/last-scan-at",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["entity"],
)
def update_entity_last_scan_at(entity_id: int, db: Session = Depends(get_db)):
    """
    Update the last_scan_at timestamp for an entity and trigger update for fts and vec.
    """
    succeeded = crud.touch_entity(entity_id, db)
    if not succeeded:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )


@app.post(
    "/entities/{entity_id}/index",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["entity"],
)
def update_index(entity_id: int, db: Session = Depends(get_db)):
    """
    Update the FTS and vector indexes for an entity.
    """
    entity = crud.get_entity_by_id(entity_id, db)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    crud.update_entity_index(entity, db)


@app.post(
    "/entities/batch-index",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["entity"],
)
async def batch_update_index(request: BatchIndexRequest, db: Session = Depends(get_db)):
    """
    Batch update the FTS and vector indexes for multiple entities.
    """
    try:
        crud.batch_update_entity_indices(request.entity_ids, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.put("/entities/{entity_id}/tags", response_model=Entity, tags=["entity"])
def replace_entity_tags(
    entity_id: int, update_tags: UpdateEntityTagsParam, db: Session = Depends(get_db)
):
    entity = crud.get_entity_by_id(entity_id, db)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    return crud.update_entity_tags(entity_id, update_tags.tags, db)


@app.patch("/entities/{entity_id}/tags", response_model=Entity, tags=["entity"])
def patch_entity_tags(
    entity_id: int, update_tags: UpdateEntityTagsParam, db: Session = Depends(get_db)
):
    entity = crud.get_entity_by_id(entity_id, db)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    return crud.add_new_tags(entity_id, update_tags.tags, db)


@app.patch("/entities/{entity_id}/metadata", response_model=Entity, tags=["entity"])
def patch_entity_metadata(
    entity_id: int,
    update_metadata: UpdateEntityMetadataParam,
    db: Session = Depends(get_db),
):
    entity = crud.get_entity_by_id(entity_id, db)
    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found",
        )

    # Use the CRUD function to update the metadata entries
    entity = crud.update_entity_metadata_entries(
        entity_id, update_metadata.metadata_entries, db
    )
    return entity


@app.delete(
    "/libraries/{library_id}/entities/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["entity"],
)
def remove_entity(library_id: int, entity_id: int, db: Session = Depends(get_db)):
    entity = crud.get_entity_by_id(entity_id, db)
    if entity is None or entity.library_id != library_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found in the specified library",
        )

    crud.remove_entity(entity_id, db)


@app.post("/plugins", response_model=Plugin, tags=["plugin"])
def new_plugin(new_plugin: NewPluginParam, db: Session = Depends(get_db)):
    existing_plugin = crud.get_plugin_by_name(new_plugin.name, db)
    if existing_plugin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plugin with this name already exists",
        )
    plugin = crud.create_plugin(new_plugin, db)
    return plugin


@app.get("/plugins", response_model=List[Plugin], tags=["plugin"])
def list_plugins(db: Session = Depends(get_db)):
    plugins = crud.get_plugins(db)
    return plugins


@app.post(
    "/libraries/{library_id}/plugins",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["plugin"],
)
def add_library_plugin(
    library_id: int, new_plugin: NewLibraryPluginParam, db: Session = Depends(get_db)
):
    library = crud.get_library_by_id(library_id, db)
    if library is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    plugin = None
    if new_plugin.plugin_id is not None:
        plugin = crud.get_plugin_by_id(new_plugin.plugin_id, db)
    elif new_plugin.plugin_name is not None:
        plugin = crud.get_plugin_by_name(new_plugin.plugin_name, db)

    if plugin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plugin not found"
        )

    if any(p.id == plugin.id for p in library.plugins):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plugin already exists in the library",
        )

    crud.add_plugin_to_library(library_id, plugin.id, db)


@app.delete(
    "/libraries/{library_id}/plugins/{plugin_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["plugin"],
)
def delete_library_plugin(
    library_id: int, plugin_id: int, db: Session = Depends(get_db)
):
    library = crud.get_library_by_id(library_id, db)
    if library is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Library not found"
        )

    plugin = crud.get_plugin_by_id(plugin_id, db)
    if plugin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plugin not found"
        )

    crud.remove_plugin_from_library(library_id, plugin_id, db)


def is_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]


def get_thumbnail_info(metadata: dict) -> tuple:
    if not metadata:
        return None, None, None

    if not metadata.get("sequence"):
        return None, None, False

    return metadata.get("screen_name"), metadata.get("sequence"), True


def extract_video_frame(video_path: Path, frame_number: int) -> Image.Image:
    cap = cv2.VideoCapture(str(video_path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame_rgb)


@app.get("/files/video/{file_path:path}", tags=["files"])
async def get_video_frame(file_path: str):

    full_path = Path("/") / file_path.strip("/")

    if not full_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    if not is_image(full_path):
        return FileResponse(full_path)

    metadata = read_metadata(str(full_path))
    screen, sequence, is_thumbnail = get_thumbnail_info(metadata)

    logging.debug(
        "Screen: %s, Sequence: %s, Is Thumbnail: %s", screen, sequence, is_thumbnail
    )

    if not all([screen, sequence, is_thumbnail]):
        return FileResponse(full_path)

    video_path = full_path.parent / f"{screen}.mp4"
    logging.debug("Video path: %s", video_path)
    if not video_path.is_file():
        return FileResponse(full_path)

    frame_image = extract_video_frame(video_path, sequence)
    if frame_image is None:
        return FileResponse(full_path)

    temp_dir = Path("/tmp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"temp_{full_path.name}"
    frame_image.save(temp_path)

    return FileResponse(
        temp_path, headers={"Content-Disposition": f"inline; filename={full_path.name}"}
    )


@app.get("/files/{file_path:path}", tags=["files"])
async def get_file(file_path: str):
    full_path = Path("/") / file_path.strip("/")
    # Check if the file exists and is a file
    if full_path.is_file():
        return FileResponse(full_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/search", response_model=SearchResult, tags=["search"])
async def search_entities_v2(
    q: str,
    library_ids: str = Query(None, description="Comma-separated list of library IDs"),
    limit: Annotated[int, Query(ge=1, le=200)] = 48,
    start: int = None,
    end: int = None,
    db: Session = Depends(get_db),
):
    library_ids = [int(id) for id in library_ids.split(",")] if library_ids else None

    try:
        if q.strip() == "":
            # Use list_entities when q is empty
            entities = crud.list_entities(
                db=db, limit=limit, library_ids=library_ids, start=start, end=end
            )
        else:
            # Use hybrid_search when q is not empty
            entities = crud.hybrid_search(
                query=q,
                db=db,
                limit=limit,
                library_ids=library_ids,
                start=start,
                end=end,
            )

        # Convert Entity list to SearchHit list
        hits = []
        for entity in entities:
            entity_search_result = EntitySearchResult(
                id=str(entity.id),
                filepath=entity.filepath,
                filename=entity.filename,
                size=entity.size,
                file_created_at=int(entity.file_created_at.timestamp()),
                file_last_modified_at=int(entity.file_last_modified_at.timestamp()),
                file_type=entity.file_type,
                file_type_group=entity.file_type_group,
                last_scan_at=(
                    int(entity.last_scan_at.timestamp())
                    if entity.last_scan_at
                    else None
                ),
                library_id=entity.library_id,
                folder_id=entity.folder_id,
                tags=[tag.name for tag in entity.tags],
                metadata_entries=[
                    MetadataIndexItem(
                        key=metadata.key,
                        value=(
                            json.loads(metadata.value)
                            if metadata.data_type == MetadataType.JSON_DATA
                            else metadata.value
                        ),
                        source=metadata.source,
                    )
                    for metadata in entity.metadata_entries
                ],
            )

            hits.append(
                SearchHit(
                    document=entity_search_result,
                    highlight={},
                    highlights=[],
                    text_match=None,
                    hybrid_search_info=None,
                    text_match_info=None,
                )
            )

        # Build SearchResult
        search_result = SearchResult(
            facet_counts=[],
            found=len(hits),
            hits=hits,
            out_of=len(hits),
            page=1,
            request_params=RequestParams(
                collection_name="entities", first_q=q, per_page=limit, q=q
            ),
            search_cutoff=False,
            search_time_ms=0,
        )

        return search_result

    except Exception as e:
        logging.error("Error searching entities: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get(
    "/libraries/{library_id}/entities/{entity_id}/context",
    response_model=EntityContext,
    tags=["entity"],
)
def get_entity_context(
    library_id: int,
    entity_id: int,
    prev: Annotated[int | None, Query(ge=0, le=100)] = None,
    next: Annotated[int | None, Query(ge=0, le=100)] = None,
    db: Session = Depends(get_db),
):
    """
    Get the context (previous and next entities) for a given entity.

    Args:
        library_id: The ID of the library
        entity_id: The ID of the target entity
        prev: Number of previous entities to fetch (optional)
        next: Number of next entities to fetch (optional)

    Returns:
        EntityContext object containing prev and next lists of entities
    """
    # If both prev and next are None, return empty lists
    if prev is None and next is None:
        return EntityContext(prev=[], next=[])

    # Convert None to 0 for the crud function
    prev_count = prev if prev is not None else 0
    next_count = next if next is not None else 0

    # Get the context entities
    prev_entities, next_entities = crud.get_entity_context(
        db=db,
        library_id=library_id,
        entity_id=entity_id,
        prev=prev_count,
        next=next_count,
    )

    # Return the context object
    return EntityContext(prev=prev_entities, next=next_entities)


def run_server():
    logging.info("Database path: %s", get_database_path())
    logging.info("VLM plugin enabled: %s", settings.vlm)
    logging.info("OCR plugin enabled: %s", settings.ocr)

    # Add VLM plugin router
    # Removed check for settings.vlm.enabled
    vlm_main.init_plugin(settings.vlm)
    app.include_router(vlm_main.router, prefix="/plugins/vlm")

    # Add OCR plugin router
    # Removed check for settings.ocr.enabled
    ocr_main.init_plugin(settings.ocr)
    app.include_router(ocr_main.router, prefix="/plugins/ocr")

    uvicorn.run(
        "memos.server:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=False,
        log_config=LOGGING_CONFIG,
    )
