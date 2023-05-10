from pprint import pprint

from classes import HeadHunter, SuperJob, Connector


def main():
    vacancies_json = []
    #keyword = input('Введите ключевое слово для поиска: ')
    keyword = 'Python'
    hh = HeadHunter(keyword)
    sj = SuperJob(keyword)

    for api in (hh, sj):
        api.get_vacancies(pages_count=1)
        vacancies_json.extend(api.get_formatted_vacancies())
        pprint(vacancies_json[0])
        exit()

    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - Вывести список вакансий; \n"
            "exit - Выход.\n"
        )
        if command.lower() == 'exit':
            break
        elif command == '1':
            vacancies = connector.select()

    for vacancy in vacancies:
        print(vacancy, end='\n\n')


if __name__ == '__main__':
    main()
