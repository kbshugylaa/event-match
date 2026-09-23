import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .catalog import CatalogError, load_catalog, options
from .demos import build_demos
from .matching import match
from .models import START, END, MatchRequest
from .ranking import MODE

ROOT = Path(__file__).resolve().parent.parent


def create_app(catalog_path=None):
    app = FastAPI(title='Event Match KZ', version='0.1.0')
    path = Path(catalog_path or os.environ.get('CATALOG_PATH', ROOT / 'data/contractors.jsonl'))
    profiles, error, demos = [], None, {'scenarios': [], 'unavailable': []}
    try:
        profiles = load_catalog(path)
        demos = build_demos(profiles)
    except CatalogError as exc:
        logging.warning('%s', exc)
        error = ('Исходный CSV/JSONL отсутствует. Добавьте каталог и перезапустите сервер.'
                 if not path.exists() else 'Каталог не прошёл проверку. Подробности — в журнале сервера.')

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, exc):
        return JSONResponse(status_code=422, content={'detail': {
            'message': 'Проверьте поля формы.',
            'errors': [{'field': '.'.join(str(p) for p in e['loc'][1:]), 'message': e['msg']} for e in exc.errors()]}})

    @app.get('/api/options')
    def get_options():
        return {**options(profiles), 'data_ready': error is None, 'data_error': error,
                'catalog_count': len(profiles), 'expected_count': 66,
                'test_data': 'fixtures' in path.parts and 'tests' in path.parts,
                'warnings': [f'Ожидалось 66 профилей, загружено {len(profiles)}.'] if profiles and len(profiles) != 66 else [],
                'calendar': {'start': START.isoformat(), 'end': END.isoformat()}, 'mode': MODE}

    @app.get('/api/demos')
    def get_demos():
        return {**demos, 'data_ready': error is None}

    @app.post('/api/match')
    def post_match(request: MatchRequest):
        if error:
            raise HTTPException(503, detail={'code': 'catalog_unavailable', 'message': error})
        opts = options(profiles)
        for field, key in [('city', 'cities'), ('category', 'categories'), ('event_format', 'event_formats'), ('language', 'languages')]:
            value = getattr(request, field)
            if value is not None and value not in opts[key]:
                raise HTTPException(422, detail={'message': f'Значение поля {field} отсутствует в каталоге.'})
        return match(profiles, request)

    @app.get('/')
    def home():
        return FileResponse(ROOT / 'static/index.html')

    app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')
    return app


app = create_app()
