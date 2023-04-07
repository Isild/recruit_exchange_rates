from sqlalchemy import Column, Integer, String, DateTime, Float
from typing import List

from ..database import Base


class ExchangeRateModel(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    # I use this kind of column when I want to add extra secure for data to avoid
    #  get data from nearby based on id, but it depends on project
    # uuid = Column(String, unique=True, index=True)
    rate = Column(Float)
    date = Column(DateTime)
    currency = Column(String)
