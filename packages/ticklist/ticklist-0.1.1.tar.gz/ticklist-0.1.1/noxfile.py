"""Nox file."""

import tomllib
from importlib.metadata import version
from pathlib import Path

import nox

# nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True

# nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv"

# get the supported python versions from the classifiers in pyproject.toml.
# which are automatically created using pyproject-fmt
pyp = tomllib.loads(Path("pyproject.toml").read_text())
pythons = [
    pv.rsplit(" ")[-1]
    for pv in pyp["project"]["classifiers"]
    if pv.startswith("Programming Language :: Python :: 3.")
]

pydantic_oldest = "2.5"
# keep this in sync with the pydantic dependency as defined in the pyproject.toml
pydantic_latest = version("pydantic")


def uv_install(session: nox.Session) -> None:
    session.run_install(
        "uv",
        "sync",
        "--frozen",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session(python=pythons, tags=["tests"])
@nox.parametrize("pydantic", [pydantic_latest, pydantic_oldest])
def tests(session: nox.Session, pydantic: str) -> None:
    """Testing."""
    uv_install(session)
    session.install(f"pydantic=={pydantic}")
    session.run("uv", "pip", "show", "pydantic")

    if session.python == pythons[-1] and pydantic == pydantic_latest:
        session.notify("coverage")
    else:
        session.run("pytest")


@nox.session
def coverage(session: nox.Session) -> None:
    """Coverage report."""
    uv_install(session)
    session.run("coverage", "run", "-m", "pytest")

    session.run("coverage", "report")


@nox.session(tags=["quality"])
def quality(session: nox.Session) -> None:
    """Quality checks."""
    uv_install(session)

    session.run(
        "ruff", "check", "src", "tests", "noxfile.py", "--fix", "--exit-non-zero-on-fix"
    )
    session.run("pyproject-fmt", "pyproject.toml")

    session.run("mypy", "src", "noxfile.py")
