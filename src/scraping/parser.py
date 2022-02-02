import requests
from bs4 import BeautifulSoup as BS
from random import randint

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def head_hunter(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'vacancy-serp'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
                for div in div_lst:
                    title = div.find('span', attrs={'class': 'g-user-content'})
                    href = title.a['href']
                    cont = div.find('div', attrs={'class': 'g-user-content'})
                    content = cont.text
                    company = 'No name'
                    div_company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                    if div_company:
                        company = div_company.a.text
                    jobs.append({
                        'title': title.text,
                        'url': href,
                        'description': content,
                        'company': company,
                        'city_id': city,
                        'language_id': language
                    })
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def super_job(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://voronezh.superjob.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': '_3zucV _1RE7b l9LnJ'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'f-test-search-result-item'})
                for div in div_lst:
                    try:
                        title = div.find('span', attrs={'class': '_3a-0Y _3DjcL _3sM6i'})
                        href = title.a['href']
                        cont = div.find('div', attrs={'class': 'HSTPm _3C76h _10Aay _2_FIo _1tH7S'})
                        content = cont.text
                        company = 'No name'
                        div_company = div.find('span', attrs={'class': '_3Fsn4 f-test-text-vacancy-item-company-name _1_OKi _3DjcL _1tCB5 _3fXVo _2iyjv'})
                        if div_company:
                            company = div_company.a.text
                        jobs.append({
                            'title': title.text,
                            'url': domain + href,
                            'description': content,
                            'company': company,
                            'city_id': city,
                            'language_id': language
                        })
                    except AttributeError:
                        """Mute error"""
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def career_habr(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://career.habr.com'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'section-group section-group--gap-medium'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'vacancy-card__info'})
                for div in div_lst:
                    title = div.find('div', attrs={'class': 'vacancy-card__title'})
                    href = title.a['href']
                    cont = div.find('div', attrs={'class': 'vacancy-card__skills'})
                    content = cont.text
                    company = 'No name'
                    div_company = div.find('div', attrs={'class': 'vacancy-card__title'})
                    if div_company:
                        company = div_company.a.text
                    jobs.append({
                        'title': title.text,
                        'url': domain + href,
                        'description': content,
                        'company': company,
                        'city_id': city,
                        'language_id': language
                    })
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors



