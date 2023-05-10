from abc import ABC, abstractmethod
import json
import os
import requests
from pprint import pprint


class ParsingError(Exception):
    def __str__(self):
        return 'Ошибка получения данных по API.'


class Vacancy:
    __slots__ = ('id', 'title', 'url', 'salary_from', 'salary_to', 'employer', 'api')

    def __init__(self, vacancy_id, title, url, salary_from, salary_to, employer, api):
        self.id = vacancy_id
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.employer = employer
        self.api = api

    def __gt__(self, other):
        if not other.salary_min:
            return True
        elif not self.salary_min:
            return False


class Connector:
    def __int__(self, keyword, vacancies_json):
        self.__filename = f"{keyword.title()}.json"
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies_json, file, ensure_ascii=False, indent=4)

    def select(self):
        # vacancies = []
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        vacancies = [Vacancy(x['id'], x['title'], x['salary_from'], x['salary_to'], x['employer'], x['api']) for x in
                     data]
        return vacancies


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunter(Engine):
    def __init__(self, keyword):
        self.__header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0"}
        self.__params = {
            "text": keyword,
            "page": 0,  # номер страницы
            "per_page": 100  # количество отображаемых записей на странице
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):
        formatted_salary = [None, None]
        if salary and salary['from'] and salary['from'] != 0:
            formatted_salary[0] = salary['from'] if salary['currency'].lower() == 'rur' else salary['from'] * 80
        if salary and salary['to'] and salary['to'] != 0:
            formatted_salary[1] = salary['to'] if salary['currency'].lower() == 'rur' else salary['to'] * 80
        return formatted_salary

    def get_request(self):
        response = requests.get('https://api.hh.ru/vacancies', headers=self.__header, params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_vacancies(self, pages_count=1):
        while self.__params['page'] < pages_count:
            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных!')
                break
            print(f"Найдено ({len(values)}) вакансий.")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy['salary'])
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['name'],
                'api': 'HeadHunter'
            })
        return formatted_vacancies


class SuperJob(Engine):
    def __init__(self, keyword):
        self.__header = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}
        self.__params = {
            "text": keyword,
            "page": 0,  # номер страницы
            "count": 100  # количество отображаемых записей на странице
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary, currency):
        formatted_salary = None
        if salary and salary != 0:
            formatted_salary = salary if currency == 'rub' else salary * 80
        return formatted_salary

    def get_request(self):
        response = requests.get('https://api.superjob.ru/2.0/vacancies', headers=self.__header, params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['objects']

    def get_vacancies(self, pages_count=1):
        while self.__params['page'] < pages_count:
            print(f"SuperJob, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных!')
                break
            print(f"Найдено ({len(values)}) вакансий.")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy['salary'])
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'salary_from': self.get_salary(vacancy['payment_from'], vacancy['currency']),
                'salary_to': self.get_salary(vacancy['payment_to'], vacancy['currency']),
                'employer': vacancy['firm_name'],
                'api': 'Superjob'
            })
        return formatted_vacancies
