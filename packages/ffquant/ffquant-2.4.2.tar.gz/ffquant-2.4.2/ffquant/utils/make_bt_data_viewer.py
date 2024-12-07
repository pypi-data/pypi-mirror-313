import subprocess
from ffquant.utils.Logger import stdout_log
import traceback
import os

def make_executable_file(py_file_path, version="1.0.0"):
    exec_file_name = f"backtest_data_viewer_{version}"
    command = [
        'pyinstaller',
        '--onefile',
        '--name', exec_file_name,
        f"{py_file_path}"
    ]
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        stdout_log(f"Failed to make executable file, error: {e}, traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    version = "1.0.0"
    py_file_path = f"{os.path.dirname(__file__)}/standalone_dash.py"
    make_executable_file(py_file_path=py_file_path, version=version)