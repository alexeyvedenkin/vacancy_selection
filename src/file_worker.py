import json
import os
import zipfile
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

    def add_to_zip(self, zip_filename):
        """ Метод для добавления JSON-файла в ZIP-архив """
        json_file_path = os.path.join(DATA_DIR, f"{self.filename}.json")  # Путь к JSON-файлу

        # Проверяем, существует ли файл перед добавлением в ZIP
        json_file_path = os.path.join(DATA_DIR, f"{self.filename}.json")  # Path to JSON file
        zip_path = os.path.join(DATA_DIR, zip_filename)  # Use the same DATA_DIR for ZIP file

        # Check if the file exists before adding to ZIP
        if os.path.exists(json_file_path):
            with zipfile.ZipFile(zip_path, 'a') as zip_file:  # 'a' to append to existing archive
                zip_file.write(json_file_path, arcname=f"{self.filename}.json")  # Add file to archive
                # print(f'Файл {self.filename}.json добавлен в архив {zip_path}.')
        else:
            print(f'Файл не найден: {json_file_path}')
