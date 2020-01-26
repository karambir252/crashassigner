from .client import GithubClient
from ..models.file import FileContent
from ..collections.tree import TreeNode, Tree

_ls_query = '''
query {{
  repository(owner: "{}", name: "{}") {{
    object(expression: "{}") {{
  ... on Tree {{
        entries {{
          name
          type
        }}
      }}
    }}
  }}
}}
'''


def _build_ls_query(owner, repository, expression):
    return _ls_query.format(owner, repository, expression)


_content_query = '''
query {{
  repository(owner: "{}", name: "{}") {{
    object(expression: "{}:{}") {{
      ... on Blob {{
        text
      }}
    }}
  }}
}}
'''


def _build_content_query(owner, repository, branch, file_path):
    return _content_query.format(owner, repository, branch, file_path)


class GithubFilesAPI:
    def __init__(self, client: GithubClient):
        self.client = client

    def get_files(self, owner, repository, branch, folder_path):
        expression = '{}:{}'.format(branch, folder_path)
        query = _build_ls_query(owner, repository, expression)
        result = self.client.get(query)
        return result['data']['repository']['object']['entries']

    def _load_files_in_node(self, root: TreeNode, owner, repository, branch, folder_path):
        files_infos = self.get_files(owner, repository, branch, folder_path)
        for file_info in files_infos:
            file_name = file_info['name']
            file_type = file_info['type']
            if folder_path:
                full_path = '{}/{}'.format(folder_path, file_name)
            else:
                full_path = file_name

            file_info['full_path'] = full_path

            node = TreeNode(file_name, file_info)
            root.add_child(file_name, node)
            if file_type == 'tree':
                self._load_files_in_node(
                    node, owner, repository, branch, full_path
                )

    def get_file_tree(self, owner, repository, branch) -> Tree:
        file_tree = Tree(repository)
        self._load_files_in_node(
            file_tree.root,
            owner,
            repository,
            branch,
            ''
        )
        return file_tree

    def get_file_content(self, owner, repository, branch, file_path) -> FileContent:
        query = _build_content_query(owner, repository, branch, file_path)
        data = self.client.get(query)
        return FileContent(data['data']['repository']['object'])
