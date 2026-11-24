
# RateGuard
### MongoDB-Powered API Rate Limiting System

RateGuard is a backend-based API rate-limiting system developed using
Python, FastAPI, and MongoDB.

It controls the number of requests a client can make within a
specified time window using the Fixed Window Counter algorithm.

The system identifies clients through API keys, tracks their
requests, and blocks requests that exceed the configured limit.

---

## Features

- API Key Authentication
- Fixed Window Counter Algorithm
- MongoDB-Based Request Tracking
- Atomic Request Counter Updates
- HTTP 429 Too Many Requests Response
- Configurable Request Limits
- Request Analytics
- Database Health Monitoring
- Automated API Testing

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | MongoDB Community Server |
| Database Driver | PyMongo |
| Rate Limiting Algorithm | Fixed Window Counter |
| API Testing | Postman |
| API Documentation | Swagger UI |
| Automated Testing | Pytest |

---

## Project Structure

```text
RateGuard/
├── backend/
│   └── app/
│       ├── routes/
│       ├── services/
│       └── models/
├── tests/
├── documentation/
├── screenshots/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How RateGuard Works

1. A client sends an API request with an API key.
2. RateGuard authenticates the API key.
3. The system identifies the client.
4. MongoDB tracks the client's request count.
5. The Fixed Window Counter algorithm checks the request limit.
6. Requests within the limit are allowed.
7. Excess requests are rejected with HTTP 429.
8. Request statistics are stored for analytics.

---

## Default Configuration

| Setting | Default Value |
|---|---|
| Request Limit | 10 requests |
| Time Window | 60 seconds |
| Database | rateguard_db |
| Algorithm | Fixed Window Counter |

---

## Installation and Setup

### 1. Clone or Download the Project

Obtain the RateGuard project files.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start MongoDB

Make sure your local MongoDB Community Server is running.

### 6. Start the FastAPI Application

```bash
uvicorn backend.app.main:app --reload
```

### 7. Open API Documentation

http://127.0.0.1:8000/docs

---

## Project Objectives

- Understand the working principle of API rate limiting.
- Implement the Fixed Window Counter algorithm.
- Integrate MongoDB for persistent request tracking.
- Prevent excessive API requests.
- Analyse allowed and blocked requests.
- Demonstrate reliable request handling.

---

## Author

Developed as an academic project.

**Project Name:** RateGuard
**Category:** Backend Development / Database Management
