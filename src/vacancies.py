from src.api_service import HeadHunterAPI


class Vacancy:
    """ Определяет параметры для использования вакансий с API-сервиса api.hh.ru """

    def __init__(self, data):
        self.vacancy_id = data.get('id')
        self.name = data.get('name')
        self.town = data.get('area', {}).get('name', '')

        salary = data.get('salary')
        if isinstance(salary, dict):
            self.salary_from = salary.get('from', 0) if isinstance(salary.get('from'), (int, float)) else 0
            self.salary_to = salary.get('to', 0) if isinstance(salary.get('to'), (int, float)) else 0
        else:
            self.salary_from = 0
            self.salary_to = 0

        description = data.get('snippet', {}).get('responsibility', 'Описание не указано')
        if description is None:
            description = 'Описание не указано'
        self.description = (description.replace('<highlighttext>', '')
                            .replace('</highlighttext>', ''))

        self.alternate_url = data.get('alternate_url')

        requirement = data.get('snippet', {}).get('requirement', 'Требования не указаны')
        if requirement is None:
            requirement = 'Требования не указаны'
        self.requirement = (requirement.replace('<highlighttext>', '')
                            .replace('</highlighttext>', ''))
        self.alternate_url = data.get('alternate_url')

    def __str__(self):
        return (f"{self.name.strip()}, зарплата от {self.salary_from}, {self.town.strip():<15}\n"
                f"{self.alternate_url.strip()}\n"
                f"Описание вакансии: {self.description.strip():<100}\n"
                f"Требования к вакансии: {self.requirement.strip():<100}\n\n")

    def __gt__(self, other):
        """ Сортирует список вакансий по ключу salary_from в порядке убывания """
        return self.salary_from > other.salary_from

    def to_dict(self):
        """ Converts the Vacancy instance to a dictionary for JSON serialization. """
        return {
            'name': self.name,
            'area': self.town,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'alternate.url': self.alternate_url,
            'requirement': self.requirement,
        }

    @classmethod
    def from_list(cls, data_list):
        unique_vacancies = {}
        vacancies_list = []  # Формируем список вакансий, удовлетворяющих требованиям
        for data in data_list:
            if isinstance(data, dict):
                vacancy_id = data.get('id')
                if vacancy_id not in unique_vacancies:
                    unique_vacancies[vacancy_id] = cls(data)
                    vacancies_list.append(unique_vacancies[vacancy_id])
        return vacancies_list


if __name__ == "__main__":
    hh_api = HeadHunterAPI('data/vacancies.json')
    keyword = input('Введите поисковый запрос :')
    hh_api.load_vacancies(keyword)
    for vacancy in hh_api.vacancies:
        print(vacancy)

    vacancies_list = Vacancy.from_list(hh_api.vacancies)
    print(len(vacancies_list))
    for vacancy in vacancies_list:
        print(vacancy)
