from datetime import datetime
from typing import List

from pydantic import BaseModel


class FileBase(BaseModel):
    name: str
    path: str
    size: int
    is_downloadable: bool = True


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class UploadFileMetadata(BaseModel):
    filename: str
    content_type: str
    size: int


class FileUploadResponse(BaseModel):
    filename: str
    content_type: str
    size: int
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    files: List[File] = []

    class Config:
        orm_mode = True
