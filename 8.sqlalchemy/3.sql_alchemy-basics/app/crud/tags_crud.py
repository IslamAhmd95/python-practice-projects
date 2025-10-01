from app.database import sessionLocal
from app.models.tag import Tag

def create_tag(data):
    with sessionLocal() as session:
        tag = Tag(name=data['name'])
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag

def update_tag(tag_id, data):
    with sessionLocal() as session:
        tag = session.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            raise ValueError("Tag not found")
        tag.name = data['name']
        session.commit()
        session.refresh(tag)
        return tag
    
def delete_tag(tag_id):
    with sessionLocal() as session:
        tag = session.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            raise ValueError("Tag not found")
        session.delete(tag)
        session.commit()
        return "Tag deleted"
    
def get_all_tags():
    with sessionLocal() as session:
        tags = session.query(Tag).all()
        return tags

def get_specific_tag(tag_id):
    with sessionLocal() as session:
        tag = session.get(Tag, tag_id)
        if not tag:
            raise ValueError("Tag not found")
        return tag
    
def get_tag_posts(tag_id):
    with sessionLocal() as session:
        tag = session.get(Tag, tag_id)
        if not tag:
            raise ValueError("Tag not found")
        return tag.posts