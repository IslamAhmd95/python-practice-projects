## What are more features to add ?

1️⃣ Email Verification + Password Reset

* Goal:

    When a user signs up, they must verify their email before logging in.
    They can also request a “Forgot Password” link.

* Concepts you’ll learn:

    1. Use async/await (or BackgroundTasks in FastAPI), it doesn’t create a new worker or separate process — just runs concurrently inside the same app.
        - These are in-memory, run inside the same FastAPI process.
        - They don’t need extra servers or queues.
    2. Email sending via SMTP (e.g., Gmail or Mailtrap)
    3. Token-based verification (JWT or unique verification token)

    Password reset flow

* Implementation Steps:

    Add is_verified: bool = False to your User model.

    When registering → send email with verification link (token in query).

    Create /verify-email?token=... route to confirm.

    Add /forgot-password (send email with reset link) and /reset-password (verify + update password).

    Restrict login if not user.is_verified.

        🔐 Optional later: implement token expiry using Redis or a signed timestamp

---

2️⃣ Image Upload (User & Post)

* Concepts you’ll learn:

    1. Use async/await (or BackgroundTasks in FastAPI), it doesn’t create a new worker or separate process — just runs concurrently inside the same app.
        - These are in-memory, run inside the same FastAPI process.
        - They don’t need extra servers or queues.


---

3️⃣ Search (Elasticsearch or OpenSearch)

* Goal:

    Enable powerful post searching (by title/content/tags) using Elasticsearch.

* Concepts you’ll learn:

    - Full-text search engine
    - Syncing your DB data with an index
    - Querying ES for relevant results


---

4️⃣ Notifications System

* Goal:

    When a user gets followed, or their post is liked or commented on, send a notification.

* Concepts you’ll learn:

    - Background jobs (async task queues) "celery & redis"
    - Notification models (user → actor → action → target)
    - Real-time or delayed delivery

* Implementation Steps:

    1. Create Notification model:
    ```python

        class Notification(SQLModel, table=True):
            id: int | None = Field(default=None, primary_key=True)
            receiver_id: int = Field(foreign_key="user.id")
            actor_id: int = Field(foreign_key="user.id")
            action_type: str  # 'follow', 'like', 'comment'
            post_id: int | None = Field(foreign_key="post.id")
            created_at: datetime = Field(default_factory=datetime.utcnow)
            is_read: bool = False
    ```
    2. Whenever a follow/like/comment event happens → create a notification.
    3. Add /notifications route to list user’s notifications.
    4. Later, we can add Celery + Redis for async handling or even WebSockets for real-time delivery.





## Features
celery
redis
email verification
realtime notification
asyncio
file uploading
elastic search