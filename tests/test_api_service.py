from typing import Any
from unittest.mock import patch

from src.api_service import HeadHunterAPI


class TestHeadHunterAPI:

    @patch('requests.get')
    def test_load_vacancies(self, mock_get: Any) -> None:
        # Arrange: Set up the mock response
        mock_get.return_value.json.return_value = {
            'items': [
                {'name': 'Python Developer', 'id': 1},
                {'name': 'Java Developer', 'id': 2}
            ]
        }
        api = HeadHunterAPI('dummy_file_path')  # You can provide any dummy file path as needed

        # Act: Call the method you want to test
        vacancies = api.load_vacancies('Python')

        # Assert: Check if we got the expected result
        assert len(vacancies) == 1  # We expect one vacancy that matched
        assert vacancies[0]['name'] == 'Python Developer'  # Check if the right name is returned
