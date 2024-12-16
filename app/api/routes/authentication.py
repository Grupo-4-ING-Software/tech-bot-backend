from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.services.database_connection_service import sessionLocal, engine
from app.schemas.user import User
from passlib.context import CryptContext
from pydantic import BaseModel
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from app.core.settings import get_settings
import requests
import json

router = APIRouter()
settings = get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    email: str
    password: str

class GoogleRequest(BaseModel):
    token: str


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return "User created correctly" 

def create_google_user(db: Session, email: str):
    db_user = User(email=email, hashed_password=None) 
    db.add(db_user)
    db.commit()
    return db_user

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Crear token con información del usuario
    token_data = {
        "sub": user.email,
        "user_id": user.id,
        "email": user.email
    }
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }

@router.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message":"Token is valid"}

@router.post("/login/google")
async def login_with_google(request: GoogleRequest, db: Session = Depends(get_db)):
    token = request.token
    try:
        id_info = id_token.verify_oauth2_token(token, Request(), settings.GOOGLE_CLIENT_ID)

        email = id_info.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Google token"
            )
        
        # Buscar o crear usuario
        db_user = get_user_by_email(db, email=email)
        if not db_user:
            db_user = create_google_user(db, email=email)
        
        # Crear token con información del usuario
        token_data = {
            "sub": db_user.email,
            "user_id": db_user.id,
            "email": db_user.email
        }
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": db_user.id,
                "email": db_user.email
            }
        }

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid Google OAuth token"
        )

@router.post("/register/google")
async def register_with_google(request: GoogleRequest, db: Session = Depends(get_db)):
    token = request.token
    try:
        id_info = id_token.verify_oauth2_token(token, Request(), get_settings().GOOGLE_CLIENT_ID)

        email = id_info.get("email")
        if email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google token")

        db_user = get_user_by_email(db, email=email)
        if db_user:
            print("User already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cuenta registrada con este correo electrónico"
            )
        
        db_user = create_google_user(db, email=email)

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google OAuth token")

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({
        "exp": expire,
        "user_id": data.get("user_id")
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")
