from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
