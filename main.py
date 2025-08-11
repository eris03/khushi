import sqlite3
import os
import sqlite3
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from upi_api import router as upi_router
from auth import router as auth_router

# Create FastAPI app with comprehensive OpenAPI configuration
app = FastAPI(
    title="User Management & UPI Payment API",
    description="""
    A comprehensive API for user management and UPI payment processing.
    
    ## Features
    - **User Management**: Complete CRUD operations for user data
    - **UPI Payments**: Mock UPI payment initiation and status tracking
    - **Real-time Updates**: Payment status updates with transaction tracking
    
    ## Usage
    - Use `/docs` for interactive Swagger UI
    - Use `/redoc` for alternative ReDoc documentation
    """,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations related to user management"
        },
        {
            "name": "upi",
            "description": "Operations related to UPI payment processing"
        }
    ]
)

# Enable CORS for frontend access
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'users.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Create database directory and initialize database if it doesn't exist
def init_db():
    db_dir = os.path.join(os.path.dirname(__file__), 'db')
    os.makedirs(db_dir, exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the users table with password field
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL,
        occupation TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# User model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int
    occupation: str

# Create a new user
@app.post("/users/", response_model=User)
def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO users (id, name, email, age, occupation)
        VALUES (?, ?, ?, ?, ?)
        ''', (user.id, user.name, user.email, user.age, user.occupation))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User ID or email already exists")
    finally:
        conn.close()
    
    return user

# Get all users
@app.get("/users/", response_model=List[User])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to User objects
    users = [User(id=row[0], name=row[1], email=row[2], age=row[3], occupation=row[4]) for row in rows]
    return users

# Get user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(id=row[0], name=row[1], email=row[2], age=row[3], occupation=row[4])

# Update user by ID
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    if user_id != updated_user.id:
        raise HTTPException(status_code=400, detail="User ID mismatch")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE users
    SET name = ?, email = ?, age = ?, occupation = ?
    WHERE id = ?
    ''', (updated_user.name, updated_user.email, updated_user.age, updated_user.occupation, user_id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    conn.commit()
    conn.close()
    
    return updated_user

# Delete user by ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    conn.commit()
    conn.close()
    
    return {"detail": "User deleted successfully"}

# Root endpoint to avoid 404 on /
@app.get("/")
def root():
    return {"message": "User Management API is running!"}

app.include_router(upi_router)
