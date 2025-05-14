import json
import os

import pytest

from config import DATA_DIR
from src.file_worker import JSONWorker


@pytest.fixture
def json_worker() -> JSONWorker:
    """Fixture to create a JSONWorker instance for testing."""
    # Create a mock data dictionary
    mock_data = [{
        'title': 'Software Engineer',
        'company': 'Example Corp',
        'location': 'Remote'
    }]

    # Create a JSONWorker instance
    filename = 'test_vacancies'
    worker = JSONWorker(mock_data, filename)
    return worker


def test_file_output(vacancy1) -> None:
    """Test if the JSON file is created correctly."""
    json_worker = JSONWorker(data=[vacancy1], filename='test_vacancy')  # Use 'test_vacancy' as a filename
    json_worker.file_output()
    file_path = os.path.join(DATA_DIR, f"{json_worker.filename}.json")

    assert os.path.exists(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]['name'] == 'Software Engineer'


def test_add_to_zip(json_worker: JSONWorker) -> None:
    """ Проверяет добавление JSON-файла в zip-архив """
    json_worker.file_output()
    json_worker.add_to_zip('test_archive.zip')

    zip_path = os.path.join(DATA_DIR, 'test_archive.zip')
    assert os.path.exists(zip_path)

    os.remove(zip_path)
