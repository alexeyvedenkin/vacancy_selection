from src.api_service import HeadHunterAPI


class Vacancy:
    """ Определяет параметры для использования вакансий с API-сервиса api.hh.ru """

    def __init__(self, data):
        self.vacancy_id = data.get('id')
        self.name = data.get('name')
        self.town = data.get('area', {}).get('name', '')

        # Adjust handling of salary_range to avoid NoneType errors
        salary_range = data.get('salary_range')  # Get salary_range directly
        if isinstance(salary_range, dict):  # Ensure it's a dictionary
            self.salary_from = salary_range.get('from', 0) if isinstance(salary_range.get('from'), (int, float)) else 0
            self.salary_to = salary_range.get('to', 0) if isinstance(salary_range.get('to'), (int, float)) else 0
        else:
            self.salary_from = 0  # Default if salary_range is None or not a dict
            self.salary_to = 0  # Default if salary_range is None or not a dict

        self.requirement = (data.get('snippet', {}).get('requirement', 'Требования не указаны')
                            .replace('<highlighttext>', '').replace('</highlighttext>', ''))
        self.alternate_url = data.get('alternate_url')

    def __str__(self):
        return (f'''{self.name}, зарплата от {self.salary_from}, {self.town}, {self.alternate_url}, 
        требования к вакансии: {self.requirement}\n''')

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

    def __gt__(self, other):
        """ Сортирует список вакансий по ключу salary_from в порядке убывания """
        return self.salary_from > other.salary_from

    @classmethod
    def from_list(cls, data_list):
        unique_vacancies = {}
        vacancies_list = []  # Формируем список вакансий, удовлетворяющих требованиям
        for data in data_list:
            if isinstance(data, dict):
                vacancy_id = data.get('alternate_url')
                if vacancy_id not in unique_vacancies:
                    unique_vacancies[vacancy_id] = cls(data)
                    vacancies_list.append(unique_vacancies[vacancy_id])
        return vacancies_list


if __name__ == "__main__":
    hh_api = HeadHunterAPI('data/vacancies.json')
    hh_api.load_vacancies("машинист")
    for vacancy in hh_api.vacancies:
        print(vacancy)

    vacancies_list = Vacancy.from_list(hh_api.vacancies)
    print(len(vacancies_list))
    for vacancy in vacancies_list:
        print(vacancy)
