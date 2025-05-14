import pytest

from src.vacancies import Vacancy


@pytest.fixture
def vacancy1():
    data = {
        'id': '1',
        'name': 'Software Engineer',
        'area': {'name': 'New York'},
        'salary': {'from': 50000, 'to': 90000},
        'snippet': {
            'responsibility': '<highlighttext>Develop applications</highlighttext>',
            'requirement': '<highlighttext>Python skills</highlighttext>',
        },
        'alternate_url': 'https://example.com/vacancy/1'
    }
    return Vacancy(data)


@pytest.fixture
def vacancy2():
    data = {
        'id': '2',
        'name': 'Software Engineer',
        'area': {'name': 'New York'},
        'salary': {'from': 30000, 'to': 80000},
        'snippet': {
            'responsibility': '<highlighttext>Develop applications</highlighttext>',
            'requirement': '<highlighttext>Python skills</highlighttext>',
        },
        'alternate_url': 'https://example.com/vacancy/1'
    }
    return Vacancy(data)


@pytest.fixture
def vacancy3():
    data = {
        'id': '3',
        'name': 'Software Engineer',
        'area': {'name': 'New York'},
        'salary': {'from': 70000, 'to': 70000},
        'snippet': {
            'responsibility': '<highlighttext>Develop applications</highlighttext>',
            'requirement': '<highlighttext>Python skills</highlighttext>',
        },
        'alternate_url': 'https://example.com/vacancy/1'
    }
    return Vacancy(data)
