import subprocess

def test_cli_by_type():
    result = subprocess.run(['python', 'file_organza/cli.py', 'test_folder', '--by-type'], capture_output=True)
    assert result.returncode == 0
