"""
Purpose: entry point of the app.

    - Imports engine & SessionLocal from db/config.py.
    - Imports models (so SQLAlchemy knows about them).
    - Calls Base.metadata.create_all() to create tables.
    - Runs a simple CRUD test.
"""

from sqlalchemy import or_, and_
from db.config import engine, SessionLocal  # Brings in the engine (connection to the database) and SessionLocal (our session factory for talking to DB).
from db.base import Base  # Imports the Base class. This holds all models’ metadata (like table definitions).
from models.user import User


def init_db():
    
    Base.metadata.create_all(bind=engine)  # Tells SQLAlchemy: “Look at all models that inherit from Base (like User) and create their tables in the database if they don’t already exist.”

def main():
    init_db()
    
    # Opens a session (like opening a conversation with the database).
    # You use this session to add, read, update, and delete rows.
    session = SessionLocal()
    try:

        ## CREATE

        # user_john = User(username="john", email="john@example.com")
        # user_alice = User(username="alice", email="alice@example.com")
        # user_mark = User(username="mark", email="mark@example.com")

        # # add multiple users at once
        # session.add_all([user_john, user_alice, user_mark])  # Marks it to be added.
        # session.commit()  # Actually saves it in the database.

        # session.refresh(new_user)  # Updates the Python object with fresh data from the DB (like its auto-generated id).
        # print("Inserted:", new_user.id, new_user.username)


        ## READ all users with filtering and ordering

        
        users = session.query(User).all()  # get all users
        first_user = session.query(User).first()  # get the first user
        last_user = session.query(User).order_by(User.id.desc()).first()  # get the last user
        user_by_id = session.query(User).get(2)  # get user by primary key (id=2)
        user_by_username = session.query(User).filter_by(username='alice').first()  # get user by username

        result = session.query(User).filter(User.username == "alice").all()
        result = session.query(User).filter(User.id > 5).all()
        result = session.query(User).filter(and_(User.id > 5, User.username != "bob")).all()
        result = session.query(User).filter(or_(User.username == "alice", User.username == "bob")).all()

        session.query(User).filter(User.username.like("%a%")).all()
        session.query(User).filter(User.email.contains("@gmail.com")).all()
        session.query(User).filter(User.username.startswith("a")).all()
        session.query(User).filter(User.username.endswith("z")).all()

        session.query(User).order_by(User.username).all()
        session.query(User).order_by(User.id.desc()).all()

        session.query(User).limit(5).all()     # first 5 users
        session.query(User).offset(10).all()  # skip first 10 users



        # Get one user

        # user = session.query(User).filter_by(username="alice").first()
        # print("Read:", user)

        # UPDATE

        # user.email = "alice@new.com"  # Change the email in Python memory.
        # session.commit()  # Pushes the update into the database.
        # session.refresh(user)  # Refreshes the object from the DB (so it’s up-to-date).
        # print("Updated:", user.email)

        # DELETE

        # session.delete(user)  # Marks this row for deletion.
        # session.commit()  # Executes the deletion in the DB.
        # print("Deleted user.")
    finally:
        session.close()

if __name__ == "__main__":
    main()




