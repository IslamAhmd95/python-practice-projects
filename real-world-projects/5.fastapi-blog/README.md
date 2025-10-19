# 🧠 FastAPI Blog API

A simple yet complete **FastAPI project** that demonstrates user authentication, JWT-based access tokens, and CRUD operations for blog posts.

---

## 🚀 Features

- ✅ **User Registration & Login**
- 🔐 **JWT Authentication** (access tokens)
- 🧩 **Protected Routes** (require valid token)
- 🗄️ **SQLAlchemy ORM** for database access
- 📦 **Environment Variables** using `.env`
- 📘 **Automatic Swagger Docs** at `/docs`

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
    git clone https://github.com/IslamAhmd95/python-practice-projects/

    cd real-world-projects/5.fastapi-blog/
```

### 2. Create Virtual Environment

```

    python3 -m venv venv
    source venv/bin/activate      # On Linux/macOS
    # or
    venv\Scripts\activate         # On Windows


```

### 3. Install Dependencies

```

    pip install -r requirements.txt

```

### 4. Create .env file

    - cp .env .env.example
    - Fill your env secrets

### 5. Run the Server

```

    uvicorn app.main:app --reload

```