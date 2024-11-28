import subprocess
import re
from typing import Dict, List
import datetime
import os


def get_commit_messages(repo_path: str) -> List[str]:
    """
    Get all commit messages from a Git repository.

    Args:
        repo_path (str): Path to the Git repository.

    Returns:
        List[str]: List of commit messages.
    """
    try:
        # Run git log command to get commit messages
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while fetching commit messages: {e}")
        return []


def group_commits_by_tags(commit_messages: List[str]) -> Dict[str, List[str]]:
    """
    Group commit messages by tags based on keywords.

    Args:
        commit_messages (List[str]): List of commit messages.

    Returns:
        Dict[str, List[str]]: Dictionary with tags as keys and commit messages
         as values.
    """
    tags = {"Feature": ["feature", "add", "implement", "new"],
            "Bug Fix": ["fix", "bug", "error", "issue"],
            "Improvement": ["improve", "enhance", "refactor", "update"]}
    grouped_commits: Dict[str, List[str]] = {tag: [] for tag in tags}

    for message in commit_messages:
        for tag, keywords in tags.items():
            pattern = re.compile(
                r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b',
                re.IGNORECASE)

            # Check if any keyword matches
            if pattern.search(message):
                grouped_commits[tag].append(message)
                break

    return grouped_commits


def format_changelog(grouped_commits: Dict[str, List[str]]) -> str:
    """
    Format the grouped commit messages into a structured changelog section.

    Args:
        grouped_commits (Dict[str, List[str]]): Dictionary with tags as keys
        and commit messages as values.

    Returns:
        str: Formatted changelog section.
    """
    changelog = ""
    for tag, messages in grouped_commits.items():
        changelog += f"### {tag}\n"
        for message in messages:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
            changelog += f"- {timestamp} - {message}\n"
        changelog += "\n"

    return changelog


def append_changelog_to_readme(changelog: str, readme_path: str):
    """
    Append the changelog section to an existing ReadMe file.

    Args:
        changelog (str): Formatted changelog section.
        readme_path (str): Path to the ReadMe file.
    """
    # Check if the ReadMe file exists
    if not os.path.exists(readme_path):
        print(f"ReadMe file not found at {readme_path}")
        return

    # Read the existing ReadMe file
    with open(readme_path, "r") as file:
        readme_content = file.read()

    # Check if the Changelog section already exists
    changelog_heading = "## Changelog\n"

    if "## Changelog" in readme_content:
        # Locate the start of the existing changelog section
        changelog_start = readme_content.index(changelog_heading)

        # Locate the end of the changelog section (or end of the file if no
        # further sections exist)
        next_section_index = readme_content.find("## ",
                                                 changelog_start + len(
            changelog_heading))
        if next_section_index == -1:
            next_section_index = len(readme_content)

        # Replace the current changelog section with the updated content
        readme_content = (
                readme_content[:changelog_start]
                + changelog_heading
                + changelog.strip() + "\n"
                + readme_content[next_section_index:]
        )
    else:
        # Append the changelog section to the end of the file
        readme_content += f"\n\n{changelog_heading}{changelog.strip()}\n"

    # Write the updated ReadMe file
    with open(readme_path, "w") as file:
        file.write(readme_content)


def main():
    """
    Main function to extract commit messages, group them by tags, format the
     changelog, and append it to the ReadMe file.
    """
    repo_path = "./"  # Replace with the path to your
    # Git repository
    readme_path = "./README.md"  # Replace with the path to your
    # ReadMe file

    commit_messages = get_commit_messages(repo_path)
    if not commit_messages:
        print("No commit messages found.")
        return

    grouped_commits = group_commits_by_tags(commit_messages)
    changelog = format_changelog(grouped_commits)
    append_changelog_to_readme(changelog, readme_path)


if __name__ == "__main__":
    main()
