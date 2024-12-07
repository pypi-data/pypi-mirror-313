# pylint: disable=too-many-arguments
"""Adapter for GitHub API."""
import functools
from typing import Dict, Generator, List, Optional, Tuple, Union

import requests

from opendapi.defs import HTTPMethod
from opendapi.utils import make_api_request


class GithubAdapter:
    """Functions to interact with the GitHub API."""

    def __init__(
        self,
        api_url: str,
        github_token: str,
        exception_cls: Optional[Exception] = None,
        per_page: int = 50,
    ) -> None:
        """Initialize the adapter."""
        self.api_url = api_url
        self.github_token = github_token
        self.exception_cls = exception_cls or Exception
        self.per_page = per_page

    def _check_and_raise(self, response: requests.Response, url: str):
        """Raise an exception."""
        if response.status_code > 400 and response.status_code != 422:
            raise self.exception_cls(
                "Something went wrong! "
                f"API failure with {response.status_code} for {url}. "
                f"Response: {response.text}"
            )

    def raw_make_api(
        self,
        url: str,
        json_payload: Dict,
        method: HTTPMethod,
        session: Optional[requests.Session] = None,
        raise_on_error: bool = True,
    ) -> Tuple[requests.Response, Optional[requests.Session]]:
        """Make API calls to github, returning entire response"""

        response, session = make_api_request(
            url,
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.github_token}",
                "User-Agent": "opendapi.org",
            },
            json_payload,
            method,
            req_session=session,
        )

        # Error on any status code other than 201 (created) or 422 (PR already exists)
        if (
            raise_on_error
            and response.status_code > 400
            and response.status_code != 422
        ):
            self._check_and_raise(response, url)

        return response, session

    def create_url(self, api_path: str) -> str:
        return f"{self.api_url}/{api_path}"

    def make_api(
        self, api_path: str, json_payload: Dict, method: HTTPMethod
    ) -> Union[Dict, List[Dict]]:
        """Make API calls to github, returning response json"""
        response, _ = self.raw_make_api(self.create_url(api_path), json_payload, method)
        return response.json()

    def make_api_with_pagination(
        self,
        url: str,
        json_payload: Optional[Dict] = None,
    ) -> Generator[Union[Dict, List[Dict]], None, None]:
        session = requests.Session()
        json_payload = {
            **(json_payload or {}),
            "per_page": self.per_page,
        }
        while url:
            response, _ = self.raw_make_api(
                url,
                json_payload,
                HTTPMethod.GET,
                session=session,
            )
            self._check_and_raise(response, url)
            yield response.json()
            url = (
                response.links["next"]["url"] if response.headers.get("link") else None
            )

    def add_pull_request_comment(self, pull_request_number: int, message: str):
        """Add a comment to the pull request."""
        self.make_api(
            f"issues/{pull_request_number}/comments",
            {"body": message},
            HTTPMethod.POST,
        )

    def get_pull_request_comments(
        self, pull_request_number: int
    ) -> Generator[Dict, None, None]:
        """Generator that yields comments of a pull request."""
        url = self.create_url(f"issues/{pull_request_number}/comments")
        for comments in self.make_api_with_pagination(url):
            for comment in comments:
                yield comment

    @functools.lru_cache()
    def get_pull_request_comments_cached(self, pull_request_number: int) -> List[Dict]:
        """Cached version of get_pull_request_comments"""
        return [
            comment for comment in self.get_pull_request_comments(pull_request_number)
        ]

    def get_pull_request_comment(self, comment_id: int) -> Dict:
        """Get a specific comment of a pull request."""

        return self.make_api(
            f"issues/comments/{comment_id}",
            {},
            HTTPMethod.GET,
        )

    @functools.lru_cache()
    def get_pull_request_comment_cached(self, comment_id: int) -> Dict:
        """Cached version of get_pull_request_comment"""
        return self.get_pull_request_comment(comment_id)

    def update_pull_request_comment(self, comment_id: int, message: str) -> None:
        """Update a comment on the pull request."""
        self.make_api(
            f"issues/comments/{comment_id}",
            {"body": message},
            HTTPMethod.POST,
        )

    def get_pull_requests(
        self, repo_owner: str, base: str, head: str, state: str
    ) -> List[Dict]:
        """Get pull requests from Github."""
        return self.make_api(
            "pulls",
            {
                "head": f"{repo_owner}:{head}",
                "base": base,
                "state": state,
            },
            HTTPMethod.GET,
        )

    @functools.lru_cache()
    def get_pull_requests_cached(
        self, repo_owner: str, base: str, head: str, state: str
    ) -> List[Dict]:
        """Cached version of get_pull_requests"""
        return self.get_pull_requests(repo_owner, base, head, state)

    def get_merged_pull_requests(
        self, repo_owner: str, base: str, head: str
    ) -> List[Dict]:
        """Get merged pull requests from Github."""
        pull_requests = self.make_api(
            "pulls",
            {
                "head": f"{repo_owner}:{head}",
                "base": base,
                "state": "closed",
                "sort": "updated",
            },
            HTTPMethod.GET,
        )
        return sorted(
            [pr for pr in pull_requests if pr.get("merged_at")],
            key=lambda pr: pr.get("merged_at"),
            reverse=True,
        )

    @functools.lru_cache()
    def get_merged_pull_requests_cached(
        self, repo_owner: str, base: str, head: str
    ) -> List[Dict]:
        """Cached version of get_merged_pull_requests"""
        return self.get_merged_pull_requests(repo_owner, base, head)

    def create_pull_request_if_not_exists(
        self, repo_owner: str, title: str, body: str, base: str, head: str
    ) -> int:
        """Create or update a pull request on Github."""
        # Check if a pull request already exists for this branch using list pull requests
        pull_requests = self.get_pull_requests(repo_owner, base, head, "open")

        if not pull_requests:
            # Create a new pull request if one doesn't exist
            response_json = self.make_api(
                "pulls",
                {"title": title, "body": body, "head": head, "base": base},
                HTTPMethod.POST,
            )
            pull_request_number = response_json.get("number")
        else:
            pull_request_number = pull_requests[0].get("number")

        return pull_request_number

    def delete_comment(self, comment_id: int) -> None:
        """Delete a comment."""
        self.raw_make_api(
            self.create_url(f"issues/comments/{comment_id}"),
            {},
            HTTPMethod.DELETE,
        )
