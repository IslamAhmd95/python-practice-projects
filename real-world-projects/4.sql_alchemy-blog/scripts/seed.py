# Run : python -m scripts.seed
# -m makes Python run seed.py as part of a package, not just a standalone file → which is why imports work.

from faker import Faker
import random
from sqlalchemy import select
from app.core.database import sessionLocal, BaseModel, engine
from app.models.user import User, RoleEnum
from app.models.post import Post
from app.models.profile import Profile
from app.models.tag import Tag
from app.models.comment import Comment
from app.core.hashing import hash_password

import app.core.events      # It executes the entire file once (top to bottom) and activates all event listeners for your entire application.


faker = Faker()

def seed_users(session):
    
    admins = [
        User(name="Islam Ahmed", username="IslamAhmd", email="Islam@gmail.com", password=hash_password("adminpass"), role=RoleEnum.ADMIN.value),
        User(name="Admin User", username="adminuser", email="Admin@gmail.com", password=hash_password("adminpass"), role=RoleEnum.ADMIN.value)
    ]

    for admin in admins:
        profile = Profile(bio=faker.paragraph(nb_sentences=3), user=admin)
        session.add(profile)


    users = [
        User(name=faker.name(), username=faker.unique.user_name(), email=faker.email(), password=hash_password("password123"))
        for _ in range(50)
    ]

    for user in users:
        profile = Profile(bio=faker.paragraph(nb_sentences=3), user=user)
        session.add(profile)


    session.add_all(admins)
    session.add_all(users)
    session.flush()  # ensures the database assigns primary keys (IDs) to all the newly created objects without committing the transaction.

    for user in users:
        possible_users_to_follow = [u for u in users if u.id != user.id]
        num_to_follow = random.randint(1, min(len(possible_users_to_follow), 4))
        random_follows = random.sample(possible_users_to_follow, num_to_follow)
        user.following.extend(random_follows)

    session.commit()

def seed_tags(session):
    tags = [
        Tag(name=faker.unique.word())
        for _ in range(20)
    ]
    session.add_all(tags)
    session.commit()

def seed_posts(session):
    user_ids = session.scalars(select(User.id)).all()

    posts = [
        Post(title=faker.sentence(nb_words=3),
             content=faker.paragraph(nb_sentences=3),
             author_id=random.choice(user_ids))  # assumes 50 users exist
        for _ in range(100)
    ]

    tags = session.query(Tag).all()

    for post in posts:
        num_tags = random.randint(1, 3)
        post.tags.extend(random.sample(tags, num_tags))

    session.add_all(posts)
    session.commit()

def seed_comments(session):

    user_ids = session.scalars(select(User.id)).all()
    post_ids = session.scalars(select(Post.id)).all()

    comments = [
        Comment(content=faker.sentence(),
                author_id=random.choice(user_ids),
                post_id=random.choice(post_ids)) 
        for _ in range(200)
    ]
    session.add_all(comments)
    session.commit()

def seed_likes(session):
    users = session.query(User).all()
    posts = session.query(Post).all()
    comments = session.query(Comment).all()

    for user in users:
        posts_num = random.randint(1, len(posts))
        liked_posts = random.sample(posts, posts_num)
        user.liked_posts.extend(liked_posts)

        comments_num = random.randint(1, len(comments))
        liked_comments = random.sample(comments, comments_num)
        user.liked_comments.extend(liked_comments)

    session.commit()

def fresh():
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)


def run():
    fresh()
    with sessionLocal() as session:
        seed_users(session)
        seed_tags(session)
        seed_posts(session)
        seed_comments(session)
        seed_likes(session)

if __name__ == "__main__":
    run()
