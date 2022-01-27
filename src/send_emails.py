import os, sys
from django.contrib.auth import get_user_model
import django
from django.core.mail import EmailMultiAlternatives
import datetime

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

django.setup()
from scraping.models import Vacancy, Error, Url
from scraping_service.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f'Расссылка вакансий за {today}'
text_content = f'Расссылка вакансий за {today}'
from_email = EMAIL_HOST_USER

empty = '<h2>Новая информация на сегодня отсутствует.</h2>'


User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
user_dct = {}
for i in qs:
    user_dct.setdefault((i['city'], i['language']), [])
    user_dct[(i['city'], i['language'])].append(i['email'])
if user_dct:
    params = {'city_id__in': [], 'language_id__in': []}
    for pair in user_dct.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in user_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{ row["url"] }">{ row["title"] }</a></h3>'
            html += f'<p>{ row["description"]}</p>'
            html += f'<p>{ row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()
qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data['errors']
    for i in data:
        _html += f'<h5><a href="{ i["url"] }">Error: { i["title"] }</a></h5>'
        subject += f' Ошибки скрапинга {today}'
        text_content += f' Ошибки скрапинга {today}'
    data = error.data['user_data']
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей</h2>'
    for i in data:
        _html += f'<h5>Город: { i["city"] }, Специальность: { i["language"] }, email: { i["email"] }</h5>'
        subject += f'Пожелания пользователей {today}'
        text_content += f'Пожелания пользователей {today}'
qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']): True for i in qs}
urls_err = ''
for keys in urls_dct.keys():
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            urls_err += f'<p> Для города: {keys[0]} и специальности {keys[1]} отсутствуют урлы<p/>'
if urls_err:
    subject += 'Отсутствующие урлы'
    _html += urls_err
if subject:
    msg = EmailMultiAlternatives(_html, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()












