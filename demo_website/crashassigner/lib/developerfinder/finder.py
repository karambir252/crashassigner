from typing import List, Dict, Tuple
from collections import defaultdict

from sentry.models.event import SentryEvent
from github.api import GithubAPI


def _sanitize_path(file_path: str):
    if file_path.startswith('/'):
        return file_path[1:]
    return file_path


def generate_all_path_suffixes(file_path: str):
    file_path = _sanitize_path(file_path)
    file_path_parts = file_path.split('/')
    return [
        '/'.join(file_path_parts[i:])
        for i in range(len(file_path_parts))
    ]


def file_path_to_path_suffixes(file_paths: Dict[str, object]) -> Dict[str, List[object]]:
    result = defaultdict(list)
    for file_path, metadata in file_paths.items():
        for path_suffix in generate_all_path_suffixes(file_path):
            result[path_suffix].append(metadata)
    return result


def find_possible_files(
        github_api: GithubAPI,
        file_full_path: str,
        repositories_meta: List[Tuple[str, str, str]]):
    possible_files = []
    for repo_owner, repo_name, repo_branch in repositories_meta:
        file_tree = github_api.files.get_file_tree(
            repo_owner, repo_name, repo_branch
        )

        path_suffixes_mapping = file_path_to_path_suffixes(
            file_tree.flatten_to_dict()
        )

        for path_suffix in generate_all_path_suffixes(file_full_path):
            if path_suffix in path_suffixes_mapping:
                for metadata in path_suffixes_mapping[path_suffix]:
                    possible_files.append(
                        (repo_owner, repo_name, repo_branch, metadata)
                    )
                return possible_files
    return []


def find_developer(
        github_api: GithubAPI,
        event: SentryEvent,
        possible_repositories_meta: List[Tuple[str, str, str]]):
    crashed_file_path = event.get_file_full_path()
    crashed_line_number = event.get_crashed_line_number()
    crashed_line_code = event.get_crashed_line_code()

    possible_files = find_possible_files(
        github_api, crashed_file_path, possible_repositories_meta
    )

    for repo_owner, repo_name, repo_branch, file_metadata in possible_files:
        file_path = file_metadata['full_path']
        file_content = github_api.files.get_file_content(
            repo_owner, repo_name, repo_branch, file_path
        )

        if crashed_line_number > file_content.get_number_of_lines():
            # This line number not exist in file
            continue
        elif file_content.get_line_code(crashed_line_number) != crashed_line_code:
            # This line is not crashed
            continue

        # This line is crashed line so find its developer and return
        file_blame = github_api.blames.get_blame(
            repo_owner, repo_name, repo_branch, file_path
        )

        developer_github_username = file_blame.get_line_author(
            crashed_line_number)

        return developer_github_username
