from pydantic import BaseModel


class Post(BaseModel):
    id: str | None
    name: str
    description: str
    filename_server: str


class PostUpdate(BaseModel):
    name: str
    description: str
