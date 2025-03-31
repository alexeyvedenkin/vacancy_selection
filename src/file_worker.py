import os
import json
from abc import ABC, abstractmethod
from config import DATA_DIR
from src.api_requests import RequestHeadHunter


class BaseWorker(ABC):
    """ Обязывает дочерние классы реализовать методы для добавления вакансий в файл """

    @abstractmethod
    def file_output(self):
        pass


class JSONWorker(BaseWorker):
    """ Реализует методы для добавления вакансий в JSON-файл """

    def __init__(self, data, filename):
        """
        Инициализатор класса JSONWorker.

        :param data: Данные для сохранения.
        :param filename: Имя файла без расширения.
        """
        self.data = data  # Сохраняем данные
        self.filename = filename  # Сохраняем имя файла

    def file_output(self):
        """Метод для экспорта данных в JSON-файл в директорию data."""
        # Путь к файлу, который будет создан
        file_path = os.path.join(DATA_DIR, f"{self.filename}.json")  # Определяем полный путь к файлу
        with open(file_path, 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump(self.data, file, ensure_ascii=False)  # Записываем данные в формате JSON


if __name__ == "__main__":
    # Пример использования
    api = RequestHeadHunter()  # Создаем экземпляр класса
    hh_data = api.get_data({"page": 0, "per_page": 20, "text": "Главный бухгалтер"})  # Передаем параметры запроса
    exporter = JSONWorker(hh_data, 'vacancies')  # Создаем объект класса с данными и именем файла
    exporter.file_output()  # Вызываем метод для экспорта