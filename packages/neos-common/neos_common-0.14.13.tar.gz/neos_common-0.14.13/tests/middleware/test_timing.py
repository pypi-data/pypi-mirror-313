import uuid
from pathlib import Path
from unittest import mock

import pytest
from _pytest.capture import CaptureFixture

fastapi = pytest.importorskip("fastapi")
requests = pytest.importorskip("starlette.requests")
staticfiles = pytest.importorskip("starlette.staticfiles")
testclient = pytest.importorskip("starlette.testclient")
timing = pytest.importorskip("neos_common.middleware.timing")


@pytest.fixture
def client():
    app = fastapi.FastAPI()
    timing.add_timing_middleware(app, exclude="untimed")
    static_files_app = staticfiles.StaticFiles(directory=".")
    app.mount(path="/static", app=static_files_app, name="static")

    @app.get("/timed")
    def get_timed() -> None:
        pass

    @app.get("/untimed")
    def get_untimed() -> None:
        pass

    return testclient.TestClient(app)


def test_timing(capsys: CaptureFixture[str], client, monkeypatch) -> None:
    trace_id = uuid.uuid4()
    monkeypatch.setattr(timing.uuid, "uuid4", mock.Mock(return_value=trace_id))
    client.get("/timed")
    out, err = capsys.readouterr()
    assert err == ""
    assert out.startswith(f"TIMING ({trace_id.hex}): Start")
    assert f"TIMING ({trace_id.hex}): Wall" in out
    assert "CPU:" in out
    assert out.endswith("test_timing.get_timed\n")


def test_silent_timing(capsys: CaptureFixture[str], client) -> None:
    client.get("/untimed")
    out, err = capsys.readouterr()
    assert err == ""
    assert out == ""


def test_mount(capsys: CaptureFixture[str], client, monkeypatch) -> None:
    trace_id = uuid.uuid4()
    monkeypatch.setattr(timing.uuid, "uuid4", mock.Mock(return_value=trace_id))
    basename = Path(__file__).name
    client.get(f"/static/{basename}")
    out, err = capsys.readouterr()
    assert err == ""
    assert out.startswith(f"TIMING ({trace_id.hex}):")
    assert out.endswith("StaticFiles<'static'>\n")


def test_missing(capsys: CaptureFixture[str], client, monkeypatch) -> None:
    trace_id = uuid.uuid4()
    monkeypatch.setattr(timing.uuid, "uuid4", mock.Mock(return_value=trace_id))
    client.get("/will-404")
    out, err = capsys.readouterr()
    assert err == ""
    assert out.startswith(f"TIMING ({trace_id.hex}):")
    assert out.endswith("<Path: /will-404>\n")


@pytest.fixture
def client2():
    app2 = fastapi.FastAPI()
    timing.add_timing_middleware(app2, prefix="app2")

    @app2.get("/")
    def get_with_intermediate_timing(request: requests.Request) -> None:
        timing.record_timing(request, note="hello")

    return testclient.TestClient(app2)


def test_intermediate(capsys: CaptureFixture[str], client2, monkeypatch) -> None:
    trace_id = uuid.uuid4()
    monkeypatch.setattr(timing.uuid, "uuid4", mock.Mock(return_value=trace_id))
    client2.get("/")
    out, err = capsys.readouterr()
    assert err == ""
    outs = out.strip().split("\n")
    assert len(outs) == 3
    assert outs[0].startswith(f"TIMING ({trace_id.hex}): Start")
    assert outs[1].startswith(f"TIMING ({trace_id.hex}):")
    assert outs[1].endswith("test_timing.get_with_intermediate_timing (hello)")
    assert outs[2].startswith(f"TIMING ({trace_id.hex}):")
    assert outs[2].endswith("test_timing.get_with_intermediate_timing")


@pytest.fixture
def client3():
    app3 = fastapi.FastAPI()

    @app3.get("/")
    def fail_to_record(request: requests.Request) -> None:
        timing.record_timing(request)

    return testclient.TestClient(app3)


def test_recording_fails_without_middleware(client3) -> None:
    with pytest.raises(
        RuntimeError,
        match="No timer, or invalid timer, present on request. Ensure timing middleware is added to the app.",
    ):
        client3.get("/")
