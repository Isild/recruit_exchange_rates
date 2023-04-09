from sqlalchemy.orm import Session
from sqlalchemy import or_, func, asc, desc
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.sql import text

from ..models import exchange_rate_model
from ..schemas import exchange_rate_schemas
from .base_service import BaseService
from ..helpers import requests_handling


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

    def find_all(self, page: int = 1, limit: int = 100, search: str = None, date_from: datetime = None, date_to: datetime = None, order_by: str = "ASC", last_hour: bool = False):
        query = self.db.query(exchange_rate_model.ExchangeRateModel)

        if order_by == "ASC":
            query = query.order_by(
                asc(exchange_rate_model.ExchangeRateModel.date))
        elif order_by == "DESC":
            query = query.order_by(
                desc(exchange_rate_model.ExchangeRateModel.date))

        if search:
            query = query.filter(or_(exchange_rate_model.ExchangeRateModel.currency.contains(
                search), exchange_rate_model.ExchangeRateModel.rate.contains(search)))

        if date_from:
            query = query.filter(
                exchange_rate_model.ExchangeRateModel.date >= date_from)

        if date_to:
            time = datetime.max.time()
            date_to = datetime.combine(date_to, time)

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

    def get_last_exchagne_rate_datetime(self, m_date: date):
        search = "{}%".format(m_date)
        query = self.db.query(exchange_rate_model.ExchangeRateModel).\
            order_by(desc(exchange_rate_model.ExchangeRateModel.date)).\
            filter(exchange_rate_model.ExchangeRateModel.date.like(search))

        try:
            return query.first().date
        except:
            return None

    def check_is_db_has_actual_data_form_date(self, m_date: date) -> bool:
        time_to_check = datetime.combine(m_date, datetime.now().time())
        last_db_date = self.get_last_exchagne_rate_datetime(m_date=m_date)

        try:
            return not last_db_date + timedelta(hours=1) <= time_to_check
        except:
            return False

    def synchronise_exrange_rate_data(self, m_date: date) -> bool:
        response = requests_handling.get_current_day_exchange_rate()
        data = response.json()

        timestamp = data['timestamp']
        last_db_timestamp = self.get_last_exchagne_rate_datetime(m_date=m_date)

        if timestamp != last_db_timestamp:
            self.create(exchange_rate_schemas.ExchangeRateBase(
                eur=data['rates']['EUR'], gbp=data['rates']['GBP'], jpy=data['rates']['JPY'], usd=data['rates']['USD'],
                date=datetime.fromtimestamp(timestamp, tz=timezone.utc)))

    def get_history_exrange_rate_data(self, m_date: date) -> bool:
        response = requests_handling.get_historical_day_exchange_rate(
            data_date=m_date)
        data = response.json()

        timestamp = data['timestamp']

        self.create(exchange_rate_schemas.ExchangeRateBase(
            eur=data['rates']['EUR'], gbp=data['rates']['GBP'], jpy=data['rates']['JPY'], usd=data['rates']['USD'],
            date=datetime.fromtimestamp(timestamp, tz=timezone.utc)))

        return True
