"""Дополнительные материалы привязаны к id, не изменяют исходный CSV."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PortfolioItem(BaseModel):
    model_config = ConfigDict(extra='forbid')
    src: str
    alt: str = Field(min_length=1, max_length=250)
    caption: str = Field(min_length=1, max_length=500)
    source: str = Field(min_length=1, max_length=500)
    demonstration: bool = False

    @field_validator('src')
    @classmethod
    def local_image(cls, value):
        if not re.fullmatch(r'/static/portfolio/[A-Za-z0-9_-]+\.(?:png|jpg|jpeg|webp)', value):
            raise ValueError('Ожидается локальное изображение /static/portfolio/имя.png|jpg|jpeg|webp')
        return value


class Supplement(BaseModel):
    model_config = ConfigDict(extra='forbid')
    source: str = Field(min_length=1)
    phone: str | None = None
    email: str | None = None
    messenger: str | None = None
    portfolio: list[PortfolioItem] = Field(default_factory=list)

    @field_validator('phone')
    @classmethod
    def valid_phone(cls, value):
        if value is not None and not re.fullmatch(r'\+?[0-9 ()-]{7,25}', value):
            raise ValueError('Некорректный телефон')
        return value

    @field_validator('email')
    @classmethod
    def valid_email(cls, value):
        if value is not None and not re.fullmatch(r'[^\s@?&#]+@[^\s@?&#]+\.[^\s@?&#]+', value):
            raise ValueError('Некорректный email')
        return value

    @field_validator('messenger')
    @classmethod
    def valid_messenger(cls, value):
        if value is not None:
            parsed = urlparse(value)
            if parsed.scheme != 'https' or parsed.hostname not in {'t.me','wa.me'} or parsed.username or parsed.password:
                raise ValueError('Допустимы предоставленные HTTPS-ссылки t.me или wa.me')
        return value


def load_supplements(path, profiles, root):
    if not Path(path).is_file():
        return {}
    raw = json.loads(Path(path).read_text(encoding='utf-8'))
    ids = {p.id for p in profiles}
    if not isinstance(raw, dict) or set(raw) - ids:
        raise ValueError('Неизвестные id в дополнительных материалах')
    result = {}
    for key, value in raw.items():
        item = Supplement.model_validate(value)
        for picture in item.portfolio:
            if not (root / picture.src.lstrip('/')).is_file():
                raise ValueError(f'Изображение не найдено: {picture.src}')
        result[key] = item.model_dump()
    return result
