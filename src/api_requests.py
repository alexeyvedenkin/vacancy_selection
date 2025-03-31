from abc import ABC, abstractmethod

import json
import requests


class ApiService(ABC):
    """ Определяет параметры классов, взаимодействующих с API-сервисами """

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass


class RequestHeadHunter(ApiService):
    """ Определяет параметры взаимодействия с API-сервисом hh.ru"""

    base_url = "https://api.hh.ru/vacancies"

    def __init__(self, base_url=None):
        """ Конструктор дла класса RequestHeadHunter """
        self.base_url = base_url if base_url else RequestHeadHunter.base_url  # Сохраняем базовый URL

    def get_data(self, params=None):  # Установлено динамическое изменение параметров
        """ Получает данные от API-сервиса hh.ru"""

        if params is None:  # Если параметры не указаны
            params = {}

        url = self.base_url  # Использован базовый URL для обращения к API

        try:
            response = requests.get(url, params=params)  # Параметры включены в запрос
            response.raise_for_status()  # Проверка корректности ответа от API

            return response.json()  # Возвращаем ответ в формате JSON

        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при запросе: {e}")  # Обработка ошибок
            return None  # Возвращаем None при ошибке, чтобы исключить случайный доступ к данным

class SortedByCurrency:
    """ Производит сортировку ответа от API-сервиса по валюте для выплаты зарплаты """
    vacancy_rus = {}
    vacancy_other = {}

    def __init__(self, api_service: dict, sort_key):
        self.api_service = api_service  # Экземпляр RequestHeadHunter
        # self.sort_key = sort_key  # Ключ для сортировки

    @classmethod
    def country_sort(cls):
        pass

class SortedApiResult:
    """ Производит сортировку результатов SortedByCurrency по заданному параметру """
    def __init__(self, api_service, sort_key):
        self.api_service = api_service  # Экземпляр RequestHeadHunter
        self.sort_key = sort_key  # Ключ для сортировки

    def get_sorted_results(self):
        results = self.api_service.get_data()  # получение данных от RequestHeadHunter
        if results is None or 'items' not in results:  # проверка корректности
            return []  # возвращаем пустой список при ошибке

        if not isinstance(results['items'], list):  # проверка наличия ключа 'items'
            return []  # возвращаем пустой список при ошибке

        # Filter to include only dictionaries in the sorting process
        items_to_sort = [item for item in results['items'] if isinstance(item, dict)]

        # Sort items, providing a default value (e.g., 0) for missing keys
        return sorted(items_to_sort,
                      key=lambda x: x.get(self.sort_key, 0))  # Sort by specified key, default to 0 if None


if __name__ == "__main__":
    api = RequestHeadHunter()  # Создаем экземпляр класса
    data = api.get_data({"page": 0, "per_page": 20, "text": "Главный бухгалтер"})  # Передаем параметры запроса

    # Проверяем, что data не None, и что это словарь с ключом 'items'
    if data and isinstance(data, dict) and 'items' in data:
        if data['items']:  # Проверяем, что 'items' не пуст
            for item in data['items']:
                print(item)  # Печатаем каждый элемент
        else:
            print("Нет данных")  # Обработка пустого списка items
    else:
        print("Нет данных или формат ответа от API некорректный")  # Обработка других случаев

    sorted_api_result = SortedApiResult(api, "salary_from")  # Убедитесь, что 'salary_from' существует в данных
    sorted_results = sorted_api_result.get_sorted_results()
    print(json.dumps(sorted_results, indent=2))
