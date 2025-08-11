# Backend API Documentation

## Overview
This backend is built with FastAPI and provides RESTful API endpoints for user management and UPI payment integration.

## User Management Endpoints

- **GET /users/**  
  Retrieve a list of all users.

- **GET /users/{user_id}**  
  Retrieve details of a specific user by ID.

- **POST /users/**  
  Create a new user.  
  Request body:  
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 25,
    "occupation": "Engineer"
  }
  ```

- **PUT /users/{user_id}**  
  Update an existing user by ID.  
  Request body same as POST.

- **DELETE /users/{user_id}**  
  Delete a user by ID.

## UPI Payment Integration Endpoints

- **POST /upi/payment**  
  Initiate a UPI payment.  
  Request body:  
  ```json
  {
    "payer_vpa": "payer@upi",
    "payee_vpa": "payee@upi",
    "amount": 100.50,
    "transaction_note": "Payment for services"
  }
  ```  
  Response:  
  ```json
  {
    "transaction_id": "TXN000001",
    "status": "PENDING",
    "message": "Payment initiated successfully"
  }
  ```

- **GET /upi/status/{transaction_id}**  
  Get the status of a UPI payment transaction.  
  Response:  
  ```json
  {
    "transaction_id": "TXN000001",
    "status": "PENDING",
    "message": "Transaction status retrieved successfully"
  }
  ```

## Swagger UI

The API documentation is automatically generated and available at:  
`http://localhost:8000/docs`

This includes all user management and UPI payment endpoints with request/response schemas.

## Running the Backend

1. Install dependencies:  
   `pip install -r requirements.txt`

2. Start the server:  
   `uvicorn backend.main:app --reload`

3. Access API docs at:  
   `http://localhost:8000/docs`

## Notes

- The UPI payment endpoints are mock implementations for demonstration.
- The user data is stored in a SQLite database located at `backend/db/users.db`.
