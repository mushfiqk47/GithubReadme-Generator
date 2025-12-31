import logging
import requests
from typing import Dict, Any, Optional
from src.core.config import config

logger = logging.getLogger(__name__)

class GitHubClient:
    """
    Client for interacting with the GitHub GraphQL API.
    Designed to fetch file trees and content in minimal round-trips.
    """
    API_URL = "https://api.github.com/graphql"

    def __init__(self):
        self.token = config.GITHUB_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def run_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes a GraphQL query."""
        payload = {"query": query, "variables": variables or {}}
        response = requests.post(self.API_URL, json=payload, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Query execution failed. Status: {response.status_code}. Response: {response.text}")
        
        data = response.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
            
        return data

    def get_repo_context(self, owner: str, name: str) -> Dict[str, Any]:
        """
        Fetches the repository file tree and contents of key files.
        Note: For very large repos, this might need pagination or depth limiting.
        """
        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            description
            homepageUrl
            object(expression: "HEAD:") {
              ... on Tree {
                entries {
                  name
                  type
                  object {
                    ... on Blob {
                      byteSize
                      text
                      isBinary
                    }
                    ... on Tree {
                      entries {
                        name
                        type
                        object {
                          ... on Blob {
                            byteSize
                            text
                            isBinary
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """
        # Note: The query above is simplified. A full recursive fetch often requires 
        # a more complex strategy or multiple IDs if the tree is deep.
        # For this v1 implementation, we are fetching the top 2 levels to catch likely 
        # config files and entry points. Deeply nested code might require the 'Map-Reduce' approach later.
        
        variables = {"owner": owner, "name": name}
        result = self.run_query(query, variables)
        return result["data"]["repository"]
