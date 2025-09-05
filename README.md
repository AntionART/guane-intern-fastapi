# README.md

# Guane Intern FastAPI Project

This project is a FastAPI application designed for managing dog and user operations. It includes various features such as authentication, database interactions, and background tasks.

## Project Structure

```
guane-intern-fastapi
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── settings.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── dog.py
│   │   └── user.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── dog.py
│   │   └── user.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── routes
│   │       ├── __init__.py
│   │       ├── dogs.py
│   │       ├── users.py
│   │       ├── auth.py
│   │       └── files.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── security.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── dog_service.py
│   │   └── external_api.py
│   └── tasks
│       ├── __init__.py
│       ├── celery_app.py
│       └── dog_tasks.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd guane-intern-fastapi
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the FastAPI application, execute the following command:
```
uvicorn app.main:app --reload
```

## Docker

To build and run the application using Docker, use the following commands:
```
docker-compose up --build
```

## Environment Variables

Make sure to create a `.env` file in the root directory with the necessary environment variables.

## License

This project is licensed under the MIT License.