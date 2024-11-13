import subprocess
import datetime


def get_changed_python_files():
    """Get a list of changed Python files."""
    changed_files_result = subprocess.run(
        ["git", "diff", "--name-only", "--staged", "--diff-filter=d"],
        capture_output=True,
        text=True
    )
    if changed_files_result.returncode != 0:
        raise Exception("Failed to get changed files.")

    changed_files = changed_files_result.stdout.strip().split('\n')
    return [f for f in changed_files if f.endswith('.py')]


def run_linters(file_paths):
    """Run Pylint and Flake8 on the given Python files and log the results."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    log_filename = f"linter_log_{today}.txt"

    with open(log_filename, "w") as log_file:
        for file_path in file_paths:
            print(f"Running Pylint on {file_path}...", file=log_file)
            pylint_result = subprocess.run(["pylint", file_path],
                                           capture_output=True, text=True)
            log_file.write(f"Pylint Output for {file_path}:\n")
            log_file.write(pylint_result.stdout)
            if pylint_result.stderr:
                log_file.write(f"Pylint Errors for {file_path}:\n")
                log_file.write(pylint_result.stderr)
            log_file.write("\n")

            print(f"\nRunning Flake8 on {file_path}...", file=log_file)
            flake8_result = subprocess.run(["flake8", file_path],
                                           capture_output=True, text=True)
            log_file.write(f"Flake8 Output for {file_path}:\n")
            log_file.write(flake8_result.stdout)
            if flake8_result.stderr:
                log_file.write(f"Flake8 Errors for {file_path}:\n")
                log_file.write(flake8_result.stderr)
            log_file.write("\n")

        print("Linter checks completed.")


# Get the list of changed Python files
changed_python_files = get_changed_python_files()

# Run the linters on the changed Python files
run_linters(changed_python_files)