"""Фиксированный режим words-v1: доля уникальных слов запроса в description."""
import re

STOPWORDS = {'и', 'в', 'на', 'с', 'по', 'для', 'из', 'к', 'а', 'но', 'или', 'не', 'от', 'до'}
MODE = 'words-v1'


def tokens(text):
    return set(re.findall(r'[^\W_]+', text.casefold().replace('ё', 'е'), re.UNICODE)) - STOPWORDS


def relevance(profile, request):
    query = tokens(f'{request.event_format} {request.category} {request.wishes}')
    overlap = sorted(query & tokens(profile.description))
    return len(overlap) / max(1, len(query)), overlap


def rank(profiles, request):
    return sorted(profiles, key=lambda p: (-relevance(p, request)[0], p.id))
