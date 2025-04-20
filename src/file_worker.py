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
        if os.path.exists(json_file_path):
            with zipfile.ZipFile(zip_filename, 'a') as zip_file:  # 'a' для добавления в существующий архив
                zip_file.write(json_file_path, arcname=f"{self.filename}.json")  # Добавляем файл в архив
                print(f'Файл {json_file_path} добавлен в архив {zip_filename}.')
        else:
            print(f'Файл не найден: {json_file_path}')
