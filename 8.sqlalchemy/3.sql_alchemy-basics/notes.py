from sqlalchemy import select
from app.database import sessionLocal
from app.models import Tag, User, Post
from faker import Faker

faker = Faker()


with sessionLocal() as session:
    tag = Tag(name=faker.unique.name())
    session.add(tag)
    session.commit()
    session.refresh(tag)
    print(tag.id)


with sessionLocal.begin() as session:
    tag = Tag(name=faker.unique.name())
    session.add(tag)
    
    for i in range(5):
        with session.begin_nested():
            if i == 3:
                tag = Tag(name=faker.unique.name())
                session.add(tag)
                raise

            tag = Tag(name=faker.unique.name())
            session.add(tag)



print(session.scalar(select(Tag.id).order_by(Tag.id.desc())))





"""
## SQLAlchemy 2.0 Querying

1. Building a query

    from sqlalchemy import select

    stmt = select(User)               # SELECT * FROM user
    stmt = select(User.name)          # SELECT name FROM user
    stmt = select(User).where(User.id == 1)  # SELECT * FROM user WHERE id=1

    - Always:
        👉 Build query with select(...)
        👉 Run with session.execute(stmt)

2. Extracting results

    A) .scalar()

    - Returns first column of the first row
    - If no rows → None
    - If multiple rows → only first row’s first column
    - Ex:

        stmt = select(User.name).where(User.id == 1)
        name = session.execute(stmt).scalar()
        =
        name = session.scalar(stmt)
        print(name)  # "Alice"

    B) .scalars()

        - Unwraps the ORM objects or column values from rows
        - Commonly used for ORM objects
        - You can chain .all(), .first(), .one(), .one_or_none()
        - Ex:

            # Get all User objects
            users = session.execute(select(User)).scalars().all()
            =
            users = session.scalars(select(User)).all()


            # First User object or None
            user = session.execute(select(User)).scalars().first()

    C) .first()

        - Returns the first row (tuple-like) or None.
        - Usually used without .scalars().
        - Ex:

            row = session.execute(select(User.name)).first()
            print(row)   # ('Alice',) or None

    D) .one()

        - Expects exactly one row.
        - ❌ Error if zero or multiple rows.
        - Ex:

            user = session.execute(select(User).where(User.id == 1)).scalars().one()

    E) .one_or_none()

        - Expects 0 or 1 row.
        - Returns row if found, else None.
        - ❌ Error if more than one row.
        - Ex:

            user = session.execute(select(User).where(User.id == 1)).scalars().one_or_none()

    F) .scalar_one()

        - Same as .one() but unwraps the first column directly.
        - Ex:

            name = session.execute(select(User.name).where(User.id == 1)).scalar_one()

    G) .scalar_one_or_none()

        - Same as .one_or_none() but unwraps the first column directly.
        - Ex:

            name = session.execute(select(User.name).where(User.id == 1)).scalar_one_or_none()

"""

"""

## SQLAlchemy Session Transactions

A Session in SQLAlchemy is the main interface to the database.
It manages:

    - Objects (adding, deleting, refreshing)
    - Transactions (commit, rollback)
    - Queries (select, execute)


1. Regular Session (explicit transaction management)

    - Each commit() → wraps your operations in a transaction.
    - If something fails, you must call session.rollback() manually.
    - More flexible, but you manage transactions explicitly.
    - Ex:

        with sessionLocal() as session:   # no transaction yet
            tag = Tag(name="physics")
            session.add(tag)
            session.commit()              # starts and commits a transaction
            session.refresh(tag)
            print(tag.id)

    

2. Transactional Session (session.begin())

    - Ex:

        with sessionLocal.begin() as session:
            tag = Tag(name="math")
            session.add(tag)
            # no need to call commit()
    
    - Starts a transaction immediately when entering the with block.

    - On exit:
        - If no exceptions → automatically commits.
        - If exception → automatically rolls back.

    - Ensures all-or-nothing safety.


3. Flushing & Refreshing

.flush()

    - Pushes SQL statements to DB without committing.
    - Reserves IDs (e.g., from autoincrement PK).
    - If transaction rolls back, the row is removed but the ID stays burned.
    - Ex:

        with sessionLocal.begin() as session:
            tag = Tag(name="biology")
            session.add(tag)
            session.flush()
            print(tag.id)  # already generated, but not yet committed
            raise ValueError("rollback") 
        # Result: No row saved, but next insert will use the next ID.

.refresh(obj)

    - Reloads object state from the database.
    - Requires the row to exist (so use after commit() or flush()).
    - Ex:

        session.add(tag)
        session.commit()
        session.refresh(tag)
        print(tag.id)


4. Savepoints: session.begin_nested()

    - Creates a sub-transaction (savepoint).
    - Useful for testing, partial rollback, retries.
    - Ex:

        with sessionLocal.begin() as session:
            for i in range(5):
                with session.begin_nested():
                    if i == 3:
                        session.add(Tag(name="bad"))
                        raise Exception("rollback inner")
                    session.add(Tag(name="good"))
        # Outer transaction commits everything at the end.
        # At i=3 → inner savepoint rolls back, but the loop continues.
        # Final result: all rows except i=3.


5. ID Gaps & Rollbacks

    - Autoincrement IDs are consumed at flush, not commit.
    - Rollback does not reset the counter → gaps appear.
    - Ex:

        # Insert + rollback
        with sessionLocal.begin() as session:
            tag = Tag(name="temp")
            session.add(tag)
            session.flush()  # ID assigned
            raise Exception("rollback")

        # Next insert
        with sessionLocal.begin() as session:
            tag = Tag(name="real")
            session.add(tag)
        # tag.id will be +1, gap created


"""