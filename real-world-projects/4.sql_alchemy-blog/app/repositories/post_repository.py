from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload, load_only

from app.models.post import Post
from app.models.tag import Tag
from app.models.user import User
from app.models.comment import Comment
from app.models.post_likes import post_likes
from app.schemas.post_schema import PostFilterSchema, CommentFilterSchema, CreateCommentSchema
from app.core.enums import OrderEnum


def get_all(db: Session, filters: PostFilterSchema):
    total = db.scalar(
        select(func.count()).select_from(Post)
    )

    posts = db.scalars(
        select(Post)
        .options(
            selectinload(Post.tags).load_only(Tag.id, Tag.name),
            selectinload(Post.user).load_only(User.id, User.name, User.username)
        )
        .order_by(Post.created_at.asc() if filters.order == OrderEnum.ASC else Post.created_at.desc())
        .offset(filters.offset)
        .limit(filters.limit)
    ).all()

    return posts, total


def get_by_id(db: Session, post_id: int):
    post = db.scalar(
        select(Post)
        .options(selectinload(Post.tags).load_only(Tag.id, Tag.name),
            selectinload(Post.user).load_only(User.id, User.name, User.username)
        )
        .where(Post.id == post_id)
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post


def create_post(db: Session, data, current_user):
    new_post = Post(
        title=data.title,
        content=data.content,
        author_id=current_user.id
    )

    if data.tag_ids:
        tags = db.scalars(select(Tag).where(Tag.id.in_(data.tag_ids))).all()
        new_post.tags = tags

    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create post: {str(e)}")



def update(db: Session, post_id: int, data, current_user):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    if data.title:
        post.title = data.title
    if data.content:
        post.content = data.content
    if data.tag_ids is not None:
        tags = db.scalars(select(Tag).where(Tag.id.in_(data.tag_ids))).all()
        post.tags = tags

    try:
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update post: {str(e)}")



def delete(db: Session, post_id: int, current_user):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    try:
        db.delete(post)
        db.commit()
        return post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to delete post: {str(e)}")


def like_post(db: Session, post_id: int, user_id: int):
    post = db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    user = db.execute(select(User).where(User.id == user_id)).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    stmt = db.query(post_likes).filter_by(post_id=post_id, user_id=user_id)
    if db.query(stmt.exists()).scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already liked this post.")
    try:
        db.execute(post_likes.insert().values(post_id=post_id, user_id=user_id))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to like post: {str(e)}")


def unlike_post(db: Session, post_id: int, user_id: int):
    stmt = db.query(post_likes).filter_by(post_id=post_id, user_id=user_id)
    if not db.query(stmt.exists()).scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already did not like this post")

    try:
        db.execute(post_likes.delete().where(
            (post_likes.c.post_id == post_id) & (post_likes.c.user_id == user_id)
        ))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to unlike post: {str(e)}")


def get_post_likes(db: Session, post_id: int):
    post = db.scalar(
        select(Post)
        .options(selectinload(Post.liked_by).load_only(User.id, User.username, User.name))
        .where(Post.id == post_id)
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


def get_comments(db: Session, post_id: int, filters: CommentFilterSchema):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
        
    total = db.scalar(
        select(func.count()).select_from(Comment)
        .where(Comment.post_id == post_id)
    )

    comments = db.scalars(
        select(Comment)
        .where(Comment.post_id == post_id)
        .options(
            selectinload(Comment.user).load_only(User.id, User.name, User.username)
        )
        .order_by(
            Comment.id.asc() if filters.order == OrderEnum.ASC else Comment.id.desc()
        )
        .offset(filters.offset)
        .limit(filters.limit)
    ).all()

    return comments, total


def create_comment(db: Session, comment_data: CreateCommentSchema, post_id: int, user_id: int):
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    try: 
        new_comment = Comment(
            content=comment_data.content,
            author_id=user_id,
            post_id=post_id
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create comment: {str(e)}"
        )
