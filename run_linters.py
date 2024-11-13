import subprocess
import datetime
import os
import sys

def run_linters(file_paths):
    """Run Pylint and Flake8 on given Python files and log the results."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    log_filename = f"linter_log_{today}.txt"

    with open(log_filename, "w") as log_file:
        for file_path in file_paths:
            if os.path.isfile(file_path) and file_path.endswith('.py'):
                print(f"Running Pylint on {file_path}...", file=log_file)
                pylint_result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
                log_file.write(f"Pylint Output for {file_path}:\n")
                log_file.write(pylint_result.stdout)
                if pylint_result.stderr:
                    log_file.write(f"Pylint Errors for {file_path}:\n")
                    log_file.write(pylint_result.stderr)
                log_file.write("\n")

                print(f"\nRunning Flake8 on {file_path}...", file=log_file)
                flake8_result = subprocess.run(["flake8", file_path], capture_output=True, text=True)
                log_file.write(f"Flake8 Output for {file_path}:\n")
                log_file.write(flake8_result.stdout)
                if flake8_result.stderr:
                    log_file.write(f"Flake8 Errors for {file_path}:\n")
                    log_file.write(flake8_result.stderr)
                log_file.write("\n")

            else:
                print(f"Skipping {file_path}: not a Python file or does not exist.", file=log_file)

        if any("pylint" in result.stdout or "pylint" in result.stderr for result in [pylint_result, flake8_result]):
            print("Linter checks found issues.")
        else:
            print("Linter checks completed successfully.")

# Call the function
if __name__ == "__main__":
    # Get the list of committed Python files
    committed_files = subprocess.run(["git", "diff", "--staged", "--name-only", "--", "*.py"], capture_output=True, text=True)
    file_paths = committed_files.stdout.strip().split('\n')
    run_linters(file_paths)