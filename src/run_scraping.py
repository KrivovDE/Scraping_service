import asyncio
import os, sys
from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

from scraping.parser import *
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parsers = (
    (work, 'work'),
    (rabota, 'rabota'),
    (dou, 'dou'),
    (hh, 'hh')
)

jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


# async def main(value):
#     func, url, city, language = value
#     job, err = await loop.run_in_executor(None, func, url, city, language)
#     errors.extend(err)
#     jobs.extend(job)

async def main():
    tasks1 = asyncio.create_task(work(url, city=None, language=None))
    tasks2 = asyncio.create_task(rabota(url, city=None, language=None))
    tasks3 = asyncio.create_task(dou(url, city=None, language=None))
    tasks4 = asyncio.create_task(hh(url, city=None, language=None))

    await asyncio.gather(tasks1, tasks2, tasks3, tasks4)

settings = get_settings()
url_list = get_urls(settings)

# loop = asyncio.get_event_loop()
# # loop = asyncio.get_running_loop()
#
#
# tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
#              for data in url_list
#              for func, key in parsers]
#
# tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
# loop.run_until_complete(tasks)
# loop.close()

# tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
#              for data in url_list
#              for func, key in parsers]

# tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

asyncio.run(main())

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    er = Error(data=errors).save()

# h = codecs.open('../work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()