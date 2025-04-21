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

    # Метод для проверки наличия архива
    def archive_exists(self, archive_name):
        return os.path.exists(archive_name)

    def add_to_zip(self, zip_filename):
        """ Метод для добавления JSON-файла в ZIP-архив """
        # Если архив существует, создаем новый с номером
        query_counter = 1
        archive_name = zip_filename
        base_name = zip_filename.split('.')[0]  # Получаем базовое имя архива
        while self.archive_exists(archive_name):
            archive_name = f"{base_name}_{query_counter}.zip"
            query_counter += 1

        json_file_path = os.path.join(DATA_DIR, f"{self.filename}.json")
        zip_path = os.path.join(DATA_DIR, archive_name)

        if os.path.exists(json_file_path):
            with zipfile.ZipFile(zip_path, 'a') as zip_file:
                zip_file.write(json_file_path, arcname=f"{self.filename}.json")
                # print(f'Файл {self.filename}.json добавлен в архив {zip_path}.')
        else:
            print(f'Файл не найден: {json_file_path}')
