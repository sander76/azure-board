"""Nox file."""

import nox

nox.options.default_venv_backend = "uv"


@nox.session
def test(session: nox.Session) -> None:
    """Testing."""
    session.run_install(
        "uv",
        "sync",
        "--frozen",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )

    session.run("pytest")


@nox.session(tags=["quality"])
def quality(session: nox.Session) -> None:
    """Quality checks."""
    session.run_install(
        "uv",
        "sync",
        "--frozen",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )

    session.run("ruff", "check", "src", "tests", "noxfile.py", "--fix", "--exit-non-zero-on-fix")
    session.run("pyproject-fmt", "pyproject.toml")

    session.run("mypy", "src")
