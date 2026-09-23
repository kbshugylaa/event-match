from .explanations import explain
from .ranking import MODE, rank, relevance

STEPS = ('busy', 'format', 'budget', 'hours', 'language')
REASONS = {'busy': 'Заняты на выбранную дату', 'format': 'Не поддерживают формат',
           'budget': 'Стартовая цена выше бюджета', 'hours': 'Недостаточно часов',
           'language': 'Нет выбранного языка'}


def rejection(profile, request):
    if request.date in profile.busy_dates:
        return 'busy'
    if request.event_format not in profile.event_formats:
        return 'format'
    if profile.price_from_kzt > request.budget_kzt:
        return 'budget'
    if request.hours is not None and profile.max_hours is not None and profile.max_hours < request.hours:
        return 'hours'
    if request.language and request.language not in profile.languages:
        return 'language'
    return None


def match(profiles, request):
    pool = [p for p in profiles if p.city == request.city and request.category in p.categories]
    counts = dict.fromkeys(STEPS, 0)
    excluded, eligible = [], []
    for profile in pool:
        reason = rejection(profile, request)
        if reason:
            counts[reason] += 1
            excluded.append({'id': profile.id, 'name': profile.anon_name, 'reason': reason})
        else:
            eligible.append(profile)
    ordered = rank(eligible, request)
    cards = []
    for profile in ordered[:3]:
        score, overlap = relevance(profile, request)
        cards.append({**profile.model_dump(mode='json'), 'score': score, 'matched_words': overlap,
                      'availability': f'Не занят по календарю на {request.date.isoformat()}',
                      'explanation': explain(profile, request, overlap)})
    return {'status': 'matched' if eligible else ('no_eligible_candidates' if pool else 'no_category_in_city'),
            'mode': MODE, 'found_count': len(eligible), 'shown_count': len(cards),
            'pool_count': len(pool), 'funnel': counts, 'excluded': excluded,
            'recommendations': cards,
            'shortfall': ('В городе нет выбранной категории.' if not pool else
                          f'В городе в этой категории {len(pool)}; исключено условиями {len(pool)-len(eligible)}; осталось {len(eligible)}.')
                         if len(eligible) < 3 else None}
