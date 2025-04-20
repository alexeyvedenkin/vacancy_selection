from src.api_service import HeadHunterAPI
from src.file_worker import JSONWorker
from src.vacancies import Vacancy
import re
from config import DATA_DIR


def user_interaction():
    print('Вас приветствует программа подбора вакансий с сайта hh.ru\n')
    query = input('Введите поисковый запрос: \n').strip()
    keyword = keep_cyrillic_letters(query)
    if keyword != query:
        print(f'Запрос "{query}" преобразован в "{keyword}"')
    print('Производится подбор вакансий, ожидайте\n')
    hh_api = HeadHunterAPI('data/vacancies.json')
    hh_api.load_vacancies(keyword)
    # for vacancy in hh_api.vacancies:
    #     print(vacancy)
    vacancies_list = Vacancy.from_list(hh_api.vacancies)
    exporter = JSONWorker(vacancies_list, 'vacancies')
    exporter.file_output()
    print(f'По вашему запросу подобрано {len(vacancies_list)} вакансий. '
          f'Результат выгружен в файл data/{exporter.filename}.json\n')
    user_choice = input('Вывести список вакансий? да/нет \n')
    if user_choice.lower() in ['д', 'да', 'y', 'yes']:
        print(*vacancies_list)
    print()
    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): \n").split()
    work_filter_words = []
    for word in filter_words:
        work_word = keep_cyrillic_letters(word)
        if not work_word:
            print(f'Запрос "{word}" не может быть обработан')
        elif work_word != word:
            print(f'Запрос "{word}" преобразован в "{work_word}"')
        work_filter_words.append(work_word)
    filtered_vacancies = filter_vacancies(vacancies_list, work_filter_words)
    exporter = JSONWorker(vacancies_list, 'filtered_vacancies')
    exporter.file_output()
    print(f'Отобрано {len(filtered_vacancies)} вакансий. '
          f'Результат выгружен в файл data/{exporter.filename}.json\n')
    user_choice = input('Вывести отфильтрованный список? да/нет \n')
    if user_choice.lower() in ['д', 'да', 'y', 'yes']:
        print(*filtered_vacancies)
    print()
    salary_range = input("Введите минимальный уровень зарплаты: \n")
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    exporter = JSONWorker(vacancies_list, 'ranged_vacancies')
    exporter.file_output()
    print(f'На текущий момент в списке {len(ranged_vacancies)} вакансий. '
          f'Результат выгружен в файл data/{exporter.filename}.json\n')
    user_choice = input('Вывести полученный список? да/нет \n')
    if user_choice.lower() in ['д', 'да', 'y', 'yes']:
        print(*ranged_vacancies)
    print()
    top_n = int(input("Введите количество вакансий для вывода в топ-лист: \n"))
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    print(*sorted_vacancies[:top_n])
    # print(len(vacancies_list))
    # for vacancy in vacancies_list:
    #     print(vacancy)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # print(*ranged_vacancies[:top_n])
    # print(*sorted_vacancies[:top_n])

def filter_vacancies(vacancies_list, filter_words):
    # Отфильтровывает вакансии, содержащие ключевые слова
    filtered_vacancies = [vacancy for vacancy in vacancies_list if
                          any(keyword in str(vacancy) for keyword in filter_words)]
    # print(filtered_vacancies)
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


def keep_cyrillic_letters(input_string):
    # Исключает из запроса символы, не являющиеся буквами кириллицы
    cleaned_string = ''.join(re.findall(r'[А-Яа-яЁё]', input_string))
    return cleaned_string


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