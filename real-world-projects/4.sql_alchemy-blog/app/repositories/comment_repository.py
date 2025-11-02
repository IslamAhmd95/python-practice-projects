from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment_schema import UpdateCommentSchema
from app.schemas.user_schema import ReadUser



def get_comment_by_id(db: Session, comment_id: int) -> dict:
    comment = db.scalar(
        select(Comment)
        .options(
            selectinload(Comment.user),
            selectinload(Comment.post)
        )
        .where(Comment.id == comment_id)
    )

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    return comment

def update(db, comment_id: int, comment_data: UpdateCommentSchema, user_id: int):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this comment"
        )

    try:
        comment.content = comment_data.content
        db.commit()
        db.refresh(comment)
        return comment
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update comment: {str(e)}"
        )
    

def delete(db: Session, comment_id: int, user_id: int):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this comment"
        )

    try:
        db.delete(comment)
        db.commit()
        return comment
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete comment: {str(e)}"
        ) 
    

def like_comment(db: Session, comment_id: int, user: ReadUser):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if user in comment.liked_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already liked this comment"
        )

    try:
        comment.liked_by.append(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to like comment: {str(e)}"
        )
    

def unlike_comment(db: Session, comment_id: int, current_user: ReadUser):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    if current_user not in comment.liked_by:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have not liked this comment yet"
        )

    try:
        comment.liked_by.remove(current_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unlike comment: {str(e)}"
        )
    

def get_comment_likes(db, comment_id):
    comment = db.scalar(
        select(Comment)
        .options(selectinload(Comment.liked_by).load_only(User.id, User.name, User.username))
        .where(Comment.id == comment_id)
    )
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    return comment