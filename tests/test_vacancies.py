from src.vacancies import Vacancy


def test_vacancy_initialization() -> None:
    # Sample data to initialize a Vacancy
    data = {
        'id': '1',
        'name': 'Software Engineer',
        'area': {'name': 'New York'},
        'salary': {'from': 70000, 'to': 90000},
        'snippet': {
            'responsibility': '<highlighttext>Develop applications</highlighttext>',
            'requirement': '<highlighttext>Python skills</highlighttext>',
        },
        'alternate_url': 'https://example.com/vacancy/1'
    }

    vacancy = Vacancy(data)  # Create an instance of Vacancy

    assert vacancy.salary_from == 70000  # Test salary_from
    assert vacancy.salary_to == 90000  # Test salary_to
    # assert vacancy.__str__() == (
    #     "Software Engineer, зарплата от 70000, New York\n"
    #     "https://example.com/vacancy/1\n"
    #     "Описание вакансии: Develop applications\n"
    #     "Требования к вакансии: Python skills\n\n"
    # )  # Test string representation


def test_vacancy_no_salary() -> None:
    # Sample data without salary information
    data = {
        'id': '2',
        'name': 'Data Analyst',
        'area': {'name': 'San Francisco'},
        'snippet': {
            'responsibility': 'Analyze data',
            'requirement': 'SQL knowledge',
        },
        'alternate_url': 'https://example.com/vacancy/2'
    }

    vacancy = Vacancy(data)  # Create another instance
    assert vacancy.salary_from == 0  # Test default salary_from
    assert vacancy.salary_to == 0  # Test default salary_to


def test_description_with_valid_data():
    data = {
        'id': 1,
        'name': 'Software Engineer',
        'area': {'name': 'New York'},
        'salary': {'from': 100000, 'to': 150000},
        'snippet': {'responsibility': '<highlighttext>Develop software</highlighttext>'}
    }
    vacancy = Vacancy(data)
    assert vacancy.description == 'Develop software'


def test_description_with_empty_data():
    data = {}
    vacancy = Vacancy(data)
    assert vacancy.description == 'Описание не указано'


def test_to_dict():
    data = {
        'id': 1,
        'name': 'Software Engineer',
        'area': {'name': 'New York'},
        'salary': {'from': 70000, 'to': 100000},
        'snippet': {
            'responsibility': 'Develop software',
            'requirement': 'Python, Django'
        },
        'alternate_url': 'http://example.com'
    }

    vacancy = Vacancy(data)
    expected_dict = {
        'name': 'Software Engineer',
        'area': 'New York',
        'salary_from': 70000,
        'salary_to': 100000,
        'alternate.url': 'http://example.com',
        'requirement': 'Python, Django'
    }

    assert vacancy.to_dict() == expected_dict