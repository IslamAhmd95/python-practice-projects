from fastapi import HTTPException, status # pyright: ignore[reportMissingImports]
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from app.models.tag import Tag
from app.schemas.tag_schema import CreateTagSchema, TagFilterSchema
from app.core.enums import OrderEnum


def get_all(db: Session, filters: TagFilterSchema) -> list[Tag]:
    total = db.scalar(select(func.count()).select_from(Tag))
    tags = db.scalars(
            select(Tag)
            .options(selectinload(Tag.posts))
            .order_by(Tag.created_at.asc() if filters.order == OrderEnum.ASC else Tag.created_at.desc())
            .offset(filters.offset).limit(filters.limit)
        ).all()
    
    return tags, total


def create(db: Session, data: CreateTagSchema) -> dict:
    if db.execute(select(Tag).where(Tag.name == data.name)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag with this name already exists")
    
    new_tag = Tag(name=data.name)
    try:
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        return new_tag
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create tag: {str(e)}")


def get_by_id(db: Session, tag_id: int) -> Tag | None:
    tag = db.scalar(select(Tag).options(selectinload(Tag.posts)).where(Tag.id == tag_id))
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    
    return tag


def update(db: Session, tag_id: int, data: CreateTagSchema) -> dict:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    
    exists = db.execute(
        select(Tag).where(Tag.name == data.name, Tag.id != tag_id)
    ).first()

    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag name already exists")

    try:
        tag.name = data.name
        db.commit()
        db.refresh(tag)
        return tag
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to update tag: {str(e)}")


def delete(db: Session, tag_id: int) -> dict:
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    
    db.delete(tag)
    db.commit()
    return tag