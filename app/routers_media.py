from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os, shutil
from app.models import Media, User
from app.deps import get_db, get_current_user
from app.config import settings
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api", tags=["media"])

@router.post("/medias", response_model=dict)
def upload_media(file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    os.makedirs(settings.API_MEDIA_DIR, exist_ok=True)
    tmp_path = os.path.join(settings.API_MEDIA_DIR, f"tmp_{file.filename}")
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    media = Media(filename=file.filename, content_type=file.content_type or "application/octet-stream", path="pending", author_id=user.id)
    db.add(media)
    db.flush()
    final_path = os.path.join(settings.API_MEDIA_DIR, f"{media.id}_{file.filename}")
    os.rename(tmp_path, final_path)
    media.path = final_path
    db.commit()
    return {"result": True, "media_id": media.id}

@router.get("/media/{media_id}")
def get_media(media_id: int, db: Session = Depends(get_db)):
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(404, "Not found")
    return FileResponse(media.path, media_type=media.content_type, filename=media.filename)
