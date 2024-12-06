import os
import pathlib
from unittest import mock

import pytest

from neos_common import changelog


@pytest.fixture
def cwd(tmp_path):
    orig = pathlib.Path.cwd()

    try:
        os.chdir(str(tmp_path))
        yield tmp_path
    finally:
        os.chdir(orig)


def test_generate_docs(cwd):
    (cwd / "docs").mkdir()
    ctx = mock.Mock(config=mock.Mock(custom={"pdoc": {"modules": ["neos_common"]}}))
    paths = changelog.generate_docs(ctx, "0.0.0")

    assert paths == [
        "docs/neos_common/index.md",
        "docs/neos_common/api.md",
        "docs/neos_common/authorization/index.md",
        "docs/neos_common/authorization/base.md",
        "docs/neos_common/authorization/token.md",
        "docs/neos_common/authorization/util.md",
        "docs/neos_common/authorization/validator.md",
        "docs/neos_common/base.md",
        "docs/neos_common/changelog.md",
        "docs/neos_common/cli.md",
        "docs/neos_common/client/index.md",
        "docs/neos_common/client/base.md",
        "docs/neos_common/client/email.md",
        "docs/neos_common/client/hub_client.md",
        "docs/neos_common/client/kafka_client.md",
        "docs/neos_common/client/keycloak_client.md",
        "docs/neos_common/config.md",
        "docs/neos_common/error.md",
        "docs/neos_common/event.md",
        "docs/neos_common/middleware/index.md",
        "docs/neos_common/middleware/timing.md",
        "docs/neos_common/schema.md",
        "docs/neos_common/socket/index.md",
        "docs/neos_common/socket/client.md",
        "docs/neos_common/socket/server.md",
        "docs/neos_common/socket/util.md",
        "docs/neos_common/util.md",
    ]
