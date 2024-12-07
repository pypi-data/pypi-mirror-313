import json
from typing import TYPE_CHECKING, Any, Dict

import requests

from wallaroo.utils import _unwrap

from .object import UserLimitError
from .version import _user_agent

if TYPE_CHECKING:
    # Imports that happen below in methods to fix circular import dependency
    # issues need to also be specified here to satisfy mypy type checking.
    from .client import Client


class User:
    """A platform User."""

    def __init__(self, client, data: Dict[str, Any]) -> None:
        self.client = client
        self._id = data["id"]
        self._email = data["email"] if "email" in data else "admin@keycloak"
        self._username = data["username"]
        self._enabled = data["enabled"]
        self._createdTimeastamp = data["createdTimestamp"]

    def __repr__(self):
        return f"""User({{"id": "{self.id()}", "email": "{self.email()}", "username": "{self.username()}", "enabled": "{self.enabled()})"""

    def id(self) -> str:
        return self._id

    def email(self) -> str:
        return self._email

    def username(self) -> str:
        return self._username

    def enabled(self) -> bool:
        return self._enabled

    @staticmethod
    def list_users(
        auth,
        api_endpoint: str = "http://api-lb:8080",
    ):
        headers = {
            "authorization": auth._bearer_token_str(),
            "user-agent": _user_agent,
        }
        users = requests.post(
            f"{api_endpoint}/v1/api/users/query", data="{}", headers=headers
        )
        if users.status_code > 299:
            raise Exception("Failed to list exiting users.")
        return users.json()["users"].values()

    @staticmethod
    def get_email_by_id(
        client: "Client",
        id: str,
    ):
        from wallaroo.wallaroo_ml_ops_api_client.api.user.users_query import (
            UsersQueryBody,
            sync_detailed,
        )
        from wallaroo.wallaroo_ml_ops_api_client.models.users_query_response_200 import (
            UsersQueryResponse200,
        )

        r = sync_detailed(client=client.mlops(), body=UsersQueryBody([id]))

        if isinstance(r.parsed, UsersQueryResponse200):
            return _unwrap(r.parsed.users[id])["email"]

        raise Exception("Failed to get user information.", r)

    @staticmethod
    def invite_user(
        email,
        password,
        auth,
        api_endpoint: str = "http://api-lb:8080",
    ):
        # TODO: Refactor User.list_users() here when this stabilizes

        headers = {
            "authorization": auth._bearer_token_str(),
            "user-agent": _user_agent,
        }
        users = requests.post(
            f"{api_endpoint}/v1/api/users/query", data=json.dumps({}), headers=headers
        )
        if users.status_code > 299:
            print(users.content)
            print(users.text)
            raise Exception("Failed to list existing users.")
        existing_users = users.json()["users"].values()
        user_present = [user for user in existing_users if user["username"] == email]
        if len(user_present) == 0:
            data = {"email": email}
            if password:
                data["password"] = password
            response = requests.post(
                f"{api_endpoint}/v1/api/users/invite",
                json=data,
                headers=headers,
            )

            if response.status_code == 403:
                raise UserLimitError()
            if response.status_code != 200:
                raise Exception("Failed to invite user")

            user = response.json()
            return user
        else:
            return user_present[0]
