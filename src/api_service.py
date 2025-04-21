from abc import ABC, abstractmethod


import requests


class Parser(ABC):
    """ Определяет параметры классов, взаимодействующих с API-сервисами """

    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self, *args, **kwargs):
        pass

class HeadHunterAPI(Parser):
    """ Класс для работы с API HeadHunter """

    def __init__(self, file_worker: str) -> None:
        super().__init__()
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100, 'area': 113}
        self.__vacancies = []
        self.__file_worker = file_worker

    def get_vacancies(self) -> list:
        """ Осуществляет доступ к приватному атрибуту """
        return self.__vacancies

    def load_vacancies(self, keyword: str) -> list:
        """ Метод для загрузки вакансий с сайта api.hh.ru """
        self.__params['text'] = keyword
        while self.__params.get('page') != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            fetched_vacancies = response.json()['items']

            for vacancy in fetched_vacancies:
                if keyword.lower() in vacancy['name'].lower():
                    self.__vacancies.append(vacancy)
            self.__params['page'] += 1
        return self.__vacancies
