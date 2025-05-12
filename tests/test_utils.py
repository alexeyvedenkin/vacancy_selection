from src.utils import filter_vacancies, get_vacancies_by_salary, keep_letters, keep_right_query, sort_vacancies


def test_placeholder() -> None:
    assert True


def test_keep_letters() -> None:
    assert keep_letters("Привет, Мир123!") == "Привет Мир123"
    assert keep_letters("!@#") == ""
    assert keep_letters("Hello,- мир!") == "Hello- мир"


def test_keep_right_query() -> None:
    assert keep_right_query("12345 Hello 67890") == "12345Hello67890"
    assert keep_right_query("    Hello  World    ") == "HelloWorld"
    assert keep_right_query("Тест   1234") == "Тест1234"


def test_filter_vacancies() -> None:
    vacancies = ["Software Engineer", "Data Scientist", "Product Manager"]
    assert filter_vacancies(vacancies, ["Engineer"]) == ["Software Engineer"]
    assert filter_vacancies(vacancies, ["Manager"]) == ["Product Manager"]
    assert filter_vacancies(vacancies, ["Developer"]) == []


def test_get_vacancies_by_salary(vacancy1, vacancy2, vacancy3) -> None:
    vacancies = [vacancy1, vacancy2, vacancy3]
    result = get_vacancies_by_salary(vacancies, 40000)
    assert len(result) == 2  # 2 vacancies meet the salary criteria
    assert result[0].salary_from == 50000


def test_sort_vacancies(vacancy1, vacancy2, vacancy3) -> None:
    vacancies = [vacancy1, vacancy2, vacancy3]
    sorted_vacancies = sort_vacancies(vacancies)
    assert sorted_vacancies[0].salary_from == 70000
