import os, sys
from django.contrib.auth import get_user_model
from django.db import DatabaseError
import datetime as dt


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

# from scraping.parser import *
from scraping.parsers_2 import *
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

# parsers = (
#     (work, 'work'),
#     (rabota, 'rabota'),
#     (dou, 'dou'),
#     (hh, 'hh')
# )
parsers = (
    (hh_vrn_py, 'hh_vrn_py'),
    (sj_vrn_py, 'sj_vrn_py'),
    (ha_vrn_py, 'ha_vrn_py')
    )


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dct:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dct[pair]
            urls.append(tmp)
    return urls


settings = get_settings()
url_list = get_urls(settings)

jobs, errors = [], []

for data in url_list:
    for func, key in parsers:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], language=data['language'])
        jobs += j
        errors += e

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()

ten_days_ago = dt.date.today() - dt.timedelta(14)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()

