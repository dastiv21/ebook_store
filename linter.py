import subprocess
import datetime
import sys


def run_linters():
    """
    Run Pylint and Flake8 on the entire project directory and log the results.
    Return a non-zero exit code if any linter detects issues.
    """
    # Generate a timestamped log file name to store linter output
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"linter_log_{timestamp}.txt"

    # Initialize a flag to track linter issues
    issues_detected = False

    # Open the log file and write both Pylint and Flake8 results to it
    with open(log_filename, "w") as log_file:
        print("Running Pylint...", file=log_file)

        # Run Pylint on the current directory and capture its output
        pylint_result = subprocess.run(["pylint", "."],
                                       capture_output=True, text=True)
        log_file.write("Pylint Output:\n")
        log_file.write(pylint_result.stdout)
        if pylint_result.stderr:
            log_file.write("Pylint Errors:\n")
            log_file.write(pylint_result.stderr)
        log_file.write("\n")

        # Update flag if Pylint finds issues
        if pylint_result.returncode != 0:
            issues_detected = True

        print("\nRunning Flake8...", file=log_file)

        # Run Flake8 on the current directory and capture its output
        flake8_result = subprocess.run(["flake8", "."],
                                       capture_output=True, text=True)
        log_file.write("Flake8 Output:\n")
        log_file.write(flake8_result.stdout)
        if flake8_result.stderr:
            log_file.write("Flake8 Errors:\n")
            log_file.write(flake8_result.stderr)
        log_file.write("\n")

        # Update flag if Flake8 finds issues
        if flake8_result.returncode != 0:
            issues_detected = True

    # Print results summary
    if issues_detected:
        print("Linter checks found issues. See the log file for details.")
        return 1  # Return a non-zero value to indicate failure
    else:
        print("Linter checks completed successfully.")
        return 0  # Return zero to indicate success


if __name__ == "__main__":
    # Exit with the appropriate code based on linter results
    sys.exit(run_linters())
