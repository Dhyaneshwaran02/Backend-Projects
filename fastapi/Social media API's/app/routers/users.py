from fastapi import FastAPI,Response,HTTPException, status, Depends,APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db

router=APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User_res)
def create_post(users:schemas.UserCreate,db: Session = Depends(get_db)):

    hash_pass=utils.hash(users.password)
    users.password=hash_pass
   
    new_user=models.Users(**users.dict())#unpacking the dict using **
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.User_res)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user :
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    return user