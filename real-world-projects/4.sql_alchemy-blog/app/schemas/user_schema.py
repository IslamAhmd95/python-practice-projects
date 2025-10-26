from pydantic import BaseModel, EmailStr, ConfigDict

class ReadUserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bio: str | None = None

class ReadUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    email: EmailStr
    profile: ReadUserProfile

class AfterDeleteUser(BaseModel):
    message: str

class UpdateMe(BaseModel):
    name: str | None = None
    username: str | None = None
    email: EmailStr | None = None
    bio: str | None = None

class AfterUpdateMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: ReadUser
    message: str

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

class AfterUpdatePassword(BaseModel):
    message: str
