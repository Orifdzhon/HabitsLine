from pydantic import BaseModel, EmailStr, Field
from typing import Optional



# User CRUD
class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True


class UserDelete(UserResponse):
    id: int


# Habit CRUD
class HabitBase(BaseModel):
    user_id: int
    name: str
    frequency: str


class HabitCreate(HabitBase):
    pass


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None


class HabitResponse(HabitBase):
    id: int
    class Config:
        from_attributes = True


class HabitDelete(HabitBase):
    id: int


# HabitLog
class HabitLogBase(BaseModel):
    habit_id: int
    date: str
    status: str
    comment: str
    class Config:
        from_attributes = True


class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    date: str
    status: str
    comment: str


class CreateHabitLog(BaseModel):
    habit_id: int
    date: str
    status: str
    comment: str


# Login Auth
class Login(BaseModel):
    email: EmailStr
    password: str