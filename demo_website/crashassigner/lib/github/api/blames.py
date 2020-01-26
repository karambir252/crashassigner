from .client import GithubClient
from ..models.blame import GithubBlame

_blame_query = '''
query {{
  repository(owner: "{}", name: "{}") {{
    ref(qualifiedName: "{}") {{
      target {{
        ... on Commit {{
          blame(path: "{}") {{
            ranges {{
              startingLine
              endingLine
              age
              commit {{
                author {{
                  name
                  email
                  user {{
                    login
                  }}
                }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
'''

def _build_blame_query(owner, repository, branch, file_path):
    return _blame_query.format(owner, repository, branch, file_path)

class GithubBlamesAPI:
    def __init__(self, client: GithubClient):
        self.client = client
    
    def get_blame(self, owner, repository, branch, file_path):
        query = _build_blame_query(owner, repository, branch, file_path)
        result = self.client.get(query)
        return GithubBlame(result['data']['repository']['ref']['target']['blame'])
