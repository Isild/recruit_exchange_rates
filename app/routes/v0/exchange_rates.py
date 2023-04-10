from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from ...schemas import exchange_rate_schemas
from ...dependencies import get_db, get_settings
from ...controllers.exchange_rate_controller import ExchangeRateController

router = APIRouter(
    responses={
        403: {"description": "Permissions denied"},
        404: {"description": "Resource not found"},
        500: {"description": "Server error"}
    },
)

# this is use as a helper to simulate authorization to prevent unauthorized
#  users to have access for sensitive part of the application
is_logged_user = True


@router.post('/exchange-rates/', response_model=exchange_rate_schemas.ExchangeRateDb, status_code=status.HTTP_201_CREATED, tags=["exchange-rates"])
def store_exchange_rate(exchange_rate: exchange_rate_schemas.ExchangeRate, db: Session = Depends(get_db)) -> exchange_rate_schemas.ExchangeRate:
    if not is_logged_user:
        raise HTTPException(status_code=403, detail="Permissions denied")

    controller = ExchangeRateController(db=db)

    return controller.post(exchange_rate)


@router.get('/exchange-rates/', status_code=status.HTTP_200_OK, tags=["exchange-rates"])
def index_exchange_rate_grouped(page: int = 1, limit: int = 100, search: str = None, date_from: date = None, date_to: date = None, order_by: str = "ASC", last_hour: bool = False, db: Session = Depends(get_db)) -> exchange_rate_schemas.ExchangeRate:
    controller = ExchangeRateController(db=db)
    today = date.today()

    if date_from > today:
        date_from = today

    if date_to > today:
        date_to = today

    return controller.index(page=page, limit=limit, search=search, date_from=date_from, date_to=date_to, order_by=order_by, last_hour=last_hour)


@router.get('/exchange-rates/available-currencies', status_code=status.HTTP_200_OK, tags=["exchange-rates"])
def index_exchange_rate():
    return {
        "currencies": [
            {"id": 1, "name": "eur"},
            {"id": 2, "name": "usd"},
            {"id": 3, "name": "gbp"},
            {"id": 4, "name": "jpy"},
        ]
    }


@router.get('/exchange-rates/{id}', response_model=exchange_rate_schemas.ExchangeRateDb, status_code=status.HTTP_200_OK, tags=["exchange-rates"])
def show_exchange_rate(id: int, db: Session = Depends(get_db)):
    controller = ExchangeRateController(db=db)

    return controller.show(id=id)


@router.put("/exchange-rates/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["exchange-rates"])
def put_exchange_rate(id: int, exchange_rate: exchange_rate_schemas.ExchangeRate, db: Session = Depends(get_db)):
    if not is_logged_user:
        raise HTTPException(status_code=403, detail="Permissions denied")

    controller = ExchangeRateController(db=db)

    return controller.put(id=id, model_data=exchange_rate)


@router.delete("/exchange-rates/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["exchange-rates"])
def delete_exchange_rate(id: int, db: Session = Depends(get_db)):
    if not is_logged_user:
        raise HTTPException(status_code=403, detail="Permissions denied")

    controller = ExchangeRateController(db=db)

    return controller.delete(id=id)
