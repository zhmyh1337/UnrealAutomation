import subprocess
import os
from . import config
from . import ctx


def execute():
    original_directory = os.getcwd()

    git_dir = config['GitDir']
    git_branch = config['GitBranch']

    os.chdir(git_dir)

    if subprocess.run(['git', 'switch', git_branch]).returncode:
        return False

    if subprocess.run(['git', 'pull']).returncode:
        return False

    result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
    if result.returncode:
        return False
    commit_sha = result.stdout.strip()
    commit_sha_small = commit_sha[:6]
    ctx.last_commit = commit_sha_small

    os.chdir(original_directory)

    return True
