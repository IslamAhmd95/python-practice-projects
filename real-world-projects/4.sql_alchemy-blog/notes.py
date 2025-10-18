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


"""
## Lazy Loading

    Lazy loading means:
        - The related objects are not loaded when you query the parent.
        - They are loaded only when you first access the relationship attribute in Python code.
        - Defined at model level using the lazy parameter inside the relationship() function.
        - Think:
            - You load User.
            - The .posts are “sleeping” until you actually ask for them.
            - When you ask → SQLAlchemy fires another SQL query.

        - Pros
            - Saves time and memory when you don’t always need related data.
            - Keeps initial queries lightweight.

        - Cons
            - Can cause N+1 problem (many small queries).
            - Each attribute access may hit the database again.

    Lazy Loading Techniques / Options
        Lazy loading itself has different modes (SQLAlchemy calls them “lazy options”).

        1. lazy="select" (default)

            - Each time you access the attribute, it fires a separate SELECT.
            - Example: user.posts → query runs.
            - Pros: Simple, default, works everywhere.
            - Cons: Can cause N+1 problem if looping many parents.
            - Query:

                posts = relationship("Post", lazy="select", back_populates="author", lazy="joined")
                user = session.get(User, 1)
                print(user.posts)   # fires SELECT * FROM posts WHERE user_id=1

        2. lazy="joined"

            - Actually not “true lazy” → it’s eager using JOIN.
            - Loads relationship in the same query with parent.
            - But you still access it lazily in Python.
            - Some people include this in “lazy options” because you pass it in relationship(lazy="joined"), but it’s technically eager loading.
            - Ex:
                posts = relationship("Post", back_populates="author", lazy="joined")
                # one sql query run under the hood
                    SELECT users.id, users.name, posts.id, posts.title
                    FROM users LEFT OUTER JOIN posts ON users.id=posts.user_id;
                # Pros: One query, no N+1.
                # Cons: Data duplication if child table is big.

        3. lazy="selectin"

            - Also eager-like: runs two queries.
            - Parents first, then one IN (...) query for all children.

        4. lazy="noload"

            - Never automatically load the relationship.
            - If you access it, you just get an empty collection (for one-to-many) or None (for many-to-one).
            - Use this when you never want implicit queries and prefer explicit joins.
            - Ex:

                posts = relationship("Post", back_populates="author", lazy="noload")
                user = session.get(User, 1)
                print(user.posts)   # []
                # Pros: No hidden queries, total control.
                # Cons: You must always fetch explicitly.

        5. lazy="raiseload"

            - If you access the relationship without explicitly eager loading, it raises an error.
            - Forces you to plan queries properly.
            - Ex:

                posts = relationship("Post", back_populates="author", lazy="raiseload")
                user = session.get(User, 1)
                print(user.posts)   # raises sqlalchemy.exc.InvalidRequestError
                # Pros: Protects from unintentional N+1 problems.
                # Cons: More strict; might be annoying in quick scripts.

        6. lazy="subquery"

            - Another eager-like option (fetch children using subquery).
            - Rarely used now, replaced by selectin.

        7. lazy="dynamic"

            - The lazy='dynamic' option for relationship() is a legacy technique that provides a performance optimization for very large collections. Instead of loading the entire collection of related objects into memory, it returns a Query object (or a Query-like object in SQLAlchemy 2.0) that can be filtered and executed further.

            - When to use lazy='dynamic'
                - Legacy systems: It is still found in a lot of older SQLAlchemy code, especially from the 1.x series.
                - Avoided in modern code: The dynamic loader has limitations, particularly with asynchronous operations and certain iteration patterns where it can still implicitly load the entire collection. For truly large collections, lazy='write_only' is the recommended modern alternative.

            - Ex:

                posts: Mapped[List['Post']] = relationship(lazy='dynamic', back_populates='author')

                # When you access user.posts, you get a query object
                # This doesn't load all posts yet
                query_for_posts = user.posts  # returns this query "select * from posts where posts.user_id = user_id;

                # You can filter and get a subset without loading all posts
                recent_posts = query_for_posts.filter(Post.content.like('%recent%')).all()

                
        8. lazy='write_only'

            - This option is a modern and more robust alternative to lazy='dynamic', introduced in SQLAlchemy 2.0 for managing extremely large collections. It completely prevents the relationship from implicitly loading or iterating related objects. It is designed for write-heavy operations on a collection you never want to load into memory. 

            - How it works
                - When you access the relationship, it returns a WriteOnlyCollection object instead of a list or query.
                - This collection only has methods for adding and removing items (add(), add_all(), remove()).
                - To read or query the collection, you must explicitly use methods like .select() on the WriteOnlyCollection to build a SELECT statement.

            - When to use lazy='write_only'
                - Very large collections: When you have collections so large they are not feasible to load into memory.
                - Write-heavy operations: For scenarios where you only need to add or remove items without needing to read or display the entire collection.
                - Preventing accidental loads: If you want to absolutely ensure that the relationship is never implicitly loaded.
                - Asynchronous code: It is fully compatible with SQLAlchemy's asyncio capabilities, unlike the dynamic loader.

            - Ex:

                posts: WriteOnlyMapped['Post'] = relationship(lazy='write_only', back_populates='author')

                # Usage with a session
                with Session(engine) as session:
                    user = User(id=1)
                    session.add(user)
                    session.commit()
                    
                    # Add a post to the collection
                    user.posts.add(Post(content="New Post"))
                    session.commit()
                    
                    # You cannot iterate user.posts directly. This will fail:
                    # for post in user.posts: ...
                    
                    # To query, use the .select() method
                    stmt = user.posts.select().where(Post.content.like('%New%'))
                    recent_posts = session.scalars(stmt).all()





## Eager Loading

    - Eager loading = load related objects at the same time as the parent query (or in a controlled batch), instead of waiting until attribute access.

    - So:
        - Defined at query level using .options() with loaders like joinedload, selectinload, or subqueryload.
        - You query User, and at the same time, you already load User.posts.
        - No extra queries when you later access user.posts.
        - It’s the opposite of lazy loading.

    - Pros
        - Avoids N+1 queries.
        - Accessing related attributes doesn’t trigger extra database calls.
        - Efficient if you know you’ll always need the relationship data.

    - Cons
        - Loads more data than necessary if you don’t use the relationship.
        - joinedload can cause large joins and duplicate parent rows.
        - selectinload still runs two queries (though batched).    

    - Techniques of Eager Loading in SQLAlchemy

        - There are two main techniques:
            - Joined Eager Loading (joinedload)
            - Select In Eager Loading (selectinload)
            - (There’s also subqueryload, but it’s mostly replaced by selectinload in modern SQLAlchemy.)

            1. Joined Eager Loading (joinedload)

                - Uses JOIN in the same SQL query to fetch both parent + child.
                - Ex:

                    from sqlalchemy.orm import joinedload
                    users = session.query(User).options(joinedload(User.posts)).all()
                    =
                    SELECT users.id, users.name, posts.id, posts.title
                    FROM users
                    LEFT OUTER JOIN posts ON users.id = posts.user_id;

                    # Pros:
                        - Single query (no N+1).
                        - Fast for small datasets.
                    # Cons:
                        - Data duplication (user row repeated for each post).
                        - Bad if child table is large (lots of JOIN overhead).

            2. Select-In Eager Loading (selectinload)

                - Runs two queries not (N + 1 ) queries:
                    - Load all parents.
                    - Load all children in one IN (...) query.
                    - Ex:

                        from sqlalchemy.orm import selectinload
                        users = session.query(User).options(selectinload(User.posts)).all()
                        =
                        SELECT users.id, users.name FROM users;

                        SELECT posts.id, posts.title, posts.user_id
                        FROM posts
                        WHERE posts.user_id IN (1, 2, 3, ...);

                        - Pros:
                            - Efficient for large datasets.
                            - Avoids duplication of rows.
                        - Cons:
                            - Still more than one query.
                            - Slightly more complex than joinedload.

            3. Subquery Eager Loading (subqueryload) [Older]

                - Similar to selectinload, but uses a subquery instead of IN (...).
                - Run 2 queries .
                - Ex:

                    from sqlalchemy.orm import subqueryload
                    users = session.query(User).options(subqueryload(User.posts)).all()
                    =
                    SELECT users.id, users.name FROM users;

                    SELECT posts.id, posts.title, anon_1.users_id AS anon_1_users_id
                    FROM (SELECT users.id AS users_id FROM users) AS anon_1
                    JOIN posts ON anon_1.users_id = posts.user_id;

                    - Pros: avoids N+1.
                    - Cons: slower than selectinload, rarely needed in modern apps.

            4. defaultload()

                - defaultload() is not a loader by itself — it’s a wrapper.
                - It’s used to apply a loading option to a nested relationship.
                - When you have a relationship inside a relationship,
                and you want to change how that nested part loads — you wrap it in defaultload().
                - Ex:

                    from sqlalchemy.orm import selectin, defaultload

                    stmt = (
                        select(User).
                        options(
                            selectin(User.posts)
                            .options(defaultload(Post.comments).selectin())
                        )
                    )

                    SQLAlchemy will:
                        - Run a query for users
                        - Run a query for posts (via selectinload)
                        - Run a query for comments (via selectinload)
                        → Three queries, no N+1 problems, and fine-grained control.

            
            5. contains_eager()

                - contains_eager() is used when you’ve already joined the relationship manually in the query (using .join() or .outerjoin()),
                and you want to tell SQLAlchemy:
                    “I’ve already included this relationship in the query, so don’t lazy-load it later.”
                - It basically informs the ORM that:
                    - This join already represents the related data.
                    - So map it into the relationship attribute directly.   

                - Ex:

                    stmt = (
                        select(User)
                        .join(User.posts)  # manual join
                        .options(contains_eager(User.posts))
                    )   
                    Now when SQLAlchemy executes:
                    SELECT users.id, users.name, posts.id, posts.title
                    FROM users JOIN posts ON users.id = posts.user_id;

                    - The ORM will populate User.posts from this query
                    → without issuing any extra lazy loads.

                    - If you omit contains_eager(User.posts),
                    the ORM would:

                        - Build User objects from the users part,
                        - Then later, when you access user.posts,
                        it would issue another query — even though data is already there.

                    
            6. immediateload()

                - Run the second query for the relationship right after the main query — automatically — not later when you access it.
                - So it’s:
                    - not lazy (because it doesn’t wait until you access the attribute)
                    - not joined (because it doesn’t merge into one query)
                    - a separate, immediate second query
                - Ex:
                    
                    from sqlalchemy.orm import immediateload

                    stmt = select(User).options(immediateload(User.posts))
                    users = session.execute(stmt).scalars().all()
                    # Sqlalchemy run these sql queries directly
                    SELECT users.id, users.name FROM users;
                    SELECT posts.id, posts.title, posts.user_id FROM posts WHERE posts.user_id IN (?, ?, ...);

                    - Two queries total, but the second query happens immediately after the - first finishes loading all users.
                    - You don’t need to access user.posts to trigger it — it happens automatically.
                
                - Why It Exists

                    - immediateload() is basically an older eager loading method from before selectinload() was added.
                    - It’s still valid but less efficient on large datasets because:
                        - It loads all related posts in one query (using IN on all user IDs).
                        - But it doesn’t batch or optimize across multiple relationships like selectinload() does.

                    - So:
                        - immediateload() = “Old eager load: two queries, no delay.”
                        - selectinload() = “Improved eager load: two queries, optimized batching.”




## Lazy & Eager Loading Notes:

    1.  techniques = options (they refer to the same set of strategies).
            - The only difference is where you apply them:
                - Permanently on the relationship (lazy="...").
                - Or dynamically on a query (.options(...)). 

    2.  Multiple Loading Options

        - You can pass multiple loading options in one .options() call (or multiple calls).
        - They combine together and affect how SQLAlchemy loads data. 
        - Ex:
            from sqlalchemy.orm import selectinload, defer, load_only

            stmt = (
                select(User)
                .options(
                    selectinload(User.posts),  # eager load relationship
                    defer(User.email),         # defer specific column
                    load_only(User.id, User.name)  # load only selected columns
                )
            )

    3. Chaining Multiple Loading Options
        - You can chain options for nested relationships using .options() inside another loader.
        Ex:
            stmt = (
                select(User)
                .options(
                    selectinload(User.posts)
                    .options(  # chain deeper options
                        load_only(Post.id, Post.title),           # load only specific columns in Post
                        selectinload(Post.comments).defer(Comment.body)  # go deeper into comments
                    )
                )
            )

    4. load_only()
        - load_only() = load only certain columns and defer the rest automatically.
        - Ex:
            stmt = select(User).options(load_only(User.id, User.name))

            stmt = (
                select(User)
                .options(
                    load_only(User.id, User.name),
                    selectinload(User.posts).options(load_only(Post.id, Post.title))
                )
            )


            - Great for performance when you have large tables with unused columns.
            - Automatically defers all other columns.
            - Accessing a deferred column later → triggers an extra query.

    5. raiseload()

        - By default, raiseload() raises an error when a deferred or lazy attribute is accessed.
        - But you can pass raiseload=False to disable this behavior dynamically.
        - Ex:
            stmt = select(User).options(raiseload('*'))
            users = session.execute(stmt).scalars().all()
            # The * symbol in loaders means: Apply the option to all relationships or columns at that level.
            # now user.posts access will raise an error (because of raiseload('*'))

        - Ex:

            stmt = select(User).options(raiseload(False))
            # You’re effectively turning off raiseload behavior globally — it’s rare to use this directly.

        - Ex:

            stmt = select(User).options(raiseload(User.posts, False))
            # Meaning: do not raise errors if posts are accessed (allow lazy load).
            # Usually used when you’ve applied a global raiseload but want to make exceptions.




"""

"""
## Deferred Loading

    - What Is Deferred Loading?

        - Deferred loading = delay loading of certain columns until they are accessed.
        - It’s often used when:
            - You have a table with large text/blob columns (e.g. post body, image data, etc.)
            - You rarely need those columns immediately.
            - You want to make your initial queries faster.

    - Basic defer() on a Regular Column

        from sqlalchemy.orm import defer
        content = defer(Column(TEXT, nullable=False))
        or
        content = mapped_column(TEXT, nullable=False, deferred=True)

        # usage
        post = session.get(Post, 1)  # SELECT id, title FROM posts
        print(post.content)          # triggers SELECT content FROM posts WHERE id = 1

        - Pros:
            - Reduces initial query time when large columns exist.

        - Cons:
            - Extra SQL queries when you finally access deferred fields.

    
    - defer() / undefer() in a Query

        - Even if the column isn’t defined as deferred in the model, you can control it per query.
        - Ex:

            from sqlalchemy.orm import defer, undefer

            posts = session.execute(
                select(Post).options(defer(Post.content))
            ).scalars().all()  # runs id, title only

            print(posts[0].content)  # runs a new SELECT for content

            
            user = session.scalar(
                select(User)
                .where(User.id == 5)
                .options(
                    selectinload(User.posts).undefer(Post.content)  
                )
            )  
            # you must combine a relationship-loading option (selectinload or joinedload) with the column-loading option (undefer) since content is a column in posts not users
            # Runs: SELECT id, title, content FROM posts

    - Defer / Undefer Groups

        - When you have groups of columns that should be loaded/deferred together.
        - Ex:

            class Post(Base):
                __tablename__ = "posts"
                id = mapped_column(Integer, primary_key=True)
                title = mapped_column(String(100))
                summary = column(String(200), deferred_group='non_critical')
                content = mapped_column(Text, deferred_group='non_critical')

            # usage

                session.execute(
                    select(Post).options(defer("non_critical"))
                )  # SELECT id, title FROM posts

                session.execute(
                    select(Post).options(undefer("non_critical"))
                )  # SELECT id, title, summary, content FROM posts


    - raiseload() for Deferred Columns

        - If you use raiseload() instead of defer, SQLAlchemy will raise an error when you try to access the column after it wasn’t loaded — instead of silently running another query.
        - Ex:

            content: Mapped[str] = mapped_column(Text, nullable=False, deferred_raiseload=True)

            or 
            
            from sqlalchemy.orm import raiseload

            post = session.execute(
                select(Post).options(raiseload(Post.content))
            ).scalar_one()

            print(post.content)  # ❌ raises InvalidRequestError
    
"""


"""
## General Notes

1. `delete-orphan`
    - If a child object is no longer associated with its parent, it will be automatically deleted from the database.
    - Ex:
        parent.children.clear()
        session.commit()
        # All child records are deleted because they became orphans


2. `merge`
    - Used when a model instance exists outside the current session (a detached object).
    - It synchronizes that object with the database:
        - If the object’s primary key exists → SQLAlchemy updates the existing record.
        - If not → a new record is inserted.
    - In short:
    Safely “sync” a detached or external object into the current session and database.

3. `expunge`
    - This means: detach an object from the current session.
    - Ex:
        user = session.get(User, 1)
        session.expunge(user)
        session.commit()  # user no longer tracked, changes won’t be saved
    - Now, user is a plain Python object — no connection to the session or DB.
    If you modify it and want to save again, you’d need session.merge(user) later.

4. `single_parent=True`:
    -  It is a Python-side assertion that is typically used to enforce a one-to-one or one-to-many relationship, even when the underlying table structure could technically support more parents.

5. `refresh-expire`:
    - Cascade option that makes related objects expire/refresh when parent does, it triggers a new query when the parent is refreshed

6. `refresh(obj)` vs `expire(obj)` vs `expire_all()`
    - refresh(obj) is a session method that immediately reloads object from DB.
    - expire(obj) is a session method that marks object as expired — reloads only when accessed.
    - expire_all() is a session method that expires all objects tracked by session.

7. Using cascade="all, delete-orphan" everywhere
    - For one to many relationship or exclusive ownership like (Post -> Comment) I can use "all, delete-orphan" for cascade option
    - For many to many relationship, non-exclusive (Author → Books that might have multiple authors) or in case of unsure I should use "save-update, merge" option

"""