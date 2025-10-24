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