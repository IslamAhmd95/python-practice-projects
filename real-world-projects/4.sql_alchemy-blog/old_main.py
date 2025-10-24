from app.crud.users_crud import (
    create_user, update_user, get_all_users,
    get_specific_user, follow_user, unfollow_user, delete_user, get_user_posts
)
from app.crud.tags_crud import (
    create_tag, update_tag, get_all_tags,
    get_specific_tag, delete_tag, get_tag_posts
)
from app.crud.posts_crud import (
    create_post, update_post, delete_post,
    get_all_posts, get_specific_post, get_post_comments
)
from app.crud.comments_crud import (
    create_comment, update_comment, delete_comment,
    get_all_comments, get_specific_comment
)
from app.crud.likes_crud import toggle_like_post, toggle_like_comment
from app.hashing import hash_password

import app.events      # It executes the entire file once (top to bottom) and activates all event listeners for your entire application.


## User Crud Operations

# Create a user
u1 = create_user({
    "name": "Alice",
    "username": "alice123",
    "email": "alice@example.com",
    "password": hash_password("password123"),
    "bio": "I love blogging!"
})
print("Created:", u1.id, u1.name)

u2 = create_user({
    "name": "Bob",
    "username": "bob88",
    "email": "bob@example.com",
    "password": hash_password("password123"),
    "bio": "Hello world!"
})
print("Created:", u2.id, u2.name)

# Update user
updated = update_user(u1.id, {"name": "Alice Updated", "bio": "New bio here"})
print("Updated:", updated.id, updated.name, updated.profile.bio)

# Get all users
users = get_all_users()
print("All users:", [u.username for u in users])

# Get specific user
specific = get_specific_user(u2.id)
print("Specific user:", specific.id, specific.name)

# Delete user
print(delete_user(1))  # Deletes user with ID 1, their profile, and followers links

# Follow & Unfollow
followed = follow_user(u1.id, u2.id)
print(f"{followed.name} is now following {[u.username for u in followed.following]}")

unfollowed = unfollow_user(u1.id, u2.id)
print(f"{unfollowed.name} is now following {[u.username for u in unfollowed.following]}")

# Get user posts
user_posts = get_user_posts(2)
print("All user posts:", [p.title for p in user_posts])


## Tag Crud Operations

# Create a new tag
new_tag = create_tag({"name": "Python"})
print("Created:", new_tag.id, new_tag.name)

# Get all tags
all_tags = get_all_tags()
print("All tags:", [tag.name for tag in all_tags])

# Get a specific tag
specific = get_specific_tag(new_tag.id)
print("Specific tag:", specific.id, specific.name)

# Update the tag
updated = update_tag(new_tag.id, {"name": "SQLAlchemy"})
print("Updated:", updated.id, updated.name)

# Delete the tag
print(delete_tag(new_tag.id))

# Get tag posts
tag_posts = get_tag_posts(2)
print("All tag posts:", [p.title for p in tag_posts])


## Post Crud Operations
 
# Create a new post
new_post = create_post({
    "user_id": 2,
    "title": "My First Post",
    "content": "This is some blog content."
})
print("Created:", new_post.id, new_post.title)

# Update a post
updated_post = update_post(new_post.id, {
    "title": "Updated Title",
    "content": "Updated content here."
})
print("Updated:", updated_post.id, updated_post.title)

# Get all posts
all_posts = get_all_posts()
print("All posts:", [p.title for p in all_posts])

# Get specific post
post = get_specific_post(new_post.id)
print("Specific post:", post.title, post.content)

# Get post comments
comments = get_post_comments(20)
print("Comments:", [c.content for c in comments])

# Delete post
print(delete_post(new_post.id))


## Comment Crud Operations

# Create a comment
new_comment = create_comment({
    "content": "This is my first comment!",
    "user_id": 2,
    "post_id": 1
})
print("Created:", new_comment.content)

# Update a comment
updated = update_comment(new_comment.id, {"content": "Edited comment text"})
print("Updated:", updated.content)

# Get specific comment
c = get_specific_comment(new_comment.id)
print("Fetched:", c.content)

# Get all comments
all_comments = get_all_comments()
print("All comments:", [cm.content for cm in all_comments])

# Delete comment
msg = delete_comment(new_comment.id)
print(msg)


## Like Crud Operations

# Toggle like on a Post
result_post = toggle_like_post({"user_id": 4, "post_id": 4})
if result_post["liked"]:
    print(f"{result_post['user'].name} liked the post '{result_post['post'].title}'")
else:
    print(f"{result_post['user'].name} unliked the post '{result_post['post'].title}'")

# Toggle like on a Comment
result_comment = toggle_like_comment({"user_id": 4, "comment_id": 25})
if result_comment["liked"]:
    print(f"{result_comment['user'].name} liked the comment: '{result_comment['comment'].content}'")
else:
    print(f"{result_comment['user'].name} unliked the comment: '{result_comment['comment'].content}'")



"""    
- Recommendation for your stage now
    - Keep it simple now → just CRUD for users, posts, comments, tags, profiles.
    - Plan to add auth when you add FastAPI (and maybe password hashing with bcrypt, JWT with python-jose or fastapi.security).
    That way:
        - You first show data modeling + DB handling.
        - Then you show API building + validation + auth as a second step.
"""