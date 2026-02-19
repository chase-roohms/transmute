import os
import uuid
import hashlib

from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Depends
from fastapi.responses import FileResponse
from pathlib import Path
from core import get_settings, detect_media_type
from db import FileDB, ConversionDB, ConversionRelationsDB
from registry import ConverterRegistry
from ..deps import get_file_db, get_conversion_db, get_conversion_relations_db

router = APIRouter(prefix="/files", tags=["files"])

# Define upload directory
settings = get_settings()
converter_registry = ConverterRegistry()
UPLOAD_DIR = settings.upload_dir
CONVERTED_DIR = settings.output_dir

async def save_file(file: UploadFile, db: FileDB) -> dict:
    uuid_str = str(uuid.uuid4())
    original_filename = file.filename or "upload"
    file_extension = Path(original_filename).suffix.lower()
    unique_filename = f"{uuid_str}{file_extension}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = Path(UPLOAD_DIR) / unique_filename
    hasher = hashlib.sha256()
    size_bytes = 0
    # Stream upload to disk and compute hash in one pass
    with file_path.open("wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)  # Read in 1MB chunks
            if not chunk:
                break
            buffer.write(chunk)
            hasher.update(chunk)
            size_bytes += len(chunk)
    
    media_type = detect_media_type(file_path)

    metadata = {
        "id": uuid_str,
        "storage_path": str(file_path),
        "original_filename": original_filename,
        "media_type": media_type,
        "extension": file_extension,
        "size_bytes": size_bytes,
        "sha256_checksum": hasher.hexdigest(),
    }
    db.insert_file_metadata(metadata)
    metadata["compatible_formats"] = converter_registry.get_compatible_formats(media_type)
    return metadata

@router.get("/")
def list_files(file_db: FileDB = Depends(get_file_db)):
    """List all uploaded files"""
    files = file_db.list_files()
    return {"files": files}


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    file_db: FileDB = Depends(get_file_db)
):
    """Upload a file and save it to the server"""
    try:
        metadata = await save_file(file, file_db)
        return {"message": "File uploaded successfully", "metadata": metadata}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        await file.close()

@router.get("/{file_id}")
def get_file(file_id: str):
    """Download a converted file"""
    # Find file with matching ID
    for file_path in CONVERTED_DIR.iterdir():
        if file_path.stem == file_id:
            return FileResponse(
                path=file_path,
                filename=file_path.name,
                media_type="application/octet-stream"
            )
    raise HTTPException(status_code=404, detail="File not found")


@router.delete("/{file_id}")
def delete_file(
    file_id: str,
    file_db: FileDB = Depends(get_file_db),
    converted_file_db: ConversionDB = Depends(get_conversion_db),
    conversion_rel_db: ConversionRelationsDB = Depends(get_conversion_relations_db)
):
    """Delete an uploaded file"""
    # Find file with matching ID
    converted_file_id = conversion_rel_db.get_conversion_from_file(file_id)
    file_metadata = file_db.get_file_metadata(file_id)
    if file_metadata is None:
        raise HTTPException(status_code=404, detail="File not found")
    os.unlink(file_metadata['storage_path'])
    if converted_file_id:
        converted_file_metadata = converted_file_db.get_file_metadata(converted_file_id)
        os.unlink(converted_file_metadata['storage_path'])
        converted_file_db.delete_file_metadata(converted_file_id)
        conversion_rel_db.delete_relation_by_original(file_id)
    file_db.delete_file_metadata(file_id)
    return {"message": "File deleted successfully"}
