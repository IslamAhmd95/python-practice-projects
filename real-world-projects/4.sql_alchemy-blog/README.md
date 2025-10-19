# 📝 SQLAlchemy Blog

## 📘 Overview
**SQLAlchemy Blog** is a backend-only blog application built with **Python** and **SQLAlchemy ORM**.  
It demonstrates how to model complex relationships, perform CRUD operations, and handle business logic purely with SQLAlchemy — no web framework involved.

This project mimics real-world backend logic for a blogging system with entities like **Users, Posts, Comments, Tags, Profiles, and Likes**, all connected through relational models.

---

## ⚙️ Features
- **Users Management** — Create, update, delete users and their profiles.  
- **Posts CRUD** — Users can create, edit, view, and delete posts.  
- **Comments CRUD** — Add or update comments under posts.  
- **Tags Management** — Tag posts and fetch posts by tag.  
- **Likes System** — Like or unlike both posts and comments.  
- **Follow System** — Users can follow/unfollow each other.  
- **Relationships** —  
  - One-to-many: user → posts, post → comments  
  - Many-to-many: users ↔ followers, posts ↔ tags, users ↔ likes  

---

## 🧩 Tech Stack
| Tool | Purpose |
|------|----------|
| **Python 3.x** | Programming language |
| **SQLAlchemy ORM** | ORM and database management |
| **Alembic** | For database migrations |
| *(Future step)* **Pydantic** | Planned next layer for validating requests |
| *(Future step)* **FastAPI** | Planned next layer for API endpoints |

---


## 🚀 How to Run

1. **Clone the repo**

   ```
        git clone https://github.com/IslamAhmd95/python-practice-projects.git
        cd real-world-projects/4.sql_alchemy-blog
    ```

2. **Create a virtual environment**

    ```
        python3 -m venv venv
        source venv/bin/activate
    ```


3. **Install dependencies**

    ```
        pip install -r requirements.txt
    ```

4. **Run seed**

    ```
        python -m scripts.seed
    ```

5. **Run the example demo**

    ```
        python main.py
    ```


You’ll see console output for all CRUD operations (create, read, update, delete) across users, posts, comments, tags, and likes.