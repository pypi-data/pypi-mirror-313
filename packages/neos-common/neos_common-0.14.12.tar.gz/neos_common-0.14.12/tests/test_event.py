import json
import pathlib
import time
import uuid
from unittest import mock

import pytest

from neos_common.event import (
    EMIT_LOG_FILENAME,
    Event,
    EventPacket,
    EventPackets,
    EventVersion,
    SyncEvent,
    TmpEmitter,
    logger,
)


class TestEventVersion:
    def test_init(self):
        version = EventVersion(2, 0, 1)
        assert version.major == 2
        assert version.minor == 0
        assert version.patch == 1

    def test_eq(self):
        version_a = EventVersion(2, 0, 0)
        version_b = EventVersion(3, 2, 1)
        assert version_a == version_a  # noqa: PLR0124
        assert version_a != version_b

    def test_le(self):
        version_a = EventVersion(2, 0, 0)
        version_b = EventVersion(1, 8, 9)
        assert version_a >= version_b

    def test_str(self):
        version = EventVersion(2, 4, 55)
        assert str(version) == "v2.4.55"

    def test_from_string_success(self):
        assert EventVersion.from_string("v20.41.55") == EventVersion(20, 41, 55)

    @pytest.mark.parametrize(
        ("value"),
        ["v20..55", "v.1.5", "v2.1.", "20.41.55"],
    )
    def test_from_string_failure(self, value):
        with pytest.raises(ValueError, match=f"Could not parse event version from {value}"):
            EventVersion.from_string(value)


class CustomEvent(Event):
    def version(self) -> EventVersion:
        return EventVersion(1, 0, 0)


class TestEvent:
    @pytest.mark.parametrize(
        ("message", "json_serializable"),
        [
            ("some message", False),
            ({"a": 1, "b": [2, 3]}, True),
        ],
    )
    async def test_emit(self, tmp_path, monkeypatch, message, json_serializable):
        test_time = int(time.time())

        monkeypatch.setattr("neos_common.event.Path", mock.Mock(return_value=tmp_path))
        monkeypatch.setattr("neos_common.event.time.time", mock.Mock(return_value=test_time))

        event = CustomEvent(emitter=TmpEmitter())
        if json_serializable:
            message_json = json.dumps(message)
            span_id = await event.emit(message_json)
        else:
            span_id = await event.emit(message)

        dir_0, dir_1, filename = TmpEmitter.split_uuid_to_dirs_and_filename(span_id)
        check_path = pathlib.Path(tmp_path) / dir_0 / dir_1 / filename

        with check_path.open("r") as f:
            assert EventPackets(**json.load(f)) == EventPackets(
                packets=[
                    EventPacket(
                        source="source",
                        timestamp=test_time * 1000,
                        span_id=span_id,
                        version="v1.0.0",
                        message=message,
                        message_type="unknown",
                    ),
                ],
            )

        emit_log = pathlib.Path(tmp_path) / EMIT_LOG_FILENAME
        assert emit_log.is_file()

    async def test_emit_multiple_times(self, tmp_path, monkeypatch):
        test_time = int(time.time())

        monkeypatch.setattr("neos_common.event.Path", mock.Mock(return_value=tmp_path))
        monkeypatch.setattr("neos_common.event.time.time", mock.Mock(return_value=test_time))

        span_id = uuid.uuid4()
        event = CustomEvent(emitter=TmpEmitter())
        message_1 = {"a": 1, "b": [1, 2]}
        returned_span_id = await event.emit(json.dumps(message_1), span_id)
        assert returned_span_id == span_id

        message_2 = {"c": 3, "d": [4, 5]}
        returned_span_id = await event.emit(json.dumps(message_2), span_id)
        assert returned_span_id == span_id

        dir_0, dir_1, filename = TmpEmitter.split_uuid_to_dirs_and_filename(span_id)
        check_path = pathlib.Path(tmp_path) / dir_0 / dir_1 / filename

        with check_path.open("r") as f:
            assert (
                json.load(f)
                == EventPackets(
                    packets=[
                        EventPacket(
                            source="source",
                            timestamp=test_time * 1000,
                            span_id=span_id,
                            version="v1.0.0",
                            message=message_1,
                            message_type="unknown",
                        ),
                        EventPacket(
                            source="source",
                            timestamp=test_time * 1000,
                            span_id=span_id,
                            version="v1.0.0",
                            message=message_2,
                            message_type="unknown",
                        ),
                    ],
                ).model_dump()
            )

        emit_log = pathlib.Path(tmp_path) / EMIT_LOG_FILENAME
        assert emit_log.is_file()

    async def test_emit_suppresses_errors(self, monkeypatch):
        monkeypatch.setattr(TmpEmitter, "read_event_packets", mock.Mock(side_effect=Exception))
        monkeypatch.setattr(logger, "exception", mock.Mock())

        span_id = uuid.uuid4()
        event = CustomEvent(emitter=TmpEmitter())
        message_1 = {"a": 1, "b": [1, 2]}
        await event.emit(json.dumps(message_1), span_id)

        assert logger.exception.call_args == mock.call("Failed to emit event.")

    async def test_log_rotation(self, monkeypatch, tmp_path):
        monkeypatch.setattr("neos_common.event.Path", mock.Mock(return_value=tmp_path))

        keep_lines = 3
        emitter = TmpEmitter(keep_lines)
        event = CustomEvent(emitter=emitter)

        for _i in range(20):
            await event.emit("string message")

        event_log = tmp_path / EMIT_LOG_FILENAME

        with event_log.open("r") as f:
            assert len(f.readlines()) == keep_lines

    async def test_emit_cleanup(self, monkeypatch, tmp_path):
        monkeypatch.setattr("neos_common.event.Path", mock.Mock(return_value=tmp_path))

        emitter = TmpEmitter()
        event = CustomEvent(emitter=emitter)

        span_id_0 = uuid.uuid4()
        await event.emit(json.dumps({"a": 1, "b": [1, 2]}), span_id=span_id_0)
        await event.emit(json.dumps({"c": 3, "d": [4, 5]}), span_id=span_id_0)
        span_id_1 = uuid.uuid4()
        await event.emit("string message", span_id=span_id_1)

        emitter = TmpEmitter(3)
        event = CustomEvent(emitter=emitter)
        span_id_2 = uuid.uuid4()
        await event.emit("string message", span_id=span_id_2)

        event_log = tmp_path / EMIT_LOG_FILENAME

        with event_log.open("r") as f:
            lines = f.readlines()
            assert len(lines) == 3
            assert any(line for line in lines if str(span_id_0) in line)
            assert any(line for line in lines if str(span_id_1) in line)
            assert any(line for line in lines if str(span_id_2) in line)

        event_packets = emitter.read_event_packets(span_id_0)
        assert len(event_packets.packets) == 1
        assert event_packets.packets[0].message == {"c": 3, "d": [4, 5]}

    async def test_read_write_emit_file_without_session_id(self, monkeypatch, tmp_path):
        monkeypatch.setattr("neos_common.event.Path", mock.Mock(return_value=tmp_path))

        emitter = TmpEmitter()
        event = CustomEvent(emitter=emitter)

        span_id_0 = uuid.uuid4()
        await event.emit(json.dumps({"a": 1, "b": [1, 2]}), span_id=span_id_0)

        event_packets = emitter.read_event_packets(span_id_0)
        assert len(event_packets.packets) == 1
        assert event_packets.packets[0].message == {"a": 1, "b": [1, 2]}

        emitter.save_event_packets(span_id_0, EventPackets(packets=[]))
        event_packets = emitter.read_event_packets(span_id_0)
        assert len(event_packets.packets) == 0

    async def test_read_write_emit_file_with_session_id(self, monkeypatch, tmp_path):
        monkeypatch.setattr("neos_common.event.Path", mock.Mock(return_value=tmp_path))
        session_id = uuid.uuid4()

        emitter = TmpEmitter()
        event = CustomEvent(emitter=emitter)

        span_id_0 = uuid.uuid4()
        result = await event.emit(json.dumps({"a": 1, "b": [1, 2]}), span_id=span_id_0, session_id=session_id)

        assert result == span_id_0

        event_packets = emitter.read_event_packets(span_id_0, session_id)
        assert len(event_packets.packets) == 1
        assert event_packets.packets[0].message == {"a": 1, "b": [1, 2]}

        emitter.save_event_packets(span_id_0, EventPackets(packets=[]), session_id)
        event_packets = emitter.read_event_packets(span_id_0, session_id)
        assert len(event_packets.packets) == 0

    async def test_nested_cleanup(self, monkeypatch, tmp_path):
        monkeypatch.setattr("neos_common.event.Path", mock.Mock(return_value=tmp_path))

        emitter = TmpEmitter(4)
        event = CustomEvent(emitter=emitter)

        span_id_file_resolution_0 = uuid.UUID("00000a44-a47d-418e-937e-650f4424218c")
        span_id_file_resolution_1 = uuid.UUID("00001a44-a47d-418e-937e-650f4424218c")
        span_id_subdir_resolution_0 = uuid.UUID("00010a44-a47d-418e-937e-650f4424218c")
        span_id_dir_resolution_0 = uuid.UUID("01000a44-a47d-418e-937e-650f4424218c")

        msg = "message number {}"
        await event.emit(msg.format(0), span_id=span_id_file_resolution_0)
        await event.emit(msg.format(1), span_id=span_id_file_resolution_0)
        await event.emit(msg.format(2), span_id=span_id_file_resolution_1)
        await event.emit(msg.format(3), span_id=span_id_subdir_resolution_0)

        event_packets = emitter.read_event_packets(span_id_file_resolution_0)
        assert len(event_packets.packets) == 2

        assert emitter.get_event_filepath(span_id_file_resolution_0).is_file()
        assert emitter.get_event_filepath(span_id_file_resolution_1).is_file()
        assert emitter.get_event_filepath(span_id_subdir_resolution_0).is_file()
        assert not emitter.get_event_filepath(span_id_dir_resolution_0).is_file()

        await event.emit(msg.format(4), span_id=span_id_dir_resolution_0)
        await event.emit(msg.format(5), span_id=span_id_dir_resolution_0)
        await event.emit(msg.format(6), span_id=span_id_dir_resolution_0)
        await event.emit(msg.format(7), span_id=span_id_dir_resolution_0)

        event_packets = emitter.read_event_packets(span_id_dir_resolution_0)
        assert len(event_packets.packets) == 4

        assert not emitter.get_event_filepath(span_id_file_resolution_0).is_file()
        assert not emitter.get_event_filepath(span_id_file_resolution_1).is_file()
        assert not emitter.get_event_filepath(span_id_subdir_resolution_0).is_file()
        assert emitter.get_event_filepath(span_id_dir_resolution_0).is_file()

        await event.emit(msg.format(8), span_id=span_id_subdir_resolution_0)
        await event.emit(msg.format(9), span_id=span_id_file_resolution_1)
        await event.emit(msg.format(10), span_id=span_id_file_resolution_0)
        await event.emit(msg.format(11), span_id=span_id_file_resolution_0)

        event_packets = emitter.read_event_packets(span_id_file_resolution_0)
        assert len(event_packets.packets) == 2

        assert emitter.get_event_filepath(span_id_file_resolution_0).is_file()
        assert emitter.get_event_filepath(span_id_file_resolution_1).is_file()
        assert emitter.get_event_filepath(span_id_subdir_resolution_0).is_file()
        assert not emitter.get_event_filepath(span_id_dir_resolution_0).is_file()


class CustomSyncEvent(SyncEvent):
    def version(self) -> EventVersion:
        return EventVersion(1, 0, 0)


class TestSyncEvent:
    async def test_init(self):
        emitter_mock = mock.Mock()
        event = CustomSyncEvent(emitter=emitter_mock, source="real_source")
        assert event.emitter == emitter_mock
        assert event.source == "real_source"

    async def test_emit(self, monkeypatch):
        emitter_mock = mock.Mock()
        test_time = int(time.time())
        monkeypatch.setattr("neos_common.event.time.time", mock.Mock(return_value=test_time))

        event = CustomSyncEvent(emitter=emitter_mock, source="real_source")

        span_id = event.emit(message="my message", message_type="my message type")

        assert emitter_mock.mock_calls[0] == mock.call.emit(
            EventPacket(
                source="real_source",
                timestamp=test_time * 1000,
                span_id=span_id,
                version="v1.0.0",
                message="my message",
                message_type="my message type",
            ),
        )

    def test_get_event_filepath_without_session_id(self):
        emitter = TmpEmitter(4)
        span_id = uuid.uuid4()
        file_path = emitter.get_event_filepath(span_id)
        dir_0, dir_1, filename = TmpEmitter.split_uuid_to_dirs_and_filename(span_id)
        assert file_path == emitter.root_dir / dir_0 / dir_1 / filename

    def test_get_event_filepath_with_session_id(self):
        emitter = TmpEmitter(4)
        span_id = uuid.uuid4()
        session_id = uuid.uuid4()
        file_path = emitter.get_event_filepath(span_id, session_id)
        dir_0, dir_1, filename = TmpEmitter.split_uuid_to_dirs_and_filename(span_id)

        assert file_path == emitter.root_dir / dir_0 / dir_1 / str(session_id) / filename
