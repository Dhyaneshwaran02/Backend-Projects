from fastapi import FastAPI, HTTPException, Depends, status,APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models,oauth2
from ..database import get_db

router=APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/",response_model=List[schemas.Post_res])
async def get_posts(db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user),limit:int=2,
                    skip:int=0, search: Optional[str]=" "):
    #cur.execute("""SELECT * FROM posts""")
    #posts=cur.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == get_current_user.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    print(limit)
    return posts

@router.get("/{id}",response_model=schemas.Post_res)
async def get_post_by_id(id: int, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
    # post = cur.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post :
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post_res)
def create_post(post: schemas.Post,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("""INSERT INTO posts (title,content) VALUES(%s,%s) RETURNING *""",
    #             (post.title,post.content))
    # new_posts=cur.fetchone()
    # conn.commit()
    new_posts=models.Post(owner_id=get_current_user.id,**post.dict())#unpacking the dict using **
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("DELETE FROM posts WHERE id=%s RETURNING *", (str(id),))
    # del_post=cur.fetchone()
    # conn.commit()
    del_query = db.query(models.Post).filter(models.Post.id == id)
    del_post=del_query.first()
    if del_post == None:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    
    if del_post.owner_id != get_current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    del_query.delete(synchronize_session=False)
    db.commit()

    # Return a message indicating successful deletion
    return {"message": f"Post {id} deleted successfully"}

@router.put("/{id}",response_model=schemas.Post_res)
def update_post(id: int, update_post: schemas.Post, db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", 
    #             (updated_post.title, updated_post.content, str(id)))
    # updated_post=cur.fetchone()
    # conn.commit()  # Commit the changes to the database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=404, detail=f"Post {id} not found")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")
    post_query.update(update_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()