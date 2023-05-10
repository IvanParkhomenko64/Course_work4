from pprint import pprint

from classes import HeadHunter, SuperJob, Connector


def main():
    vacancies_json = []
    #keyword = input('Введите ключевое слово для поиска: ')
    keyword = 'Python'
    hh = HeadHunter(keyword)
    sj = SuperJob(keyword)

    for api in (hh, sj):
        api.get_vacancies(pages_count=2)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - Вывести список вакансий; \n"
            "2 - Сортировать вакансии по минимальной зарплате (убывание); \n"
            "3 - Сортировать вакансии по минимальной зарплате (возрастание); \n"
            "4 - Сортировать вакансии по максимальной зарплате (возрастание); \n"
            "exit - Выход.\n"
        )
        if command.lower() == 'exit':
            break
        elif command == '1':
            vacancies = connector.select()
        elif command == '2':
            vacancies = connector.sort_vacancies_by_salary_from_desk()
        elif command == '3':
            vacancies = connector.sort_vacancies_by_salary_from_asc()
        elif command == '4':
            vacancies = connector.sort_vacancies_by_salary_to_asc()

        for vacancy in vacancies:
          print(vacancy, end='\n\n')


if __name__ == '__main__':
    main()
