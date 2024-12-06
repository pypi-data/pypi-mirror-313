import os
import subprocess
import pytest

@pytest.fixture
def test_directory(tmp_path):
    # Create a temporary directory for testing
    test_dir = tmp_path / "test_folder"
    test_dir.mkdir()

    # Add some sample files
    (test_dir / "file1.txt").write_text("Sample text file.")
    (test_dir / "file2.jpg").write_text("Sample image file.")
    return str(test_dir)

def test_cli_by_type(test_directory):
    cli_path = os.path.abspath("file_organza/cli.py")  # Absolute path to cli.py
    result = subprocess.run(['python', cli_path, test_directory, '--by-type'], capture_output=True)

    # Debugging info in case of failure
    print("stdout:", result.stdout.decode())
    print("stderr:", result.stderr.decode())

    assert result.returncode == 0
