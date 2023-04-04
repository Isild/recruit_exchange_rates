from app.dependencies import get_db
from fastapi import FastAPI, Request, Depends
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import imp

from .database import Base, engine
from .config import cors
from .routes.v0 import exchange_rates
from .jobs import get_exchange_rates_job

Base.metadata.create_all(bind=engine)

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.add_job(
    get_exchange_rates_job.get_actual_exchange_rates, 'interval', seconds=3600)

try:
    scheduler.start()
except:
    scheduler.shutdown()


# middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors.origins,
    allow_credentials=True,
    allow_methods=cors.allow_methods,
    allow_headers=cors.allow_headers,
)

# app


@app.get("/", tags=["app"])
def read_root(request: Request):

    return {
        "version": "v0.1",
        "documentation":  "/docs"
    }


app.include_router(
    exchange_rates.router,
    prefix="/v0",
)
