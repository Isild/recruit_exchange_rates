from app.dependencies import get_db
from fastapi import FastAPI, Request
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
import time
from decouple import config
from sqlalchemy import event

from .database import Base, engine
from .config import cors
from .routes.v0 import exchange_rates
from .jobs import get_exchange_rates_job
from .models.exchange_rate_model import ExchangeRateModel
from .helpers.db_seeders import initialize_table


event.listen(ExchangeRateModel.__table__, 'after_create', initialize_table)

Base.metadata.create_all(bind=engine)

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.add_job(
    get_exchange_rates_job.get_actual_exchange_rates, 'interval', seconds=int(config('JOB_INTERVAL')))

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
