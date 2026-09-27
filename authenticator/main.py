from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from auth import AuthHandler
from schemas import AuthDetails, TokenResponse, UserResponse
from models import User
from database import get_db, init_db


app = FastAPI(
    title="Auth Microservice",
    description="A simple authentication microservice",
    version="1.0.0"
)

auth_handler = AuthHandler()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Auth Microservice API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/register", status_code=201, response_model=UserResponse)
def register(auth_details: AuthDetails, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == auth_details.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = auth_handler.get_password_hash(auth_details.password)
    user = User(username=auth_details.username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post("/login", response_model=TokenResponse)
def login(auth_details: AuthDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == auth_details.username).first()

    if not user or not auth_handler.verify_password(auth_details.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = auth_handler.encode_token(user.username)
    return {"access_token": token}


@app.get("/free")
def free_endpoint():
    return {"message": "This is a free endpoint"}


@app.get("/private", response_model=dict)
def private_endpoint(username: str = Depends(auth_handler.auth_wrapper)):
    return {"message": f"Hello {username}", "username": username}