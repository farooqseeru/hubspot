from datetime import datetime, timedelta
from typing import Optional
import boto3
import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.config import get_secret

# Load AWS Secrets
secrets = get_secret()
SECRET_KEY = secrets.get("SECRET_KEY", "your_default_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Load predefined users from AWS Secrets Manager
PREDEFINED_USERS = secrets.get("PREDEFINED_USERS", {})

router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    """Authenticate user with stored credentials"""
    user = PREDEFINED_USERS.get(username)
    if not user or not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in PREDEFINED_USERS:
            raise credentials_exception
        return PREDEFINED_USERS[username]
    except JWTError:
        raise credentials_exception


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return JWT token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    """A protected route requiring authentication"""
    return {"message": f"Hello, {current_user['username']}! You have access to this route."}
