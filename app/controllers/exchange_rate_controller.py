import math
from sqlalchemy.orm import Session
from datetime import date
from fastapi import Depends, HTTPException

from ..services.exchange_rate_service import ExchangeRateService
from ..database import Base
from ..schemas.exchange_rate_schemas import ExchangeRate
from ..schemas import exchange_rate_schemas
from .base_controller import BaseController


class ExchangeRateController(BaseController):
    def __init__(self, db: Session):
        self.db = db
        self.service = ExchangeRateService(db=db)

        return

    def post(self, model: ExchangeRate) -> ExchangeRate:
        self.service = ExchangeRateService(db=self.db)

        return self.service.create(model=model)

    def show(self, id: int) -> ExchangeRate:
        exchange_rate_db = self.service.find(id=id)

        if exchange_rate_db is None:
            raise HTTPException(status_code=404, detail="Resource not found")

        return exchange_rate_db

    def index(self, page: int, limit: int, search: str, date_from: date, date_to: date):
        exchange_rates = self.service.find_all(
            page=page, limit=limit, search=search, date_from=date_from, date_to=date_to)

        amount = self.service.get_count_all()
        last_page = math.ceil(amount/limit)

        return exchange_rate_schemas.Pagination(data=exchange_rates, page=page, last_page=last_page, limit=limit)

    def put(self, id: int, model_data: ExchangeRate) -> bool:
        exchange_rate_db = self.service.find(id=id)

        if exchange_rate_db is None:
            raise HTTPException(status_code=404, detail="Resource not found")

        exchange_rate = self.service.update(
            model=exchange_rate_db, model_data=model_data)

        return True

    def delete(self, id: int) -> bool:
        exchange_rate_db = self.service.find(id=id)

        if exchange_rate_db is None:
            raise HTTPException(status_code=404, detail="Resource not found")

        self.service.delete(model=exchange_rate_db)

        return True
