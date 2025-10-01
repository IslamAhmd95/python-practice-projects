from app.database import sessionLocal
from app.models.post import Post
from app.models.user import User


def create_post(data):
    with sessionLocal() as session:
        user = session.get(User, data['user_id'])
        if not user:
            raise ValueError("User not found")
        post = Post(title=data['title'], content=data['content'], user=user)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

def update_post(post_id, data):
    with sessionLocal() as session:
        post = session.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise ValueError("Post not found")
        if "title" in data:
            post.title = data["title"]
        if "content" in data:
            post.content = data["content"]
        session.commit()
        session.refresh(post)
        return post
    
def delete_post(post_id):
    with sessionLocal() as session:
        post = session.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise ValueError("Post not found")
        session.delete(post)
        session.commit()
        return "Post deleted"
    
def get_all_posts():
    with sessionLocal() as session:
        posts = session.query(Post).all()
        return posts

def get_specific_post(post_id):
    with sessionLocal() as session:
        post = session.get(Post, post_id)
        if not post:
            raise ValueError("Post not found")
        return post

def get_post_comments(post_id):
    with sessionLocal() as session:
        post = (
            session.query(Post)
            .filter(Post.id == post_id).first()
        )
        if not post:
            raise ValueError("Post not found")
        return post.comments
        # return post.comments works without joinedload → because lazy load is triggered while session is open.

        # return post then later post.comments → needs joinedload if session is closed.