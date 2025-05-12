import json
import os
import zipfile
from abc import ABC, abstractmethod

from config import DATA_DIR


class BaseWorker(ABC):
    """ Обязывает дочерние классы реализовать методы для добавления вакансий в файл """

    @abstractmethod
    def file_output(self) -> None:
        pass


class JSONWorker(BaseWorker):
    """ Реализует методы для добавления вакансий в JSON-файл """

    def __init__(self, data: list[dict], filename: str) -> None:
        """ Инициализатор класса JSONWorker """
        self.__data = data  # Сохраняем данные
        self.__filename = filename  # Сохраняем имя файла

    def file_output(self) -> None:
        """Метод для экспорта данных в JSON-файл в директорию data """

        # Проверяем, являются ли элементы словарями
        if all(isinstance(vacancy, dict) for vacancy in self.__data):
            data_to_save = self.__data  # Используем данные прямо, если это словари
        else:
            data_to_save = [vacancy.to_dict() for vacancy in self.__data]  # Для объектов с to_dict()

        # Определяем путь к файлу
        file_path = os.path.join(DATA_DIR, f"{self.__filename}.json")  # Определяем полный путь к файлу
        with open(file_path, 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump(data_to_save, file, ensure_ascii=False)  # Записываем данные в формате JSON

    @property
    def filename(self) -> str:
        """ Разрешает доступ к имени файла """
        return self.__filename

    def add_to_zip(self, zip_filename: str) -> None:
        """ Метод для добавления JSON-файла в ZIP-архив """

        json_file_path = os.path.join(DATA_DIR, f"{self.__filename}.json")
        zip_path = os.path.join(DATA_DIR, zip_filename)

        if os.path.exists(json_file_path):
            with zipfile.ZipFile(zip_path, 'a') as zip_file:
                zip_file.write(json_file_path, arcname=f"{self.__filename}.json")
            os.remove(json_file_path)
        else:
            print(f'Файл не найден: {json_file_path}')
