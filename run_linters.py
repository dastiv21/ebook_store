import subprocess
import datetime


def run_linters():
    """Run Pylint and Flake8 on the entire project directory and log the results."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    log_filename = f"linter_log_{today}.txt"

    with open(log_filename, "w") as log_file:
        print("Running Pylint...", file=log_file)
        pylint_result = subprocess.run(["pylint", "**/*.py"], capture_output=True,
                                       text=True)
        log_file.write("Pylint Output:\n")
        log_file.write(pylint_result.stdout)
        if pylint_result.stderr:
            log_file.write("Pylint Errors:\n")
            log_file.write(pylint_result.stderr)
        log_file.write("\n")

        print("\nRunning Flake8...", file=log_file)
        flake8_result = subprocess.run(["flake8", "."], capture_output=True,
                                       text=True)
        log_file.write("Flake8 Output:\n")
        log_file.write(flake8_result.stdout)
        if flake8_result.stderr:
            log_file.write("Flake8 Errors:\n")
            log_file.write(flake8_result.stderr)
        log_file.write("\n")

        if pylint_result.returncode != 0 or flake8_result.returncode != 0:
            print("Linter checks found issues.")
        else:
            print("Linter checks completed successfully.")


# Call the function
run_linters()


