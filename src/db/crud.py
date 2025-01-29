import bcrypt
from sqlalchemy.orm import Session
from src.models.models_database import Users, File


class UserCRUD:
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(Users).filter(Users.username == username).first()

    @staticmethod
    def create_user(db: Session, username: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db_user = Users(username=username, hashed_password=hashed_password.decode('utf-8'))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def verify_password(user: Users, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))


class FileCRUD:
    @staticmethod
    def get_file_by_path(db: Session, path: str):
        return db.query(File).filter(File.path == path).first()

    @staticmethod
    def get_file_by_id(db: Session, file_id: int):
        return db.query(File).filter(File.id == file_id).first()

    @staticmethod
    def create_file(db: Session, path: str, content: bytes, media_type: str, owner_id: int):
        db_file = File(path=path, content=content, media_type=media_type, owner_id=owner_id)
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file

    @staticmethod
    def delete_file(db: Session, file_id: int):
        file = db.query(File).filter(File.id == file_id).first()
        if file:
            db.delete(file)
            db.commit()
        return file