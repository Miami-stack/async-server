from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'hashed_password': self.hashed_password,
            'is_active': self.is_active
        }

    @classmethod
    def from_json(cls, json_data: dict):
        # Create a User object from a JSON string
        return cls(**json_data)



class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    path = Column(String)
    size = Column(Integer)
    is_downloadable = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="files")


Users.files = relationship("File", order_by=File.id, back_populates="user")
