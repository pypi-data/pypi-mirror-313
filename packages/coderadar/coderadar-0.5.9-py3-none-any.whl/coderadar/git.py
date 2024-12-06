"""This module provides a function to get the most edited lines in a file in a git repository."""

import subprocess
from collections import Counter


def get_most_edited_lines(file_path, num_commits=50, num_lines=10):
    """
    In order to estimate code churn, bug density or code hotspots, indicating
    possibly too complex code as indicated by the number of edits.
    """
    # TODO: Not yet tested - needs practical testing
    # Get the list of commit hashes for the last num_commits commits that touched the file
    commit_hashes = subprocess.check_output(
        ['git', 'log', '-n', str(num_commits), '--pretty=format:%H', '--', file_path],
        universal_newlines=True
    ).splitlines()

    lines_counter = Counter()

    # For each commit, run git blame and count the number of times each line appears
    for commit in commit_hashes:
        blame_output = subprocess.check_output(
            ['git', 'blame', '-l', '-p', commit, '--', file_path],
            universal_newlines=True
        )
        # Parse the git blame output and count the lines
        for line in blame_output.splitlines():
            if line.startswith('\t'):  # This is a line of code
                lines_counter[line[1:]] += 1  # Exclude the leading tab character

    # Get the num_lines most common lines
    most_common_lines = lines_counter.most_common(num_lines)

    return most_common_lines
