import subprocess
import datetime
import os
import sys


def run_linters(file_paths):
    """Run Pylint and Flake8 on the provided file paths and log the results."""
    today = datetime.date.today()
    log_directory = os.path.join("linter_logs", str(today.year),
                                 str(today.month).zfill(2),
                                 str(today.day).zfill(2))
    os.makedirs(log_directory, exist_ok=True)
    log_filename = f"linter_log_{today.strftime('%Y-%m-%d')}.txt"
    log_path = os.path.join(log_directory, log_filename)

    error_files = []
    with open(log_path, "w") as log_file:
        for file_path in file_paths:
            print(f"Analyzing {file_path} with Pylint...", file=log_file)
            pylint_result = subprocess.run(["pylint", file_path],
                                           capture_output=True, text=True)
            log_file.write(f"Pylint Output for {file_path}:\n")
            log_file.write(pylint_result.stdout)
            if pylint_result.stderr:
                log_file.write(f"Pylint Errors for {file_path}:\n")
                log_file.write(pylint_result.stderr)
                error_files.append(file_path)
            log_file.write("\n")

            print(f"Analyzing {file_path} with Flake8...", file=log_file)
            flake8_result = subprocess.run(["flake8", file_path],
                                           capture_output=True, text=True)
            log_file.write(f"Flake8 Output for {file_path}:\n")
            log_file.write(flake8_result.stdout)
            if flake8_result.stderr:
                log_file.write(f"Flake8 Errors for {file_path}:\n")
                log_file.write(flake8_result.stderr)
                error_files.append(file_path)
            log_file.write("\n")

    if error_files:
        print("\nLinting errors found in the following files:")
        for file in error_files:
            print(f" - {file}")
        sys.exit(1)


# Get the list of changed files that are staged for commit
changed_files_result = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=d"],
    capture_output=True, text=True)
changed_files = changed_files_result.stdout.splitlines()

# Filter to include only Python files
python_files = [f for f in changed_files if f.endswith('.py')]

# Call the function with the list of Python files
run_linters(python_files)