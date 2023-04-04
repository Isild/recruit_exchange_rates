from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from datetime import date

from ..models import exchange_rate_model
from ..schemas import exchange_rate_schemas


def create_exchange_rate(db: Session, exchange_rate: exchange_rate_schemas.ExchangeRateDb) -> exchange_rate_model.ExchangeRateModel:
    db_exchange_rate = exchange_rate_model.ExchangeRateModel(
        **exchange_rate.dict())

    db.add(db_exchange_rate)
    db.commit()
    db.refresh(db_exchange_rate)

    return db_exchange_rate


# -> list(exchange_rate_model.ExchangeRateModel):
def get_exchange_rates(db: Session, page: int = 1, limit: int = 100, search: str = None, date_from: date = None, date_to: date = None):
    query = db.query(exchange_rate_model.ExchangeRateModel)

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


def get_exchange_rate(db: Session, id: int) -> exchange_rate_model.ExchangeRateModel:
    return db.query(exchange_rate_model.ExchangeRateModel).filter(exchange_rate_model.ExchangeRateModel.id == id).first()


def update_exchange_rate(db: Session, exchange_rate_db: exchange_rate_model.ExchangeRateModel, exchange_rate_data: exchange_rate_model.ExchangeRateModel) -> bool:
    db.query(exchange_rate_model.ExchangeRateModel).filter(
        exchange_rate_model.ExchangeRateModel.id == exchange_rate_db.id).update(exchange_rate_data.dict())
    db.commit()
    db.refresh(exchange_rate_db)

    return exchange_rate_db


def delete_exchange_rate(db: Session, exchange_rate: exchange_rate_model.ExchangeRateModel) -> bool:
    db.delete(exchange_rate)
    db.commit()

    return exchange_rate


def get_exchange_rates_amount(db: Session) -> int:
    query = db.query(exchange_rate_model.ExchangeRateModel)

    return query.with_entities(func.count()).scalar()
