from pydantic import BaseModel, Field
from datetime import datetime as date_type
from typing import List


class ExchangeRateBase(BaseModel):
    rate: float = Field(
        title="The currency exchange rate",
        description="The currency exchange rate being in given date",
        eq=0,
        example=2.137001,
    )
    date: date_type = Field(
        title="The date time",
        description="The date time of the exchange rate storaging in UTC",
        example="2022-11-06 12:00",
    )
    currency: str = Field(
        title="The currency",
        description="The name of the expenditure",
        min_length=3,
        max_length=3,
        example="Name",
    )

    class Config:
        orm_mode = True


class ExchangeRate(ExchangeRateBase):
    pass


class ExchangeRateDb(ExchangeRate):
    id: int = Field(
        title="The resource ID",
        description="The resource ID",
        eq=1,
        example=1,
    )


class Pagination(BaseModel):
    data: List[ExchangeRateDb] = Field(
        title="The exchange rates data",
        description="The exchange rates data.",
    )
    page: int = Field(
        title="The total pages amount",
        description="The total pages amount.",
    )
    last_page: int = Field(
        title="The last page number",
        description="The last page number of pagination.",
    )
    limit: int = Field(
        title="The limit of displaying data",
        description="The limit of displaying data.",
    )
