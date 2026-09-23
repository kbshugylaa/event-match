""Локальные аккаунты: SQLite, scrypt, непрозрачные серверные сессии."""
import hashlib
import hmac
import re
import secrets
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

COOKIE = 'event_match_session'
SESSION_SECONDS = 24 * 60 * 60
HASH_LOCK = threading.Semaphore(2)  # Ограничиваем одновременную память scrypt.


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    with HASH_LOCK:
        digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=2**17, r=8, p=1,
                                maxmem=256*1024*1024, dklen=32).hex()
    return f'scrypt$131072$8$1${salt}${digest}'


def verify_password(password, stored):
    try:
        _, n, r, p, salt, digest = stored.split('$')
        if (n, r, p) != ('131072', '8', '1'):
            return False
        return hmac.compare_digest(hash_password(password, salt), stored)
    except (ValueError, TypeError):
        return False


class LoginInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)

    @field_validator('email')
    @classmethod
    def email_valid(cls, value):
        value = value.strip().casefold()
        if not re.fullmatch(r'[A-Za-z0-9.!#$%&\x27*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}', value):
            raise ValueError('Введите корректный email')
        return value


class RegisterInput(LoginInput):
    name: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=12, max_length=128)
    password_confirm: str = Field(min_length=12, max_length=128)

    @field_validator('name')
    @classmethod
    def name_valid(cls, value):
        value = value.strip()
        if not value or any(ord(c) < 32 for c in value):
            raise ValueError('Введите имя')
        return value

    @model_validator(mode='after')
    def matching_passwords(self):
        if self.password != self.password_confirm:
            raise ValueError('Пароли не совпадают')
        if not self.password.strip():
            raise ValueError('Пароль не может состоять из пробелов')
        return self


class AuthStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY, name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at INTEGER NOT NULL);
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY, user_id INTEGER REFERENCES users(id),
                    csrf TEXT NOT NULL, expires_at INTEGER NOT NULL, search_json TEXT);
                CREATE TABLE IF NOT EXISTS auth_limits (
                    key TEXT PRIMARY KEY, attempts INTEGER NOT NULL, started_at INTEGER NOT NULL);
            ''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            db.close()

    def throttle(self, key):
        now = int(time.time())
        key = hashlib.sha256(key.encode()).hexdigest()
        with self.connect() as db:
            db.execute('DELETE FROM auth_limits WHERE started_at < ?', (now-900,))
            db.execute('INSERT INTO auth_limits VALUES (?,1,?) ON CONFLICT(key) DO UPDATE SET attempts=attempts+1', (key, now))
            attempts = db.execute('SELECT attempts FROM auth_limits WHERE key=?', (key,)).fetchone()[0]
        if attempts > 20:
            raise HTTPException(429, detail={'message':'Слишком много попыток. Повторите через 15 минут.'})

    def register(self, data):
        password_hash = hash_password(data.password)
        try:
            with self.connect() as db:
                user_id = db.execute('INSERT INTO users(name,email,password_hash,created_at) VALUES (?,?,?,?)',
                           (data.name, data.email, password_hash, int(time.time()))).lastrowid
            return user_id
        except sqlite3.IntegrityError as exc:
            raise HTTPException(409, detail={'message':'Этот email уже зарегистрирован. Войдите в аккаунт.'}) from exc

    def login(self, data):
        with self.connect() as db:
            user = db.execute('SELECT * FROM users WHERE email=?', (data.email,)).fetchone()
        # Одинаковая дорогая операция для неизвестного email и неверного пароля.
        stored = user['password_hash'] if user else f'scrypt$131072$8$1${"00"*16}${"00"*32}'
        valid = verify_password(data.password, stored)
        if not user or not valid:
            raise HTTPException(401, detail={'message':'Неверный email или пароль.'})
        return user['id']

    def create_session(self, user_id=None):
        token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        with self.connect() as db:
            db.execute('DELETE FROM sessions WHERE expires_at <= ?', (int(time.time()),))
            db.execute('INSERT INTO sessions(token_hash,user_id,csrf,expires_at) VALUES (?,?,?,?)',
                       (self.token_hash(token), user_id, csrf, int(time.time())+SESSION_SECONDS))
        return token

    @staticmethod
    def token_hash(token):
        return hashlib.sha256(token.encode()).hexdigest()

    def session(self, token):
        if not token or len(token) > 128:
            return None
        with self.connect() as db:
            row = db.execute('''SELECT s.*,u.name,u.email FROM sessions s LEFT JOIN users u ON s.user_id=u.id
                                WHERE token_hash=? AND expires_at>?''',
                             (self.token_hash(token), int(time.time()))).fetchone()
        return dict(row) if row else None

    def revoke(self, token):
        if token:
            with self.connect() as db:
                db.execute('DELETE FROM sessions WHERE token_hash=?', (self.token_hash(token),))

    def save_search(self, session, value):
        with self.connect() as db:
            db.execute('UPDATE sessions SET search_json=? WHERE token_hash=?', (value, session['token_hash']))
app/catalog.py
app/demos.py
app/explanations.py
import re

from .ranking import tokens


def explain(profile, request, overlap):
    # Короткая точная цитата о запросе, не оценка качества или пересказ всего профиля.
    sentences = [s.strip(' •—') for s in re.split(r'(?<=[.!?])\s+|\n+|•',profile.description)]
    wishes = tokens(request.wishes)
    candidates = [s for s in sentences if tokens(s)&set(overlap)]
    fragment = max(candidates,key=lambda s:(len(tokens(s)&wishes),len(tokens(s)&set(overlap)),-len(s)),default=None)
    if fragment and len(fragment)>260:
        fragment = fragment[:257].rsplit(' ',1)[0]+'…'
    gap = f'{request.budget_kzt - profile.price_from_kzt:,.2f}'.rstrip('0').rstrip('.').replace(',', ' ')
    first = (f'В описании указано: «{fragment.rstrip(".!?")}».' if fragment else
             f'Профиль поддерживает формат «{request.event_format}» в городе {profile.city}'
             + (f' и язык «{request.language}».' if request.language else '.'))
    return first + f' Разница бюджета со стартовой ценой — {gap} ₸; итоговая стоимость требует уточнения.'
