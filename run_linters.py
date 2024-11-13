import subprocess
import datetime


def run_linters_on_files(file_paths):
    """Run Pylint and Flake8 on a list of specified Python files."""
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

            if pylint_result.returncode != 0 or flake8_result.returncode != 0:
                print(f"Linter checks found issues in {file_path}.")
            else:
                print(f"Linter checks completed successfully for {file_path}.")


def get_staged_python_files():
    """Get a list of staged Python files to be committed."""
    try:
        output = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=d", "|",
             "grep", "\\.py$"],
            capture_output=True, text=True, shell=True)
        if output.returncode != 0:
            raise Exception(output.stderr)
        # Remove trailing newlines and split to get a list of file paths
        return output.stdout.strip().split("\n")
    except Exception as e:
        print(f"Error getting staged Python files: {e}")
        return []


# Get the list of staged Python files
staged_files = get_staged_python_files()

# Call the function on the staged Python files
if staged_files:
    run_linters_on_files(staged_files)
else:
    print("No staged Python files to lint.")