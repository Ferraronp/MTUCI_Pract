import grequests
from bs4 import BeautifulSoup as bs
from vacancy_model import VacancyParser

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}


def add_params_to_url(url: str, **kwargs) -> str:
    for key in kwargs:
        if isinstance(kwargs[key], list):  # несколько значений для 1 ключа
            for value in kwargs[key]:
                url += f'{key}={value}&'
        else:
            url += f'{key}={kwargs[key]}&'
    return url


def get_vacancy_list(**kwargs) -> list[VacancyParser]:
    url = (f'https://hh.ru/search/vacancy?'
           f'search_field=name&'
           f'search_field=company_name&'
           f'search_field=description&'
           f'enable_snippets=false&'
           f'disableBrowserCache=true&'
           f'hhtmFrom=vacancy_search_list&')
    url = add_params_to_url(url, **kwargs)
    requests = (grequests.get(url + f'page={i}', headers=HEADERS) for i in range(1))

    vacancy_list = list()
    for page_response in grequests.map(requests, size=5):
        parser = bs(page_response.text, 'html.parser')
        info = parser.find_all('div', attrs={"class": "vacancy-search-item__card"})
        for vacancy in info:
            vacancy_parser = bs(str(vacancy), 'html.parser')
            title = vacancy_parser.find('span', attrs={"data-qa": "serp-item__title"})
            title = '' if title is None else title.text
            experience = vacancy_parser.find('span', attrs={"data-qa": "vacancy-serp__vacancy-work-experience"})
            experience = '' if experience is None else experience.text
            work_hours = vacancy_parser.find('span', attrs={"data-qa": "vacancy-label-remote-work-schedule"})
            work_hours = '' if work_hours is None else work_hours.text
            salary = vacancy_parser.find(name='span',
                                         attrs={'class': lambda tag: False if tag is None
                                         else 'compensation-text' in tag})
            salary = '' if salary is None else salary.text
            company = vacancy_parser.find(name='span',
                                          attrs={'class': lambda tag: False if tag is None
                                          else 'company-info-text' in tag})
            company = '' if company is None else company.text
            vacancy_url = vacancy_parser.find('h2', attrs={"data-qa": "bloko-header-2"}).next.next['href']

            address = vacancy_parser.find('span', attrs={"data-qa": "vacancy-serp__vacancy-address"})
            address = '' if address is None else address.text

            metro = vacancy_parser.find('span', attrs={"class": "metro-station"})
            metro = '' if metro is None else metro.text
            vac = VacancyParser(title=title,
                                experience=experience,
                                work_hours=work_hours,
                                salary=salary,
                                company=company,
                                address=address,
                                metro=metro,
                                vacancy_url=vacancy_url)
            vacancy_list.append(vac)
    return vacancy_list
