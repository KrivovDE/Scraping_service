import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def work(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id="pjax-job-list")
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_lst:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({
                    'title': title.text,
                    'url': domain + href,
                    'description': content,
                    'company': company
                })
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors

def rabota(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
        if not new_jobs:
            table = soup.find('table', id="ctl00_content_vacancyList_gridList")
            if table:
                tr_lst = table.find_all('tr', attrs={'id': True})
                for tr in tr_lst:
                    div = tr.find('div', attrs={'class': 'card-body'})
                    if div:
                        title = div.find('h2', attrs={'class': 'card-title'})
                        href = title.a['href']
                        content = div.p.text
                        company = 'No name'
                        p = div.find('p', attrs={'class': 'company-name'})
                        if p:
                            company = p.a.text
                        jobs.append({
                            'title': title.text,
                            'url': domain + href,
                            'description': content,
                            'company': company
                        })
            else:
                errors.append({'url': url, 'title': 'Table does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page is empty'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors

def dou(url):
    jobs = []
    errors = []
    # domain = 'https://jobs.dou.ua/vacancies/?category=Python&search=%D0%BA%D0%B8%D0%B5%D0%B2'
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id="vacancyListId")
        if main_div:
            li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_lst:
                title = li.find('div', attrs={'class': 'title'})
                href = title.a['href']
                cont = li.find('div', attrs={'class': 'sh-info'})
                content = cont.text
                company = 'No name'
                a = title.find('a', attrs={'class': 'company'})
                if a:
                    company = a.text
                jobs.append({
                    'title': title.text,
                    'url': href,
                    'description': content,
                    'company': company
                })
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors

def hh(url):
    jobs = []
    errors = []
    # domain = 'https://voronezh.hh.ru/search/vacancy?area=26&clusters=true&enable_snippets=true&ored_clusters=true&search_field=name&search_field=company_name&text=Python&order_by=publication_time&hhtmFrom=vacancy_search_list'
    resp = requests.get(url, headers=headers)

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
                    'company': company
                })
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors

if __name__ == '__main__':

    url = 'https://voronezh.hh.ru/search/vacancy?area=26&clusters=true&enable_snippets=true&ored_clusters=true&search_field=name&search_field=company_name&text=Python&order_by=publication_time&hhtmFrom=vacancy_search_list'
    jobs, errors = hh(url)

    # url = 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
    # jobs, errors = rabota(url)

    # url = 'https://jobs.dou.ua/vacancies/?category=Python&search=%D0%BA%D0%B8%D0%B5%D0%B2'
    # jobs, errors = dou(url)

    # url = 'https://www.work.ua/ru/jobs-kyiv-python'
    # jobs, errors = work(url)

    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
