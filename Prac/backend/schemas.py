from pydantic import BaseModel

class Category(BaseModel):
    category_id: int
    name: str

class Option(BaseModel):
    id: int
    name: str
    category_id: int

class User(BaseModel):
    id: int

class Vote(BaseModel):
    user_id: int
    category_id: int
    option_id: int