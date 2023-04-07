import abc
from abc import ABC
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from ..services.base_service import BaseService
from ..database import Base

class BaseController(ABC):
    @abc.abstractclassmethod
    def __init__(db: Session, service: BaseService):
        """Class constructor."""
        return

    @abc.abstractclassmethod
    def post(model: BaseModel) -> Base:
        """Method for create model instance in database."""
        return

    @abc.abstractclassmethod
    def show(id: int) -> Base:
        """Method for find single model instance in database."""
        return

    @abc.abstractclassmethod
    def index(page: int, limit: int, search: str, date_from: date, date_to: date):
        """Method for find all models instance in database."""
        return

    @abc.abstractclassmethod
    def put(model: BaseModel, model_data: BaseModel) -> bool:
        """Method for update model data in database."""
        return

    @abc.abstractclassmethod
    def delete(id: id) -> bool:
        """Method for delete model from database."""
        return
