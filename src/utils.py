from src.api_service import HeadHunterAPI
from src.file_worker import JSONWorker
from src.vacancies import Vacancy

from config import DATA_DIR


def user_interaction():
    keyword = input('Введите поисковый запрос: ')
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ") # Пример: 100000 - 150000
    hh_api = HeadHunterAPI('data/vacancies.json')
    hh_api.load_vacancies(keyword)
    for vacancy in hh_api.vacancies:
        print(vacancy)

    vacancies_list = Vacancy.from_list(hh_api.vacancies)
    print(len(vacancies_list))
    for vacancy in vacancies_list:
        print(vacancy)
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # print(*ranged_vacancies[:top_n])
    print(*sorted_vacancies[:top_n])

def filter_vacancies(vacancies_list, filter_words):
    # Отфильтровывает вакансии, содержащие ключевые слова
    filtered_vacancies = [vacancy for vacancy in vacancies_list if
                          any(keyword in str(vacancy) for keyword in filter_words)]
    print(filtered_vacancies)
    return filtered_vacancies


def get_vacancies_by_salary(filtered_vacancies, salary_range):
    # Отфильтровывает вакансии по нижнему уровню зарплаты
    ranged_vacancies = [vac for vac in filtered_vacancies if float(vac.salary_from) >= float(salary_range)]
    return ranged_vacancies


def sort_vacancies(ranged_vacancies):
    """ Сортирует вакансии по нижнему уровню зарплаты в порядке убывания """
    sorted_vacancies = sorted(ranged_vacancies, key=lambda x: float(x.salary_from), reverse=True)
    return sorted_vacancies


def get_top_vacancies():
    pass


def print_vacancies():
    pass


# # Создание экземпляра класса для работы с API сайтов с вакансиями
# hh_api = HeadHunterAPI('data/vacancies.json')
#
# # Получение вакансий с hh.ru в формате JSON
# hh_vacancies = hh_api.load_vacancies("Python")
#
# # Преобразование набора данных из JSON в список объектов
# vacancies_list = Vacancy.from_list(hh_vacancies)

# Пример работы конструктора класса с одной вакансией
# vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.",
#                   "Требования: опыт работы от 3 лет...")

# Сохранение информации о вакансиях в файл
# json_saver = JSONWorker()
# json_saver.add_vacancy(vacancy)
# json_saver.delete_vacancy(vacancy)

if __name__ == "__main__":
    # hh_api = HeadHunterAPI('data/vacancies.json')

    # Получение вакансий с hh.ru в формате JSON
    # keyword = input("Введите ключевое слово для поиска вакансий: ")
    # hh_vacancies = hh_api.load_vacancies(keyword)
    #
    # # Преобразование набора данных из JSON в список объектов
    # vacancies_list = Vacancy.from_list(hh_vacancies)
    # for vacancy in vacancies_list:
    #     print(vacancy)

    user_interaction()