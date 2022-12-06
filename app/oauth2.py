from jose import JWTError, jwt
from datetime import datetime, timedelta 
from . import models, schemas, utils, oauth2, database
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

#Secret key
#Algorithm
#Expiration time

SECRET_KEY = " qwertyuiopasdfghjklzxcvbnm1234567890!@#"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_tokens(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encode_jwt


    # verify access tokens
def verify_access_token(token : str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers ={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

