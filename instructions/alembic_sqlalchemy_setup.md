## SQLAlchemy + Alembic Project Setup Guide

This is my personal starter guide to quickly spin up a new project using SQLAlchemy + Alembic.
I’ll follow these steps whenever I create a new project.


### Step 1 — Setup Virtual Environment

    `python3 -m venv .venv`
    `source .venv/bin/activate`
    `pip install --upgrade pip`
    `pip freeze > requiremens.txt`

    or

    `python3 -m venv .venv`
    `uv init`
    `source .venv/bin/activate`

### Step 2 — Install Required Packages

    `pip install sqlalchemy alembic psycopg2-binary PyMySQL python-dotenv`
    `pip freeze > requiremens.txt`

    or

    `uv add sqlalchemy alembic psycopg2-binary PyMySQL python-dotenv`


    - psycopg2-binary → PostgreSQL driver
        `postgresql+psycopg2://user:password@localhost:5432/mydb`

    - PyMySQL → MySQL / MariaDB driver
        `mysql+pymysql://user:password@localhost:3306/mydb`

    - SQLite → already built into Python
        `sqlite:///mydb.sqlite3`

### Step 3 — Initialize Alembic

    `alembic init alembic`

    - `alembic/` will be the folder's name
    - `alembic.ini` (config file, like Laravel’s .env for migrations)

### Step 4 — Configure Database URL

    1. Create .env file in project root
        `DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/mydb`

    2. Create app/database.py:
        
    3. Edit `alembic/env.py`
        `
            from app.database import Base, DATABASE_URL
            from app import models  # ensures models are imported

            config.set_main_option("sqlalchemy.url", DATABASE_URL)
            target_metadata = Base.metadata
        `

        This ensures Alembic reads real database URL & scans all models before generating migrations.

    4. In alembic.ini, keep a dummy URL (will be overridden by env.py).
        `sqlalchemy.url = driver://user:pass@localhost/dbname`

### Step 5 — Add Your First Model

    1. Create `user.py` model inside `app/models/`
    2. import `User` class inside `app/models/__init__.py`
    3. Create migration file by running this command
        `alembic revision --autogenerate -m "create users table"`
        This creates a migration file in alembic/versions/
    4. Run migration
        `alembic upgrade head`


--------------------------------------------------------------------------------------


## Project Structure Explained

    - .venv/

        - Local virtual environment. Contains installed packages.
        - Never commit this. Instead, commit requirements.txt.

    - alembic/

        - All migration-related files.
        - env.py → tells Alembic how to find models & DB URL.
        - versions/ → every schema change is stored here (commit these files).
        - script.py.mako → migration template (don’t touch usually).

    - app/

        - Core application code.
        - crud/ → business logic (create/read/update/delete functions).
        - models/ → ORM models (User, Post, etc.).
        - database.py → central DB config (engine, SessionLocal).
        - __init__.py → imports all models so Alembic can detect them.

    - .env

        - Stores secrets (DB URL, credentials).
        - Never commit this file. Add it to .gitignore.

    - alembic.ini

        - Alembic config (basic settings, overridden by env.py).
        - Safe to commit.

    - main.py

        - Entry point — e.g. testing CRUD, or starting an API.

    - requirements.txt

        - Exact list of installed dependencies (pip freeze > requirements.txt).
        - Commit this.


--------------------------------------------------------------------------------------


## Alembic Common Commands (vs Laravel)

| Action                    | Laravel Command                           | Alembic Command                                     |
| ------------------------- | ----------------------------------------- | --------------------------------------------------- |
| Initialize migrations     | `php artisan migrate:install`             | `alembic init alembic`                              |
| Create migration          | `php artisan make:migration create_users` | `alembic revision --autogenerate -m "create users"` |
| Run migrations            | `php artisan migrate`                     | `alembic upgrade head`                              |
| Rollback last migration   | `php artisan migrate:rollback`            | `alembic downgrade -1`                              |
| Reset all migrations      | `php artisan migrate:reset`               | `alembic downgrade base`                            |
| Show migration history    | `php artisan migrate:status`              | `alembic history`                                   |
| Re-run specific migration | `php artisan migrate:refresh`             | `alembic downgrade -1 && alembic upgrade head`      |


--------------------------------------------------------------------------------------


## Notes

    1. 
        - by importing models inside app/models/__init__.py and then importing app.models in alembic/env.py, you ensure that Alembic loads all your models and sees them in Base.metadata.
        - Now when Alembic runs 
        `alembic revision --autogenerate` 
        , it sees User etc., because they’re imported via the models package, and attached to Base.metadata.

    2.
        - Put your real DB URL in .env.
        - Both your app code (database.py) and Alembic migrations (env.py) will read from .env.
        - Never hardcode DB credentials in code or alembic.ini.

    3. What if i wanted to add a new column 'age' to an existing table 'users' ?
        
        - Add the column to the User model
            `age = Column(Integer, nullable=True)`
        - Generate Migration
            `alembic revision --autogenerate -m "add age column to users"`

            - Alembic will compare Base.metadata (your models) with the actual DB schema.
            - It will generate a new file inside alembic/versions/ with the necessary ALTER TABLE statement.
        - Apply the Migration
            `alembic upgrade head`