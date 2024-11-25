#!/usr/bin/python3
import datetime


def run_linters():
    """
    Run Pylint and Flake8 on the entire project directory and log the results.
    Return a non-zero exit code if any linter detects issues.
    """
    # Generate a timestamped log file name to store linter output
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"linter_log_{timestamp}.txt"

    print("Trying to test pre-commit")
print("Linter")
run_linters()
