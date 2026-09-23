from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator

START, END = date(2026, 9, 23), date(2026, 12, 31)
Text = Annotated[StrictStr, Field(min_length=1, max_length=500)]


class Profile(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: Text
    anon_name: Text
    categories: list[Text] = Field(min_length=1)
    city: Text
    price_from_kzt: Annotated[float, Field(ge=0, allow_inf_nan=False, strict=True)]
    event_formats: list[Text] = Field(min_length=1)
    languages: list[Text] = Field(min_length=1)
    max_hours: Annotated[float, Field(gt=0, allow_inf_nan=False, strict=True)] | None
    busy_dates: list[date]
    description: StrictStr = Field(max_length=10000)
    synthetic: StrictBool
    city_imputed: StrictBool
    price_imputed: StrictBool

    @field_validator('id', 'anon_name', 'city')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('Пустая строка недопустима')
        return value.strip()

    @field_validator('categories', 'event_formats', 'languages')
    @classmethod
    def lists(cls, values):
        cleaned = [v.strip() for v in values]
        if any(not v for v in cleaned) or len(set(cleaned)) != len(cleaned):
            raise ValueError('Список содержит пустые или повторные значения')
        return cleaned

    @field_validator('busy_dates', mode='before')
    @classmethod
    def calendar_shape(cls, values):
        if not isinstance(values, list):
            raise ValueError('Календарь должен быть списком дат YYYY-MM-DD')
        for value in values:
            if type(value) is date:
                continue
            if not isinstance(value, str) or len(value) != 10:
                raise ValueError('Дата должна иметь формат YYYY-MM-DD')
            if date.fromisoformat(value).isoformat() != value:
                raise ValueError('Дата должна иметь формат YYYY-MM-DD')
        return values

    @field_validator('busy_dates')
    @classmethod
    def calendar(cls, values):
        if len(set(values)) != len(values) or any(not START <= d <= END for d in values):
            raise ValueError('Повторы или даты вне календаря 23.09–31.12.2026')
        return values


class MatchRequest(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
    city: Text
    date: date
    event_format: Text
    category: Text
    budget_kzt: Annotated[float, Field(ge=0, le=1e12, allow_inf_nan=False, strict=True)]
    hours: Annotated[float, Field(gt=0, le=1000, allow_inf_nan=False, strict=True)] | None = None
    language: Text | None = None
    wishes: str = Field(default='', max_length=1000)

    @field_validator('city', 'category', 'event_format', 'language')
    @classmethod
    def request_nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Значение не может быть пустым')
        return value

    @field_validator('date', mode='before')
    @classmethod
    def request_date_shape(cls, value):
        if type(value) is date:
            return value
        if not isinstance(value, str) or len(value) != 10 or date.fromisoformat(value).isoformat() != value:
            raise ValueError('Дата должна иметь формат YYYY-MM-DD')
        return value

    @field_validator('date')
    @classmethod
    def date_range(cls, value):
        if not START <= value <= END:
            raise ValueError('Выберите дату с 23.09.2026 по 31.12.2026')
        return value
