from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from datetime import date

from ..models import exchange_rate_model
from ..schemas import exchange_rate_schemas
from .base_service import BaseService


class ExchangeRateService(BaseService):
    def __init__(self, db: Session) -> exchange_rate_model.ExchangeRateModel:
        self.db = db

    def create(self, model: exchange_rate_schemas.ExchangeRateDb) -> exchange_rate_model.ExchangeRateModel:
        db_exchange_rate = exchange_rate_model.ExchangeRateModel(
            **model.dict())

        self.db.add(db_exchange_rate)
        self.db.commit()
        self.db.refresh(db_exchange_rate)

        return db_exchange_rate

    def find(self, id: int) -> exchange_rate_model.ExchangeRateModel:
        db_exchange_rate = self.db.query(exchange_rate_model.ExchangeRateModel).filter(
            exchange_rate_model.ExchangeRateModel.id == id).first()

        return db_exchange_rate

    def find_all(self, page: int = 1, limit: int = 100, search: str = None, date_from: date = None, date_to: date = None):
        query = self.db.query(exchange_rate_model.ExchangeRateModel)

        if search:
            query = query.filter(or_(exchange_rate_model.ExchangeRateModel.currency.contains(
                search), exchange_rate_model.ExchangeRateModel.rate.contains(search)))

        if date_from:
            query = query.filter(
                exchange_rate_model.ExchangeRateModel.date >= date_from)

        if date_to:
            query = query.filter(
                exchange_rate_model.ExchangeRateModel.date <= date_to)

        return query.offset((page - 1) * limit).limit(limit).all()

    def update(self, model: exchange_rate_model.ExchangeRateModel, model_data: exchange_rate_model.ExchangeRateModel) -> bool:
        self.db.query(exchange_rate_model.ExchangeRateModel).filter(
            exchange_rate_model.ExchangeRateModel.id == model.id).update(model_data.dict())
        self.db.commit()
        self.db.refresh(model)

        return model

    def delete(self, model: exchange_rate_model.ExchangeRateModel) -> bool:
        self.db.delete(model)
        self.db.commit()

        return model

    def get_count_all(self) -> int:
        query = self.db.query(exchange_rate_model.ExchangeRateModel)

        return query.with_entities(func.count()).scalar()
