"""Collection of useful commands for `neosctl` management.

To view a list of available commands:

$ invoke --list
"""

import invoke


@invoke.task
def install(context):
    """Install production requirements for `neos_common`."""
    context.run("uv sync --extra kafka --extra config --extra auth")


@invoke.task
def install_dev(context):
    """Install development requirements for `neos_common`."""
    context.run("uv sync --all-extras")
    context.run("uv run pre-commit install")
    context.run(
        """
        echo "Generating pyrightconfig.json";
        echo "{\\"venv\\": \\".\\", \\"venvPath\\": \\".venv)\\", \\"exclude\\": [\\"tests\\"], \\"include\\": [\\"neos_common\\"]}" > pyrightconfig.json
    """,
    )


@invoke.task
def check_style(context):
    """Run style checks."""
    context.run("ruff .")


@invoke.task
def check_types(context):
    """Run pyright checks."""
    context.run("pyright neos_common")


@invoke.task
def tests(context):
    """Run pytest unit tests."""
    context.run("pytest -x -s")


@invoke.task
def tests_debug(context):
    """Run pytest unit tests with debug logs."""
    context.run("pytest -x -s -o log_cli=1 -o log-cli-level=DEBUG")


@invoke.task
def tests_coverage(context, output="term-missing"):
    """Run pytest unit tests with coverage.

    Coverage when plugins are involved gets funky, without this coverage is reported at 50-60% instead of 100%
    https://pytest-cov.readthedocs.io/en/latest/plugins.html
    """
    context.run(
        f"pytest --cov=neos_common -x --cov-report={output}",
    )


@invoke.task
def release(context):
    """Bump to next X.Y.Z version."""
    context.run("changelog generate")


@invoke.task
def bump_patch(context):
    """Bump to next X.Y.patch version."""
    context.run("changelog generate --version-part=patch")


@invoke.task
def bump_minor(context):
    """Bump to next X.minor.0 version."""
    context.run("changelog generate --version-part=minor")


@invoke.task
def bump_major(context):
    """Bump to next major.0.0 version."""
    context.run("changelog generate --version-part=major")
