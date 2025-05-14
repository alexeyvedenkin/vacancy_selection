from typing import Any
from unittest.mock import patch

from src.api_service import HeadHunterAPI


# class TestHeadHunterAPI:
#
@patch('requests.get')
def test_load_vacancies(mock_get: Any) -> None:
    mock_get.return_value.json.return_value = {
        'items': [
            {'name': 'Python Developer', 'id': 1},
            {'name': 'Java Developer', 'id': 2}
        ]
    }
    api = HeadHunterAPI('dummy_file_path')

    vacancies = api.load_vacancies('Python')

    assert len(vacancies) == 20
    assert vacancies[0]['name'] == 'Python Developer'
