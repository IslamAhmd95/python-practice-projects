from app.database import sessionLocal
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment


def toggle_like_post(data):
    with sessionLocal() as session:
        user = session.get(User, data['user_id'])
        if not user:
            raise ValueError('User not found')
        
        post = session.get(Post, data['post_id'])
        if not post:
            raise ValueError('Post not found')
        
        liked = False
        if post not in user.liked_posts:
            user.liked_posts.append(post)
            liked = True
        else:
            user.liked_posts.remove(post)

        session.commit()
        session.refresh(user)
        session.refresh(post)

        return {"user": user, "post": post, "liked": liked}


def toggle_like_comment(data):
    with sessionLocal() as session:
        user = session.get(User, data['user_id'])
        if not user:
            raise ValueError('User not found')
        
        comment = session.get(Comment, data['comment_id'])
        if not comment:
            raise ValueError('Comment not found')
        
        liked = False
        if comment not in user.liked_comments:
            user.liked_comments.append(comment)
            liked = True
        else:
            user.liked_comments.remove(comment)

        session.commit()
        session.refresh(user)
        session.refresh(comment)
            
        return {"user": user, "comment": comment, "liked": liked}
