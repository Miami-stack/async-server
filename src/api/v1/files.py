import os
import shutil
from datetime import datetime
from typing import Optional, List

import redis
from fastapi import APIRouter, Depends, HTTPException, status, \
    Response, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.db.crud import FileCRUD
from src.models.models_database import Users
from src.models.schemas import File, UploadFileMetadata, \
    FileUploadResponse, User
from src.services.db_service import get_db
from src.services.helpers import authenticate_user

file_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)


def get_current_user(db: Session, token: str):
    r = redis.Redis(connection_pool=redis_pool)
    user_data = r.get(token)
    if user_data:
        user = Users.from_json(user_data)
    else:
        user = authenticate_user(db, token)
        if user:
            r.set(token, user.to_json(), ex=3600)
    return user


@file_router.get("/files/", response_model=List[File])
async def list_files(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    current_user = get_current_user(db, token)
    return current_user.files


@file_router.post("/files/upload", response_model=FileUploadResponse)
async def upload_file(
        file: UploadFile,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    FILES_DIRECTORY = './media'
    metadata = UploadFileMetadata(
        filename=file.filename,
        content_type=file.content_type,
        size=len(await file.read())
    )
    file.file.seek(0)
    file_location = os.path.join(FILES_DIRECTORY, metadata.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_instance = File(
        name=metadata.filename,
        path=file_location,
        size=metadata.size,
        is_downloadable=True,
        created_at=datetime.utcnow(),
        user_id=current_user.id
    )

    db.add(file_instance)
    db.commit()
    db.refresh(file_instance)

    return FileUploadResponse(
        filename=file_instance.name,
        size=file_instance.size,
        id=file_instance.id,
        created_at=file_instance.created_at,
        user_id=file_instance.user_id
    )


@file_router.get("/files/download")
async def download_file(path: Optional[str] = None,
                        file_id: Optional[int] = None,
                        db: Session = Depends(get_db)):
    if path:
        file = FileCRUD.get_file_by_path(db, path)
    elif file_id:
        file = FileCRUD.get_file_by_id(db, file_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either path or file_id must be provided"
        )

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return Response(content=file.content, media_type=file.media_type)
