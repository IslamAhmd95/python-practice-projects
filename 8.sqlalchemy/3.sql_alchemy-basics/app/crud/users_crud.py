from sqlalchemy.orm import joinedload
from app.database import sessionLocal
from app.models.user import User
from app.models.profile import Profile

def create_user(data):
    with sessionLocal() as session:
        user = User(name=data['name'], username=data['username'], email=data['email'])
        Profile(bio=data['bio'], user=user)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update_user(user_id, data):
    with sessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        user.name = data['name']
        user.profile.bio = data['bio']
        session.commit()
        session.refresh(user)
        return user

def delete_user(user_id):
    with sessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        session.delete(user)
        session.commit()
        return "User deleted."

def get_all_users():
    with sessionLocal() as session:
        return session.query(User).all()
    
def get_specific_user(user_id):
    with sessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user

def follow_user(user_id, user_to_follow_id):
    with sessionLocal() as session:
        # user = session.get(User, user_id)
        user = (
            session.query(User)
            .options(joinedload(User.following))
            .filter(User.id == user_id)
            .first()
        )
        user_to_follow = session.get(User, user_to_follow_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        if not user_to_follow:
            raise ValueError(f"User with ID {user_to_follow} not found.")
        user.following.append(user_to_follow)
        session.commit()
        session.refresh(user)
        return user
    
def unfollow_user(user_id, user_to_unfollow_id):
    with sessionLocal() as session:
        # user = session.get(User, user_id)
        user = (
            session.query(User)
            .options(joinedload(User.following))
            .filter(User.id == user_id)
            .first()
        )
        user_to_unfollow = session.get(User, user_to_unfollow_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        if not user_to_unfollow:
            raise ValueError(f"User with ID {user_to_unfollow} not found.")
        user.following.remove(user_to_unfollow)
        session.commit()
        session.refresh(user)
        return user

def get_user_posts(user_id):
    with sessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user.posts