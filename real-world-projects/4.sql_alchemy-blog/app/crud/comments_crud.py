from sqlalchemy import select
from app.database import sessionLocal
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User


def create_comment(data):
    with sessionLocal() as session:
        user = session.get(User, data['user_id'])
        post = session.get(Post, data['post_id'])
        if not user:
            raise ValueError("User not found")
        if not post:
            raise ValueError("Post not found")
        comment = Comment(content=data['content'], user=user, post=post)
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return comment

def update_comment(comment_id, data):
    with sessionLocal() as session:
        comment = session.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError("Comment not found")
        if "content" in data:
            comment.content = data["content"]
        session.commit()
        session.refresh(comment)
        return comment
    
def delete_comment(comment_id):
    with sessionLocal() as session:
        comment = session.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError("Comment not found")
        session.delete(comment)
        session.commit()
        return "Comment deleted"
    
def get_all_comments():
    with sessionLocal() as session:
        comments = session.scalars(select(Comment)).all()
        return comments

def get_specific_comment(comment_id):
    with sessionLocal() as session:
        comment = session.get(Comment, comment_id)
        if not comment:
            raise ValueError("Comment not found")
        return comment
