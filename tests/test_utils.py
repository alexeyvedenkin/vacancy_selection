from src.utils import filter_vacancies, get_vacancies_by_salary, keep_letters, keep_right_query, sort_vacancies
from src.vacancies import Vacancy


def test_placeholder():
    assert True


def test_keep_letters():
    assert keep_letters("Привет, World123!") == "ПриветWorld"
    assert keep_letters("!@#") == ""
    assert keep_letters("Hello, мир!") == "Hellомир"


def test_keep_right_query():
    assert keep_right_query("12345 Hello 67890") == "12345Hello67890"
    assert keep_right_query("    Hello  World    ") == "HelloWorld"
    assert keep_right_query("Тест   1234") == "Тест1234"


def test_filter_vacancies():
    vacancies = ["Software Engineer", "Data Scientist", "Product Manager"]
    assert filter_vacancies(vacancies, ["Engineer"]) == ["Software Engineer"]
    assert filter_vacancies(vacancies, ["Manager"]) == ["Product Manager"]
    assert filter_vacancies(vacancies, ["Developer"]) == []


def test_get_vacancies_by_salary():
    # class Vacancy:
    #     def __init__(self, salary_from):
    #         self.salary_from = salary_from

    vacancies = [Vacancy(50000), Vacancy(30000), Vacancy(70000)]
    result = get_vacancies_by_salary(vacancies, 40000)
    assert len(result) == 2  # 2 vacancies meet the salary criteria
    assert result[0].salary_from == 50000


def test_sort_vacancies():
    # class Vacancy:
    #     def __init__(self, salary_from):
    #         self.salary_from = salary_from

    vacancies = [Vacancy(30000), Vacancy(50000), Vacancy(10000)]
    sorted_vacancies = sort_vacancies(vacancies)
    assert sorted_vacancies[0].salary_from == 50000
