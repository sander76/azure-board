"""
https://github.com/microsoft/azure-devops-python-api/blob/dev/azure-devops/azure/devops/v7_1/work_item_tracking/work_item_tracking_client.py
https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-7.1&tabs=HTTP

"""

from __future__ import annotations

from base64 import b64encode
from functools import cached_property
from typing import TYPE_CHECKING, Any

import httpx
import keyring

if TYPE_CHECKING:
    from baringa_board.cli import Add


def _get_token() -> str:
    token = keyring.get_password("azure", "boards")
    if token is None:
        raise ValueError("No token available.")

    return token


def op_add(path: str, value: Any):
    return {"op": "add", "path": path, "value": value}


class BoardClient:
    def __init__(self):
        self._token = _get_token()
        self._query = {"api-version": "7.1"}
        self._host = "dev.azure.com"

    @cached_property
    def headers(self) -> dict:
        auth = b64encode(f":{self._token}".encode()).decode()
        return {
            "Content-Type": "application/json-patch+json",
            "Authorization": f"Basic {auth}",
        }

    def _post(self, path: str, body: list[dict]):
        url = httpx.URL(scheme="https", host=self._host, path=path)
        result = httpx.post(url, json=body, headers=self.headers, params=self._query)

        result.raise_for_status()

        return result.json()

    def create_item(self, organization: str, project: str, type: str, title: str, description: str) -> dict:
        path = f"/{organization}/{project}/_apis/wit/workitems/${type}"

        body = [
            op_add("/fields/System.Title", value=title),
            op_add("/fields/System.Description", value=description),
        ]

        result = self._post(path, body)

        return result
