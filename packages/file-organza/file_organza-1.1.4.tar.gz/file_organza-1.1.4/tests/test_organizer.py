import os
import pytest
from file_organza.organizer import FileOrganizer

@pytest.fixture
def setup_directory(tmp_path):
    test_dir = tmp_path / "test_folder"
    test_dir.mkdir()
    (test_dir / "file1.jpg").write_text("image")
    (test_dir / "file2.txt").write_text("document")
    return test_dir

def test_organize_by_type(setup_directory):
    organizer = FileOrganizer(setup_directory)
    organizer.organize_by_type()

    assert (setup_directory / 'jpg').exists()
    assert (setup_directory / 'txt').exists()
