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
        exit()

    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - Вывести список вакансий; \n"
            "exit - Выход.\n"
        )


if __name__ == '__main__':
    main()
