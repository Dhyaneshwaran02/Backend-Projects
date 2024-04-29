from fastapi import FastAPI, HTTPException, Depends, status,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, utils, oauth2
from ..database import get_db

router=APIRouter(tags=['Authentication'])

@router.get('/login')
async def login(users_credentials:OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == users_credentials.username).first()
    if not user :
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    if not utils.verify(users_credentials.password,user.password) :
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    
    access_token=oauth2.create_access_token(data={'user_id':user.id})
    return {'access_token':access_token,'token_type':'bearer'}