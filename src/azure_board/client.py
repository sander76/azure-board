"""
https://github.com/microsoft/azure-devops-python-api/blob/dev/azure-devops/azure/devops/v7_1/work_item_tracking/work_item_tracking_client.py
https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-7.1&tabs=HTTP

"""

from __future__ import annotations

import json
import logging
from base64 import b64encode
from functools import cached_property
from typing import TYPE_CHECKING, Any

import httpx
import keyring

_logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from azure_board.cli import Add, Main


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
        data = json.dumps(body)
        _logger.debug(data)
        result = httpx.post(url, json=body, headers=self.headers, params=self._query)

        try:
            result.raise_for_status()
        except httpx.HTTPStatusError:
            print(result.text)
            raise

        return result.json()

    def create_item(self, main: Main, add: Add) -> dict:
        path = f"/{main.organization}/{main.project}/_apis/wit/workitems/${add.type}"

        body = [
            op_add("/fields/System.Title", value=add.title),
            op_add("/fields/System.WorkItemType", value=add.type),
            op_add("/fields/System.AreaPath", value=add.area_path),
        ]
        if add.assigned_to:
            body.append(op_add("/fields/System.AssignedTo", value=add.assigned_to))
        if add.description:
            body.append(op_add("/fields/System.Description", value=add.description))

        _logger.debug(body)
        result = self._post(path, body)

        return result
