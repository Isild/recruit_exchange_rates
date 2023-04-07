from abc import ABC
from sqlalchemy.orm import Session
from ..database import Base
import abc
from pydantic import BaseModel
from datetime import date

from typing import Union


class BaseService(ABC):
    @abc.abstractclassmethod
    def __init__(db: Session):
        """Class constructor."""
        return

    @abc.abstractclassmethod
    def create(model: BaseModel) -> Base:
        """Method for create model instance in database."""
        return

    @abc.abstractclassmethod
    def find(id: int) -> Union[Base, None]:
        """Method for find single model instance in database."""
        return

    @abc.abstractclassmethod
    def find_all(page: int, limit: int, search: str, date_from: date, date_to: date):
        """Method for find all models instance in database."""
        return

    @abc.abstractclassmethod
    def update(model: BaseModel, model_data: BaseModel) -> Base:
        """Method for update model data in database."""
        return

    @abc.abstractclassmethod
    def delete(model: BaseModel) -> Base:
        """Method for delete model from database."""
        return

    @abc.abstractclassmethod
    def get_count_all() -> int:
        """Method for get count of all models in database."""
        return
