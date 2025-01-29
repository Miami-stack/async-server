import redis
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db.crud import UserCRUD
from src.models.schemas import UserCreate
from src.services.db_service import get_db
from src.services.helpers import decode_token, \
    create_access_token

user_router = APIRouter()

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)


@user_router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    return await UserCRUD.create_user(db, user.username, user.password)


@user_router.post("/auth")
async def auth(token: str = Depends(OAuth2PasswordRequestForm),
               db: Session = Depends(get_db)):
    payload = decode_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserCRUD.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})

    r = redis.Redis(connection_pool=redis_pool)
    r.set(access_token, user.to_json(), ex=3600)

    return {"access_token": access_token, "token_type": "bearer"}
