import json
from src.vacancy import Vacancy


class Connector:
    def __init__(self, keyword, vacancies_json):
        self.__filename = f"{keyword.title()}.json"
        self.insert(vacancies_json)

    def insert(self, vacancies_json):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(vacancies_json, file, ensure_ascii=False, indent=4)

    def select(self):
        # vacancies = []
        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        vacancies = [Vacancy(x['id'], x['title'], x['url'], x['salary_from'], x['salary_to'], x['employer'], x['api'])
                     for x in data]
        return vacancies

    def sort_vacancies_by_salary_from_desk(self):
        vacancies = self.select()
        vacancies = sorted(vacancies, reverse=True)
        return vacancies

    def sort_vacancies_by_salary_from_asc(self):
        vacancies = self.select()
        vacancies = sorted(vacancies)
        return vacancies

    def sort_vacancies_by_salary_to_asc(self):
        vacancies = self.select()
        vacancies = sorted(vacancies, key=lambda x: x.salary_to if x.salary_to else 0)
        return vacancies
