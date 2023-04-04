import json
from fastapi import Depends, status, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
import math

from ...services import exchange_rate_service
from ...schemas import exchange_rate_schemas
from ...dependencies import get_db, get_settings
from ...models import exchange_rate_model

router = APIRouter(
    responses={
        403: {"description": "Permissions denied"},
        404: {"description": "Resource not found"},
        500: {"description": "Server error"}
    },
)


@router.post('/exchange-rates/', response_model=exchange_rate_schemas.ExchangeRateDb, status_code=status.HTTP_201_CREATED, tags=["exchange-rates"])
def store_exchange_rate(exchange_rate: exchange_rate_schemas.ExchangeRate, db: Session = Depends(get_db)) -> exchange_rate_schemas.ExchangeRate:
    created_exchange_rate = exchange_rate_service.create_exchange_rate(
        db=db, exchange_rate=exchange_rate)

    return created_exchange_rate


@router.get('/exchange-rates/', response_model=exchange_rate_schemas.Pagination, status_code=status.HTTP_200_OK, tags=["exchange-rates"])
def index_exchange_rate(page: int = 1, limit: int = 100, search: str = None, date_from: date = None, date_to: date = None, db: Session = Depends(get_db)) -> exchange_rate_schemas.ExchangeRate:
    exchange_rates = exchange_rate_service.get_exchange_rates(
        db=db, page=page, limit=limit, search=search, date_from=date_from, date_to=date_to)

    amount = exchange_rate_service.get_exchange_rates_amount(db=db)
    last_page = math.ceil(amount/limit)

    return exchange_rate_schemas.Pagination(data=exchange_rates, page=page, last_page=last_page, limit=limit)


@router.get('/exchange-rates/{id}', response_model=exchange_rate_schemas.ExchangeRateDb, status_code=status.HTTP_200_OK, tags=["exchange-rates"])
def show_exchange_rate(id: int, db: Session = Depends(get_db)) -> exchange_rate_schemas.ExchangeRate:
    exchange_rates = exchange_rate_service.get_exchange_rate(db=db, id=id)

    return exchange_rates


@router.put("/exchange-rates/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["exchange-rates"])
def put_exchange_rate(id: int, exchange_rate: exchange_rate_schemas.ExchangeRate, db: Session = Depends(get_db)):
    exchange_rate_db = exchange_rate_service.get_exchange_rate(db=db, id=id)

    if exchange_rate_db is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    exchange_rate = exchange_rate_service.update_exchange_rate(
        db=db, exchange_rate_db=exchange_rate_db, exchange_rate_data=exchange_rate)

    return None


@router.delete("/exchange-rates/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["exchange-rates"])
def delete_exchange_rate(id: int, db: Session = Depends(get_db)):
    exchange_rate_db = exchange_rate_service.get_exchange_rate(db=db, id=id)

    if exchange_rate_db is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    exchange_rate_service.delete_exchange_rate(
        db=db, exchange_rate=exchange_rate_db)

    return None
