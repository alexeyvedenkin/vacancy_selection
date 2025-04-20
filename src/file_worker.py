import json
import os
from abc import ABC, abstractmethod

from config import DATA_DIR


class BaseWorker(ABC):
    """ Обязывает дочерние классы реализовать методы для добавления вакансий в файл """

    @abstractmethod
    def file_output(self):
        pass


class JSONWorker(BaseWorker):
    """ Реализует методы для добавления вакансий в JSON-файл """

    def __init__(self, data, filename):
        """ Инициализатор класса JSONWorker """
        self.data = data  # Сохраняем данные
        self.filename = filename  # Сохраняем имя файла

    def file_output(self):
        """Метод для экспорта данных в JSON-файл в директорию data """
        data_to_save = [vacancy.to_dict() for vacancy in self.data]
        # Определяем путь к файлу
        file_path = os.path.join(DATA_DIR, f"{self.filename}.json")  # Определяем полный путь к файлу
        with open(file_path, 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump(data_to_save, file, ensure_ascii=False)  # Записываем данные в формате JSON
