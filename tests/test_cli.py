import pytest
from pydantic import ValidationError

from azure_board.cli import Add, Main


@pytest.fixture
def add() -> Add:
    add = Add(title="my title", type="type 1")
    return add


def test_valid_type():
    """testing the runtime addition of a type literal for the type field.

    This is done at runtime right when everything is initialized.
    A config file is loaded from this test folder by means of an environment variable set
    in the pyproject.toml. (pytest-env)
    """
    val = Add.model_validate({"title": "my title", "type": "type 1"})

    assert val.type == "type 1"


def test_invalid_type():
    with pytest.raises(ValidationError, match="input_value='illegal type'"):
        Add.model_validate({"title": "my title", "type": "illegal type"})


def test_main_defaults(add: Add):
    main = Main(sub_command=add)

    assert main.organization == "my org"
    assert main.project == "my project"
