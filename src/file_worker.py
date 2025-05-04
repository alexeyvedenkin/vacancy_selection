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
        data_to_save = [vacancy for vacancy in self.__data]
        # Определяем путь к файлу
        file_path = os.path.join(DATA_DIR, f"{self.__filename}.json")  # Определяем полный путь к файлу
        with open(file_path, 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump(data_to_save, file, ensure_ascii=False)  # Записываем данные в формате JSON

    @property
    def filename(self) -> str:
        """ Разрешает доступ к имени файла """
        return self.__filename

    # @staticmethod
    # def archive_exists(archive_name: str) -> bool:
    #     """ Метод для проверки наличия архива """
    #     full_path = os.path.join(DATA_DIR, archive_name)
    #     # print(f"Проверяем существование архива: {archive_name}")
    #     return os.path.exists(full_path)

    def add_to_zip(self, zip_filename: str) -> None:
        """ Метод для добавления JSON-файла в ZIP-архив """
        # Если архив существует, создаем новый с номером
        base_name = os.path.splitext(zip_filename)[0]  # Получаем базовое имя архива
        archive_name = zip_filename
        query_counter = 1

        # # Генерируем новое имя, если архив существует
        # while self.archive_exists(archive_name):
        #     archive_name = f"{base_name}_{query_counter}.zip"  # Генерируем новое имя
        #     query_counter += 1  # Увеличиваем счётчик

        json_file_path = os.path.join(DATA_DIR, f"{self.__filename}.json")
        zip_path = os.path.join(DATA_DIR, archive_name)  # Используем обновлённое имя архива

        if os.path.exists(json_file_path):
            with zipfile.ZipFile(zip_path, 'a') as zip_file:
                zip_file.write(json_file_path, arcname=f"{self.__filename}.json")
                print(f'Файл {self.filename}.json добавлен в архив {zip_path}.')  # Включите это для отладки
            os.remove(json_file_path)
        else:
            print(f'Файл не найден: {json_file_path}')
