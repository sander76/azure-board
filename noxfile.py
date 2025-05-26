"""
Nox file.
"""

from nox import Session, options
from nox_uv import session

options.default_venv_backend = "uv|virtualenv"


@session(uv_groups=["dev"])
def test(session: Session) -> None:
    """Testing."""
    # session.install(".")
    # session.run_install(
    #     "uv",
    #     "sync",
    #     "--frozen",
    #     env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    # )

    session.run("pytest")


@session(tags=["quality"], uv_groups=["dev"])
def quality(session: Session) -> None:
    """Quality checks."""
    # session.install(".")
    # session.run_install(
    #     "uv",
    #     "sync",
    #     "--frozen",
    #     env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    # )

    session.run("ruff", "check", "src", "tests", "noxfile.py", "--fix", "--exit-non-zero-on-fix")
    session.run("pyproject-fmt", "pyproject.toml")

    session.run("mypy", "src")
