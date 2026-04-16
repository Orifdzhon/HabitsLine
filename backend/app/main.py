from fastapi import FastAPI, HTTPException, Depends, Response
from typing import List
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig
import bcrypt

from fastapi.middleware.cors import CORSMiddleware
from app.models import Base, User, Habit, HabitLog
from app.database import engine, session_local
from app.schemas import UserCreate, UserResponse, UserUpdate, HabitCreate, HabitResponse, CreateHabitLog, \
    HabitUpdate, HabitLogResponse, Login

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "JWT_SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["headers", "cookies"]

security = AuthX(config=config)

# натсройка CORS

origins = [
    "https://habitsline.ru",
    "https://www.habitsline.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()




@app.get("/")
async def home() -> dict:
    return {'code': 200, 'message': 'OK'}


# login auth
@app.post("/auth/register", response_model=dict)
async def register_user(user: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password too short")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    db_user = User(name=user.name, age=user.age, email=user.email.lower(), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': 'Account created'}


@app.post("/auth/login", response_model=dict)
async def login_user(user: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if bcrypt.checkpw(user.password.encode(), db_user.password.encode()):
        token = security.create_access_token(uid=str(db_user.id))
        response.set_cookie(
            config.JWT_ACCESS_COOKIE_NAME,
            token,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        return {'message': 'Login successful', 'access_token': token, 'token_type': 'bearer'}
    raise HTTPException(status_code=400, detail="Incorrect email or password")


# CRUD пользователя


@app.get("/users/me", response_model=UserResponse)
async def get_user(token_data = Depends(security.access_token_required), db: Session = Depends(get_db)) -> UserResponse:
    user_id = token_data.sub
    db_user = db.query(User).filter(User.id == int(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/users/me", response_model=UserResponse)
async def update_user(user: UserUpdate, password: str, token_data = Depends(security.access_token_required), db: Session = Depends(get_db)) -> UserResponse:
    user_id = token_data.sub
    db_user = db.query(User).filter(User.id == int(user_id)).first()
    if db_user:
        if bcrypt.checkpw(password.encode(), db_user.password.encode()):
            db_user.name = user.name
            db_user.age = user.age
            db_user.email = user.email
            if user.password is not None:
                hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
                db_user.password = hashed_password
            db.commit()
            db.refresh(db_user)
            return db_user
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/me", response_model=dict)
async def delete_user(password: str, token_data = Depends(security.access_token_required), db: Session = Depends(get_db)) -> dict[str, str]:
    user_id = token_data.sub
    db_user = db.query(User).filter(User.id == int(user_id)).first()
    if db_user:
        if bcrypt.checkpw(password.encode(), db_user.password.encode()):
            db.delete(db_user)
            db.commit()
            return {'message': 'User deleted'}
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/users", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    return db.query(User).all()


# CRUD привычки
@app.post("/habits", response_model=HabitResponse)
async def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    db_habit = Habit(user_id=habit.user_id, name=habit.name, frequency=habit.frequency)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


@app.get("/habits/{id}", response_model=HabitResponse)
async def get_habit(id: int, db: Session = Depends(get_db)) -> HabitResponse:
    db_habit = db.query(Habit).filter(Habit.id == id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="habit not found")
    return db_habit

@app.put("/habits/{id}", response_model=HabitResponse)
async def update_habit(habit: HabitUpdate, id: int, token_data = Depends(security.access_token_required), db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == id).first()
    user_id = int(token_data.sub)
    if db_habit:
        if db_habit.user_id == user_id:
            db_habit.name = habit.name
            db_habit.frequency = habit.frequency
            db.commit()
            db.refresh(db_habit)
            return db_habit
        else:
            raise HTTPException(status_code=404, detail="you have no rights to update this habit")
    raise HTTPException(status_code=404, detail="habit not found")


@app.delete("/habits/{id}", response_model=dict)
async def delete_habit(id: int, token_data = Depends(security.access_token_required), db: Session = Depends(get_db)) -> dict[str, str]:
    db_habit = db.query(Habit).filter(Habit.id == id).first()
    user_id = int(token_data.sub)
    if db_habit:
        if db_habit.user_id == user_id:
            db.delete(db_habit)
            db.commit()
            return {'message': 'Habit deleted'}
        else:
            raise HTTPException(status_code=403, detail="you have no rights to delete this habit")
    raise HTTPException(status_code=404, detail="habit not found")


@app.get("/habits", response_model=List[HabitResponse])
async def get_all_habit_logs(db: Session = Depends(get_db)):
    return db.query(Habit).all()


# HabitLog
@app.post("/habit_logs", response_model=HabitLogResponse)
async def create_habit_log(habit_log: CreateHabitLog, db: Session = Depends(get_db)) -> HabitLogResponse:
    db_habit_log = HabitLog(habit_id= habit_log.habit_id, date=habit_log.date, status=habit_log.status, comment=habit_log.comment)
    db.add(db_habit_log)
    db.commit()
    db.refresh(db_habit_log)
    return db_habit_log


@app.get("/habit_logs/{id}", response_model=HabitLogResponse)
async def get_habit_log(id: int, db: Session = Depends(get_db)):
    db_habit_log = db.query(HabitLog).filter(HabitLog.id == id).first()
    if not db_habit_log:
        raise HTTPException(status_code=404, detail="habit_log not found")
    db.commit()
    db.refresh(db_habit_log)
    return db_habit_log


@app.delete("/habit_logs/{id}", response_model=dict)
async def delete_habit_log(id: int, habit_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    db_habit_log = db.query(HabitLog).filter(HabitLog.id == id).first()
    if db_habit_log:
        if db_habit_log.habit_id == habit_id:
            db.delete(db_habit_log)
            db.commit()
            return {'message': 'Habit deleted'}
        else:
            raise HTTPException(status_code=403, detail="you have no rights to delete this habit_log")
    raise HTTPException(status_code=404, detail="habit_id not found")


@app.get("/habit_logs", response_model=List[HabitLogResponse])
async def get_all_habits(db: Session = Depends(get_db)):
    return db.query(HabitLog).all()