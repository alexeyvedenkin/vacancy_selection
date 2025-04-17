from src.api_service import HeadHunterAPI
from src.file_worker import JSONWorker
from src.vacancies import Vacancy


def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print(ranged_vacancies[:top_n])


def filter_vacancies(vacancies_list, filter_words):
    # Отфильтровывает вакансии, содержащие ключевые слова
    filtered_vacancies = [vacancy for vacancy in vacancies_list if
                          any(keyword in vacancy for keyword in filter_words)]
    return filtered_vacancies


def get_vacancies_by_salary(filtered_vacancies, salary_range):
    # Отфильтровывает вакансии по нижнему уровню зарплаты
    ranged_vacancies = [vac for vac in filtered_vacancies if vacancy.salary_from >= salary_range]
    return ranged_vacancies


def sort_vacancies(ranged_vacancies):
    """ Сортирует вакансии по нижнему уровню зарплаты в порядке убывания """
    sorted_vacancies = sorted(vacancies_list, reverse=True)
    return sorted_vacancies

def get_top_vacancies():
    pass


def print_vacancies():
    pass


# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI()

# Получение вакансий с hh.ru в формате JSON
hh_vacancies = hh_api.get_vacancies("Python")

# Преобразование набора данных из JSON в список объектов
vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

# Пример работы контструктора класса с одной вакансией
vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.",
                  "Требования: опыт работы от 3 лет...")

# Сохранение информации о вакансиях в файл
json_saver = JSONWorker()
json_saver.add_vacancy(vacancy)
json_saver.delete_vacancy(vacancy)

if __name__ == "__main__":
    user_interaction()