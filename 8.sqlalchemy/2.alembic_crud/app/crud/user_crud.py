from app.database import sessionLocal
from app.models.user import User

def get_users():
    with sessionLocal() as session:
        users = session.query(User).all()
        return users

def get_user_by_id(user_id: int):
    with sessionLocal() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    
def create_user(data: dict):

    # I should validate data before saving them

    with sessionLocal() as session:
        user = User(name=data['name'], email=data['email'], password=data['password'])
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update_user(user_id: int, data: dict):

    # I should validate data before saving them

    with sessionLocal() as session:
        user = session.query(User).get(user_id)
        if not user:
            print("User not exists")
            exit()

        user.name = data['name']
        user.email = data['email']
        user.password = data['password']

        session.commit()
        session.refresh(user)
        return user
    
def delete_user(user_id: int):
    with sessionLocal() as session:
        user = session.query(User).get(user_id)
        if not user:
            print("User not exists")
            exit()
            
        session.delete(user)
        session.commit()
        return "User deleted"