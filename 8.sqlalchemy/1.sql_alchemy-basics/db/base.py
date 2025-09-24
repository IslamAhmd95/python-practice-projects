"""
Purpose: keep a single Base class (declarative base) that all models inherit from.
Why separate? → It avoids circular imports (models depend on Base, Base depends on nothing).
"""


from sqlalchemy.orm import declarative_base

# Base class that all ORM models will inherit from
Base = declarative_base()



"""
Explanation:

    - declarative_base() creates a special base class called Base.

    - Every ORM model (table class) we write will inherit from this Base.

    - SQLAlchemy uses Base to keep track of all models and their tables.

    - Later, when we call Base.metadata.create_all(), it creates all tables in the DB from the models.
"""




