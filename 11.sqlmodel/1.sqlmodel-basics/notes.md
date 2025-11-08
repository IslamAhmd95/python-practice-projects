## 🧩 Serialization & Deserialization in Pydantic and SQLModel

### 💡 Basic Idea

* **Serialization** = converting a Python object (like a User instance) into a format that can be sent or stored — e.g. a JSON response.
* **Deserialization** = converting incoming data (like a JSON request) into a Python object that your app can use.

In FastAPI, **Pydantic** (and by extension **SQLModel**) handle both automatically.

---

### ⚙️ Example: Basic Flow with Pydantic

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int | None

    model_config = {"from_attributes": True}
```

#### 🧠 When a request comes in:

```json
{
  "name": "Islam",
  "email": "islam@example.com",
  "age": 25
}
```

* FastAPI uses **Pydantic** to *deserialize* this JSON into a `UserCreate` Python object.
* The fields are validated (email format, type checks, etc.).

#### ✅ When sending a response:

If your API returns a SQLAlchemy or SQLModel instance like:

```python
return user
```

FastAPI automatically *serializes* it into JSON — **but only fields defined in** `UserRead` are included.

Example response:

```json
{
  "id": 1,
  "name": "Islam",
  "email": "islam@example.com",
  "age": 25
}
```

This serialization is powered by `UserRead.model_config = {"from_attributes": True}` — it allows Pydantic to read attributes directly from ORM models.

---

### 🧰 Inserting Data:

#### Example (SQLModel version):

```python
user = User.model_validate(data)
```

* The User model has the model_validate method because it inherits from SQLModel, which itself inherits from Pydantic's BaseModel.


#### Example (SQLAlchemy version):

```python
user = User(name=data.name, email=data.email, ...)

# or

user = User(**data.model_dump()) # cleaner approach
```

* When data is an instance of a Pydantic model (like your UserCreate schema), data.model_dump() converts its validated attributes into a plain Python dictionary. The ** operator then unpacks that dictionary's key-value pairs as keyword arguments to the User constructor.


---

### 🧰 Updating Data: Handling Partial Updates

When you want to update a model, you often don’t want to overwrite all fields — only those provided.

#### Example (SQLModel version):

```python
user_data = data.model_dump(exclude_unset=True)
user.sqlmodel_update(user_data)
```

* `model_dump(exclude_unset=True)` → converts only provided (non-default) fields into a dictionary.
* `sqlmodel_update()` → updates the SQLModel instance with those fields.

This avoids changing fields that were not included in the request.

#### Example request body:

```json
{ "name": "Updated Name" }
```

Only `name` will be updated.


#### Same Update Logic with Pydantic Only

If you use plain Pydantic models (no SQLModel):

```python
update_data = data.model_dump(exclude_unset=True)
for key, value in update_data.items():
    setattr(user, key, value)
```

This does the same thing — manually applying only changed fields.

---

### 🧩 SQLModel’s Dual Nature

`SQLModel` = `SQLAlchemy` + `Pydantic`

* As an **SQLAlchemy model**, it can define tables, columns, constraints, and relationships.
* As a **Pydantic model**, it can validate data and serialize responses.

Example:

```python
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: EmailStr = Field(unique=True)
    age: int | None = Field(default=None, ge=18)
```

This single model:
✅ Creates a real SQL table
✅ Validates input data
✅ Serializes output data

---

### ⚖️ SQLModel vs SQLAlchemy + Pydantic

| Feature          | SQLAlchemy | Pydantic          | SQLModel              |
| ---------------- | ---------- | ----------------- | --------------------- |
| Table definition | ✅          | ❌                 | ✅                     |
| Validation       | ❌          | ✅                 | ✅                     |
| Serialization    | ❌          | ✅                 | ✅                     |
| Relationships    | ✅          | ❌                 | ✅                     |
| Simplicity       | ⚙️ Verbose | Clean (data only) | 🌟 Clean + full power |

---

### 🚀 Summary

* **Deserialization:** JSON → Pydantic/SQLModel instance (via request body validation)
* **Serialization:** ORM instance → JSON (via `response_model`)
* **`exclude_unset`** → only send or update provided fields
* **SQLModel** gives you the beauty of Pydantic and power of SQLAlchemy

> Use **SQLModel** if you want cleaner code for both ORM and validation. Use **SQLAlchemy + Pydantic** separately if you need the latest features or advanced control.
