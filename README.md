# recruit_exchange_rates

## First step

Copy `.env.example` file into `.env` file and complete variables.
If you run application locally you need db variable for MySQL ip with port. Also you must manually create new database and have running MySQL server.
Also you must add enviromental variable to `.env` file with correct credentials.

```
DATABASE_URL=mysql+pymysql://user_name:password@db_host:db_port/db_name?charset=utf8mb4
```

## How run application locally

Run command

```
uvicorn app.main:app --reload
```

Application runs with CORS for origins below which you can change in `cors.py` if needed

```
"http://localhost",
"http://localhost:8080",
"http://127.0.0.1",
"http://127.0.0.1:8080",
```

### Requirements

Needed requirements are store in requirements.txt file

## Docker

Application can be run by docker application with command below:

```
docker-compose up --build
```

Also database build in container so backend application is ready out of the box.
