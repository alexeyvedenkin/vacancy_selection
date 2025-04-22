import json
import os

import pytest

from config import DATA_DIR
from src.file_worker import JSONWorker


@pytest.fixture
def json_worker():
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


def test_file_output(json_worker) -> None:
    """Test if the JSON file is created correctly."""
    json_worker.file_output()  # Call the method to output to file
    file_path = os.path.join(DATA_DIR, f"{json_worker.filename}.json")

    # Check if the file exists
    assert os.path.exists(file_path)

    # Check if the content of the file is correct
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]['title'] == 'Software Engineer'


def test_archive_exists(json_worker) -> None:
    """Test the method for checking if an archive exists."""
    # Assuming no archives exist at this point
    assert not json_worker.archive_exists('non_existent.zip')


def test_add_to_zip(json_worker) -> None:
    """Test adding a JSON file to a zip archive."""
    json_worker.file_output()  # Ensure the JSON file is created
    json_worker.add_to_zip('test_archive.zip')

    # Check if the zip file is created
    zip_path = os.path.join(DATA_DIR, 'test_archive.zip')
    assert os.path.exists(zip_path)

    # Clean up the created files after test
    os.remove(zip_path)
    os.remove(os.path.join(DATA_DIR, f"{json_worker.filename}.json"))
