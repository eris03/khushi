# Frontend React App

## Setup and Run

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The app will be available at http://localhost:3000

# Backend FastAPI App

## Setup and Run

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
```bash
venv\\Scripts\\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn
```

4. Run the FastAPI server:
```bash
uvicorn backend.main:app --reload
```

The backend API will be available at http://localhost:8000

## Notes

- The frontend React app expects the backend API to be running on http://localhost:8000
- The login page uses a simple hardcoded username/password (admin/password) for demonstration.
- The user management page allows full CRUD operations on users.
