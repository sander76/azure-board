"""
https://github.com/microsoft/azure-devops-python-api/blob/dev/azure-devops/azure/devops/v7_1/work_item_tracking/work_item_tracking_client.py
https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-7.1&tabs=HTTP

"""

from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod
from base64 import b64encode
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any

import httpx
import keyring

from azure_board.config import AZURE_BOARD_DRYRUN

_logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from azure_board.cli import Add


def _get_token() -> str:
    token = keyring.get_password("azure", "boards")
    if token is None:
        raise ValueError("No token available.")

    return token


def op_add(path: str, value: Any):
    return {"op": "add", "path": path, "value": value}


@dataclass
class ItemResult:
    id: int
    item_url: str


def board_client() -> BaseClient:
    dry_run = bool(int(os.environ.get(AZURE_BOARD_DRYRUN, 0)))
    if dry_run:
        return StubClient()
    return BoardClient()


class BaseClient(ABC):
    @abstractmethod
    def create_item(self, add: Add) -> ItemResult:
        """Create a work item."""


class StubClient(BaseClient):
    def create_item(self, add: Add) -> ItemResult:
        return ItemResult(12345, "http://dummy_url")


class BoardClient(BaseClient):
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
            _logger.error(result)
            raise

        return result.json()

    def create_item(self, add: Add) -> ItemResult:
        _logger.info(f"create work item {add=!r}")
        path = f"/{add.organization}/{add.project}/_apis/wit/workitems/${add.type}"

        body = [
            op_add("/fields/System.Title", value=add.title),
            op_add("/fields/System.WorkItemType", value=add.type),
            op_add("/fields/System.AreaPath", value=add.area_path),
        ]
        if add.assigned_to:
            body.append(op_add("/fields/System.AssignedTo", value=add.assigned_to))
        if add.description:
            body.append(op_add("/fields/System.Description", value=add.description))

        _logger.debug(f"{body=!r}")
        result = self._post(path, body)
        _logger.debug(f"{result=!r}")

        edit_url = result["_links"]["html"]
        id = result["id"]
        return ItemResult(id=id, item_url=edit_url)
