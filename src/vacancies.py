from typing import Any


class Vacancy():
    """ Определяет параметры для использования вакансий с API-сервиса api.hh.ru """

    def __init__(self, data: dict) -> None:
        self.__vacancy_id: int = data.get('id')
        self.__name: str = data.get('name')
        self.__town: str = data.get('area', {}).get('name', '')

        salary = data.get('salary')
        if isinstance(salary, dict):
            self.__salary_from = salary.get('from', 0) if isinstance(salary.get('from'), (int, float)) else 0
            self.__salary_to = salary.get('to', 0) if isinstance(salary.get('to'), (int, float)) else 0
        else:
            self.__salary_from = 0
            self.__salary_to = 0

        description = data.get('snippet', {}).get('responsibility', '')  # Change default to empty string
        self.__description = (description.replace('<highlighttext>', '').replace
                              ('</highlighttext>','')) if description else 'Описание не указано'

        self.__alternate_url = data.get('alternate_url')

        requirement = data.get('snippet', {}).get('requirement', '')  # Change default to empty string
        self.__requirement = (requirement.replace('<highlighttext>', '').replace
                              ('</highlighttext>','')) if requirement else 'Требования не указаны'

    def __str__(self) -> str:
        """ Возвращает формат для вывода строкового значения вакансии"""
        return (f"{self.__name.strip()}, зарплата от {self.__salary_from}, {self.__town.strip():<15}\n"
                f"{self.__alternate_url.strip()}\n"
                f"Описание вакансии: {self.__description.strip():<100}\n"
                f"Требования к вакансии: {self.__requirement.strip():<100}\n\n")

    def __gt__(self, other: Any) -> Any:
        """ Сортирует список вакансий по ключу salary_from в порядке убывания """
        return self.__salary_from > other.salary_from

    @property
    def salary_from(self) -> int:
        """ Разрешает доступ к атрибуту salary_from """
        return self.__salary_from

    @property
    def description(self) -> str:
        """ Разрешает доступ к атрибуту description """
        return self.__description

    def to_dict(self) -> dict:
        """ Преобразует экземпляр в словарь для выгрузки в JSON """
        return {
            'name': self.__name,
            'area': self.__town,
            'salary_from': self.__salary_from,
            'salary_to': self.__salary_to,
            'alternate.url': self.__alternate_url,
            'requirement': self.__requirement,
        }

    @classmethod
    def from_list(cls, data_list: list) -> list:
        unique_vacancies = {}
        vacancies_list = []  # Формируем список вакансий, удовлетворяющих требованиям
        for data in data_list:
            if isinstance(data, dict):
                vacancy_id = data.get('id')
                if vacancy_id not in unique_vacancies:
                    unique_vacancies[vacancy_id] = cls(data)
                    vacancies_list.append(unique_vacancies[vacancy_id])
        return vacancies_list
