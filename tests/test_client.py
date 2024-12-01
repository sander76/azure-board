import pytest
from azure_board.cli import Add, Main
from azure_board.client import BoardClient


@pytest.mark.vcr
def test_create_item():
    add = Add(title="add poetry cache to pipeline", type="User Story")
    main = Main(organization="baringa", project="plcs", sub_command=add)
    client = BoardClient()

    result = client.create_item(main, add)

    print(result)
