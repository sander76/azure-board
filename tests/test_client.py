import pytest
from baringa_board.cli import Add
from baringa_board.client import BoardClient


@pytest.mark.vcr
def test_create_item():
    add = Add(
        organization="baringa", project="plcs", title="mytitle1", type="Bug", description="some description"
    )
    client = BoardClient()

    result = client.create_item(add)

    print(result)


def test_to_cli_model():
    new_model = Add.to_cli()

    assert new_model
