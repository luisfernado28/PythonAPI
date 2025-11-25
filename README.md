# Python API developed with FASTAPI

A small FastAPI-based user (employee) management API using SQLite and SQLAlchemy. It provides endpoints to list, create and authenticate employees with JWT access and refresh tokens.

Features
- FastAPI endpoints for employees and authentication
- SQLite database (no external DB server required)
- Password hashing (Argon2 via `passlib`) and JWT tokens (`python-jose`)

Tech stack
- Python 3.13
- FastAPI
- SQLAlchemy (SQLite)
- Pydantic models for request/response validation
- `passlib` (Argon2) for password hashing
- `python-jose` for JWT handling

Requirements

This project includes a pinned `requirements.txt` file generated with `pip freeze`. Install the exact versions with:

```powershell
pip install -r requirements.txt
```

Key packages (as of the latest `requirements.txt`):

- `fastapi==0.121.3`
- `uvicorn==0.38.0` (recommended for serving the app)
- `SQLAlchemy==2.0.44`
- `pydantic==2.12.4` and `pydantic_core==2.41.5`
- `passlib==1.7.4` and `argon2-cffi==25.1.0` (password hashing)
- `python-jose==3.5.0` (JWT encoding/decoding)
- `python-dotenv==1.2.1` (load `.env` files)

For the full list of pinned packages and exact versions, open `requirements.txt` in the project root.

Quickstart

1) Create and activate a virtual environment (optional but recommended):

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

2) Install dependencies:

```powershell
pip install -r requirements.txt
# If you want to run with uvicorn and it's not in requirements:
pip install "uvicorn[standard]"
```

3) Environment variables

Create a `.env` file or set the following environment variables in your shell:

- `JWT_SECRET_KEY` — secret for access tokens
- `JWT_REFRESH_SECRET_KEY` — secret for refresh tokens

Example `.env` content:

```env
JWT_SECRET_KEY=change_this_to_a_strong_random_value
JWT_REFRESH_SECRET_KEY=change_this_to_another_random_value
```

4) Run the app locally

```powershell
# from the repository root
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The server will create a `database.db` SQLite file in the project root (see `src/repositories/database.py`).

API Endpoints

- GET `/employees`
	- Returns: list of employee objects (name, last_name, email, user_type)

- GET `/employee/{employee_email}`
	- Path param: `employee_email` (string)
	- Returns: employee object or 404 if not found

- POST `/employee`
	- Body: `Employee` model (see validation rules below)
	- Creates a new employee (password is hashed before saving)

- POST `/login`
	- Form data (OAuth2 password flow): `username` (email), `password`
	- Returns: `access_token` and `refresh_token`

Validation / Notes
- Emails are validated against a pattern and currently expect the `@example.com` domain (see `src/schemas/EmpSchema.py`). Adjust the regex there if you want to accept other domains.
- Passwords must be at least 8 characters.
- `user_type` is an enum with values `admin` or `client` (see `EmployeeType` enum).

Examples

Create an employee (curl):

```bash
curl -X POST "http://127.0.0.1:8000/employee" -H "Content-Type: application/json" -d \
'{"id":1,"name":"John","last_name":"Doe","email":"john@example.com","password":"strongpass123","user_type":"client"}'
```

Login (using OAuth2 password form):

```bash
curl -X POST "http://127.0.0.1:8000/login" -F "username=john@example.com" -F "password=strongpass123"
```

Notes for developers
- Database: `sqlite:///./database.db` (configured in `src/repositories/database.py`).
- Models: SQLAlchemy model `UserDB` in `src/models/empModels.py` and Pydantic schemas in `src/schemas/EmpSchema.py`.
- Business logic: `src/services/EmployeeBL.py` implements get/create/login utilities.
- Auth helpers: JWT creation and password hashing live in `src/utils/auth.py`.

Security and common caveats
- Ensure `JWT_SECRET_KEY` and `JWT_REFRESH_SECRET_KEY` are set to strong random values in production.
- Consider relaxing or updating the email regex in `EmpSchema.py` for real-world usage.
- Argon2 hashing is used; keep `passlib` and its dependencies updated.

Contributing
- Feel free to open issues or submit pull requests. Suggested improvements:
	- Add unit tests
	- Improve request validation and error responses
	- Add Docker support and migration tooling

License
- See `LICENSE` file in the repository root.

Next steps
- To run the app locally: set environment variables, install deps, then run `uvicorn api:app --reload`.
- I can also add a simple Postman collection, Dockerfile, or GitHub Actions workflow if you'd like — tell me which and I'll scaffold it.
