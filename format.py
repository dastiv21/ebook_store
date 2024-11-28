import subprocess
import re
from collections import defaultdict

def extract_commit_messages(repo_path):
    try:
        # Get the list of tags
        tags = subprocess.check_output(['git', 'tag'], cwd=repo_path).decode().splitlines()

        # Initialize a dictionary to store grouped commits
        grouped_commits = defaultdict(list)

        # Iterate over each tag
        for tag in tags:
            # Get the commit messages for the tag
            commit_messages = subprocess.check_output(['git', 'log', '--pretty=format:%s', tag], cwd=repo_path).decode().splitlines()

            # Iterate over each commit message
            for message in commit_messages:
                # Check if the commit message contains any keywords
                if re.search(r'(feature|feat|new|add)', message, re.IGNORECASE):
                    grouped_commits['Feature'].append(message)
                elif re.search(r'(bug|fix|patch)', message, re.IGNORECASE):
                    grouped_commits['Bug Fix'].append(message)
                elif re.search(r'(improvement|enhancement|refactor)', message, re.IGNORECASE):
                    grouped_commits['Improvement'].append(message)

        return grouped_commits
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {}

if __name__ == "__main__":
    repo_path = "path/to/your/repository"  # Replace with the path to your Git repository
    grouped_commits = extract_commit_messages(repo_path)
    print(grouped_commits)