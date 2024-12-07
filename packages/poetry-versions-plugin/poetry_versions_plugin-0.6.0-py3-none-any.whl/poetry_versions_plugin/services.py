import os
from datetime import datetime

import git


def get_git_info(version=None):
    """
    获取当前Git仓库的相关信息，包括分支名称、最近提交的短SHA、提交数量、仓库是否有未提交的修改，以及当前时间。
    """
    repo = git.Repo(search_parent_directories=True)
    branch = repo.active_branch.name
    commit = repo.head.commit.hexsha[:7]
    commit_count = sum(1 for _ in repo.iter_commits(branch))
    is_dirty = repo.is_dirty()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "branch": branch,
        "commit": commit,
        "commit_count": commit_count,
        "is_dirty": is_dirty,
        "datetime": current_datetime,
        "version": version
    }


def update_readme(readme_path, info, dry_run=False):
    """
    更新README.md文件中的占位符，替换成Git信息。

    :param readme_path: README.md文件的路径
    :param info: 包含Git信息的字典
    :param dry_run: 是否为 dry-run 模式
    """
    # Open the README file and read its content
    with open(readme_path, 'r') as f:
        content = f.read()

    # Replace placeholders with actual info
    new_content = content.replace("<!-- BRANCH -->", info['branch'])
    new_content = new_content.replace("<!-- COMMIT -->", info['commit'])
    new_content = new_content.replace("<!-- COMMIT_COUNT -->", str(info['commit_count']))
    new_content = new_content.replace("<!-- IS_DIRTY -->", str(info['is_dirty']))
    new_content = new_content.replace("<!-- DATETIME -->", info['datetime'])

    if dry_run:
        # If dry_run is True, print what would be changed
        print(f"Would update {readme_path} with the following changes:")
        print(new_content)
    else:
        # If not a dry run, write changes to the file
        with open(readme_path, 'r+') as f:
            f.seek(0)
            f.write(new_content)
            f.truncate()


def update_py_file(py_path, info, dry_run=False):
    """
    创建或更新Python文件，将Git信息写入其中。

    :param py_path: Python文件的路径
    :param info: 包含Git信息的字典
    :param dry_run: 是否为 dry-run 模式
    """
    # 获取目录路径
    dir_path = os.path.dirname(py_path)

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(dir_path):
        if dry_run:
            print(f"Would create directory: {dir_path}")
        else:
            os.makedirs(dir_path, exist_ok=True)

    # Prepare the content to write
    content = "# THIS FILE IS GENERATED DURING PROJECT BUILD\n"
    content += "# See poetry poetry-versions-plugin for details\n\n"

    for key, value in info.items():
        # 根据值的类型格式化输出
        if isinstance(value, str):
            content += f"{key} = '{value}'\n"
        else:
            content += f"{key} = {value}\n"

    content += "\n"
    content += "full_version = f'{version}.{branch}+{commit_count}.{commit}'\n"
    content += "# END OF GENERATED CODE\n"

    if dry_run:
        print(f"Would write to file: {py_path}")
        print("File content would be:")
        print(content)
    else:
        with open(py_path, 'w') as f:
            f.write(content)


def update_pyproject(info, pyproject, io, dry_run=False):
    """
    更新pyproject.toml文件，将Git信息和版本号写入其中。
    :param info: 包含Git信息的字典
    :param pyproject: command.poetry.pyproject command 对象
    :param io:
    :param dry_run: 是否为 dry-run 模式
    :return: None
    """

    # 更新 pyproject.toml
    try:
        if 'versions' not in pyproject.data['tool']:
            pyproject.data['tool']['versions'] = {}

        versions = pyproject.data['tool']['versions']

        # Loop through the info dictionary and update each field
        for key, value in info.items():
            versions[key] = value
    except KeyError as ex:
        io.write_line(f'Error with parsing pyproject: {ex}')
        return

    # 保存更新
    if dry_run:
        io.write_line('dry-run mode, skip updating pyproject.toml')
    else:
        pyproject.save()


def commit_local_changes(repo_path, commit_message):
    """
    Commit local changes in the specified Git repository.

    :param repo_path: Path to the local Git repository.
    :param commit_message: Commit message to use.
    :raises: ValueError if there are no changes to commit.
    """

    # Ensure the repository path exists
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"The specified repository path does not exist: {repo_path}")

    # Initialize the repository
    repo = git.Repo(repo_path)

    # Check for uncommitted changes
    if not repo.is_dirty(untracked_files=True):
        raise ValueError("No changes to commit.")

    # Stage all changes
    repo.git.add(update=True)

    # Include new untracked files
    repo.git.add(A=True)

    # Commit the changes
    try:
        repo.index.commit(commit_message)
        print(f"Changes committed with message: '{commit_message}'")
    except Exception as e:
        print(f"Failed to commit changes: {e}")
        raise
