import subprocess
from datetime import datetime

def run_linters():
    """Run Pylint and Flake8 on the entire project directory and log results."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"linter_log_{timestamp}.txt"
    with open(log_filename, 'w') as log_file:
        print(f"Running Pylint... (Log: {log_filename})", file=log_file)
        pylint_result = subprocess.run(["pylint", "."], capture_output=True, text=True)
        print(pylint_result.stdout, file=log_file)
        if pylint_result.stderr:
            print(pylint_result.stderr, file=log_file)

        print("\nRunning Flake8... (Log: {log_filename})", file=log_file)
        flake8_result = subprocess.run(["flake8", "."], capture_output=True, text=True)
        print(flake8_result.stdout, file=log_file)
        if flake8_result.stderr:
            print(flake8_result.stderr, file=log_file)

        print("\nLinter checks completed.", file=log_file)

# Call the function
run_linters()