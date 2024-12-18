import pytest
from pydantic import ValidationError

from azure_board.cli import Add


@pytest.fixture
def base_add_model() -> dict:
    return {
        "title": "my title",
        "description": "my description",
        "type": "bug",
        "area_path": "my-area",
        "assigned_to": "me",
        "organization": "my organization",
        "project": "my project",
    }


def test_valid_type(base_add_model):
    """testing the runtime addition of a type literal for the type field.

    This is done at runtime right when everything is initialized.
    A config file is loaded from this test folder by means of an environment variable set
    in the __init__ of the main test module.
    """
    val = Add.model_validate(base_add_model | {"type": "Bug"})

    assert val.type == "Bug"


def test_invalid_type(base_add_model):
    """testing the runtime addition of a type literal for the type field.

    This is done at runtime right when everything is initialized.
    A config file is loaded from this test folder by means of an environment variable set
    in the __init__ of the main test module.
    """
    with pytest.raises(ValidationError, match="input_value='illegal type'"):
        Add.model_validate(base_add_model | {"type": "illegal type"})
