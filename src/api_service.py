from abc import ABC, abstractmethod

import json
import os
import requests

from config import DATA_DIR

class Parser(ABC):
    """ Определяет параметры классов, взаимодействующих с API-сервисами """

    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self, *args, **kwargs):
        pass

class HeadHunterAPI(Parser):
    """ Класс для работы с API HeadHunter """

    def __init__(self, file_worker):
        super().__init__()
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100, 'area': 113}
        self.vacancies = []
        self.file_worker = file_worker

    def load_vacancies(self, keyword):
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            fetched_vacancies = response.json()['items']

            for vacancy in fetched_vacancies:
                if keyword.lower() in vacancy['name'].lower():
                    self.vacancies.append(vacancy)
            self.params['page'] += 1
        return self.vacancies
