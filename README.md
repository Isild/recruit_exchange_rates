# recruit_exchange_rates

## First step

Copy `.env.example` file into `.env` file and complete variables.
To db variable you need MySQL ip with port. Also you must manually create new database.

## How DB

MySQL database runs in docker container with comand below:

```
docker-compose up --build
```

## How run application

Run command

```
uvicorn app.main:app --reload
```
