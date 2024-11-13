import subprocess
from datetime import datetime

def run_linters():
    """Run Pylint and Flake8 on the entire project directory and log the results."""
    print("Running Pylint...")
    pylint_result = subprocess.run(["pylint", "."], capture_output=True, text=True)
    print("Pylint Output:\n", pylint_result.stdout)
    if pylint_result.stderr:
        print("Pylint Errors:\n", pylint_result.stderr)

    print("\nRunning Flake8...")
    flake8_result = subprocess.run(["flake8", "."], capture_output=True, text=True)
    print("Flake8 Output:\n", flake8_result.stdout)
    if flake8_result.stderr:
        print("Flake8 Errors:\n", flake8_result.stderr)

    print("\nLinter checks completed.")

    # Log results to a file
    TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
    FILENAME = f"linter_log_{TIMESTAMP}.txt"
    with open(FILENAME, 'w') as log_file:
        log_file.write("Pylint Output:\n" + pylint_result.stdout)
        if pylint_result.stderr:
            log_file.write("Pylint Errors:\n" + pylint_result.stderr)
        log_file.write("\nFlake8 Output:\n" + flake8_result.stdout)
        if flake8_result.stderr:
            log_file.write("Flake8 Errors:\n" + flake8_result.stderr)
    print(f"Analysis result saved in {FILENAME}.")

# Call the function
run_linters()