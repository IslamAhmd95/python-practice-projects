"""
Purpose: how to connect to the database (engine + session factory).
You can later change the DB (SQLite, MySQL, Postgres) here without touching models.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import pymysql



# Example: SQLite (file-based)
# SQLITE_URL = "sqlite:///./db.sqlite"

# If you want MySQL, change this instead:
# MYSQL_URL = f"mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
MYSQL_URL = f"mysql+pymysql://root:51215@localhost:3306/sqlalchemy_basics"


# If you want PostgreSQL, use:
# PG_URL = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"


# Pick one URL (right now we use SQLite)
DATABASE_URL = MYSQL_URL

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=True
)

# Create Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)






"""
Explanation:

    - create_engine: function from SQLAlchemy that creates a connection to a database. Think of it as “the plug” that connects your Python app to the database.

    - sessionmaker: a factory (tool) that creates Session objects. A Session is like a “workspace” where you can add, read, update, or delete things in the DB.

    - quote_plus: function that helps encode special characters in passwords or usernames so the database URL doesn’t break

    - SQLITE_URL = "sqlite:///./db.sqlite"
        - Example: SQLite (file-based)
        - This line sets up a connection string for SQLite, which is a simple file-based database. The database file will be named db.sqlite and will be located in the current directory (./).

    - If you want MySQL, change this instead:
        MYSQL_URL = f"mysql+pymysql://{user}:{quote_plus(password)}@{host}:{port}/{database}"
        - This is how to set up a connection string for MySQL. You would replace user, password, host, port, and database with your actual MySQL credentials and details. The quote_plus function is used to ensure that any special characters in the password are properly encoded.

    - If you want PostgreSQL, use:
        # PG_URL = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        - Similar to the MySQL example, this is a commented-out connection string for PostgreSQL. You would replace pg_user, pg_password, pg_host, pg_port, and pg_db with your PostgreSQL credentials and details.


    - engine = the actual connection engine. This is the object that SQLAlchemy uses to talk to your database.

    - connect_args={"check_same_thread": False} is special for SQLite:

        - By default, SQLite does not allow the same database connection to be used by different threads.

        - In web apps (like FastAPI), threads are used, so we need this setting to avoid errors.

        - For MySQL/Postgres, it’s not needed, so we pass an empty {}.

    - echo=True → tells SQLAlchemy to print out the SQL commands it sends to the database (good for learning/debugging).

    - SessionLocal is a session factory — a tool that makes new Session objects whenever we call it.

        - autocommit=False → changes are not saved to DB until you call .commit().

        - autoflush=False → SQLAlchemy won’t automatically send changes to the DB until you explicitly say so.

        - bind=engine → tells the session which engine (which database connection) to use.
"""