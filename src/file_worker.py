from abc import ABC, abstractmethod


class BaseWorker(ABC):
    """ Обязывает дочерние классы реализовать методы для добавления вакансий в файл """

    def file_output(self):
        pass


class JSONWorker(BaseWorker):
    """ Реализует методы для добавления вакансий в JSON-файл """

    def file_output(self):
        pass
