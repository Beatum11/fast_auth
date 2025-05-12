
# Authentication & Authorization System using FastAPI

This project is a clean and extensible authentication & authorization API built with **FastAPI** and **SQLModel**, using **JWT tokens**, **Redis** blocklist, and **SQLite** (or any SQL backend). 

---

## Features

- ✅ User registration (`/signup`)
- ✅ User login with JWT token generation (`/signin`)
- ✅ Access/refresh token separation
- ✅ Secure token revocation via Redis blocklist (`/logout`)
- ✅ Token renewal (`/refresh`)
- ✅ Password hashing (via `passlib`)
- ✅ Pydantic validation and error handling
-  Test coverage using `pytest`, `httpx`, and `fakeredis` (IN PROCESS)
- ✅ Docker support

---

## Tech Stack

- **FastAPI**
- **SQLModel** 
- **Redis**
- **JWT**
- **Poetry**
- **Docker**
- **Pytest**

---

## Running Tests

```bash
poetry install
poetry run pytest
````

Make sure you have Redis running or use `fakeredis` for isolated tests.

---

## TODO / Ideas

* [ ] Role-based access control (RBAC)
* [ ] OAuth2 integration (Google, GitHub, etc.)
* [ ] User profile editing & management
* [ ] Email confirmation
* [ ] Rate limiting

---
