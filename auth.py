from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
token_expires = os.getenv("TOKEN_EXPIRES")
algorithm = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")