import subprocess
from datetime import datetime


def run_linters():
    """Run Pylint and Flake8 on the entire project directory, logging output to a timestamped file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"linter_log_{timestamp}.txt"
    print("Running Linters")

    with open(log_filename, 'w') as log_file:
        print("Running Pylint...")
        pylint_result = subprocess.run(["pylint", "**/*.py"], capture_output=True,
                                       text=True)
        log_file.write("Pylint Output:\n")
        log_file.write(pylint_result.stdout)
        if pylint_result.stderr:
            log_file.write("Pylint Errors:\n")
            log_file.write(pylint_result.stderr)

        print("\nRunning Flake8...")
        flake8_result = subprocess.run(["flake8", "."], capture_output=True,
                                       text=True)
        log_file.write("\nFlake8 Output:\n")
        log_file.write(flake8_result.stdout)
        if flake8_result.stderr:
            log_file.write("\nFlake8 Errors:\n")
            log_file.write(flake8_result.stderr)

        print("\nLinter checks completed.")


# Call the function
run_linters()