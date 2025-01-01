from pydantic import BaseModel


class SnippetCreate(BaseModel):
    title: str
    code: str


class SnippetAdd(SnippetCreate):
    user_id: int


class Snippet(SnippetAdd):
    id: str


class SnippetPATCH(BaseModel):
    title:  str | None = None
    code: str | None = None
