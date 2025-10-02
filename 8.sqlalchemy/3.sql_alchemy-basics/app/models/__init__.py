from .user import User
from .post import Post
from .profile import Profile
from .tag import Tag
from .comment import Comment
from .post_tags import PostTag
from .user_followers import user_followers
from .post_likes import post_likes
from .comment_likes import comment_likes

# This allows Alembic's autogenerate to discover models
__all__ = ["User", "Post", "Profile", "Tag", "Comment", "PostTag", "user_followers", "post_likes", "comment_likes"]
