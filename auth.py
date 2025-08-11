from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import os
import hashlib

router = APIRouter(prefix="/auth", tags=["authentication"])

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "users.db")

class UserSignup(BaseModel):
    name: str
    email: str
    age: int
    occupation: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/signup")
def signup(user: UserSignup):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        hashed_password = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (name, email, age, occupation, password) VALUES (?, ?, ?, ?, ?)",
            (user.name, user.email, user.age, user.occupation, hashed_password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        return {
            "success": True,
            "message": "User created successfully",
            "user": {
                "id": user_id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "occupation": user.occupation
            }
        }
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        conn.close()

@router.post("/login")
def login(user: UserLogin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    hashed_password = hash_password(user.password)
    cursor.execute(
        "SELECT id, name, email, age, occupation FROM users WHERE email = ? AND password = ?",
        (user.email, hashed_password)
    )
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user_data[0],
                "name": user_data[1],
                "email": user_data[2],
                "age": user_data[3],
                "occupation": user_data[4]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
