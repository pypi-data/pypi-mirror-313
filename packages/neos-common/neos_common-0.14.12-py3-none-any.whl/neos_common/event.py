import abc
import datetime
import enum
import json
import logging
import random
import re
import string
import time
import typing
import uuid
from pathlib import Path
from typing import Annotated

import pydantic

EMIT_LOG_FILENAME = "emit.log"
MAX_EMIT_LOG_LINE_LENGTH = 1000
ROOT_DIR = "/tmp/core-events"  # noqa: S108

logger = logging.getLogger(__name__)

UUID4 = Annotated[pydantic.UUID4, pydantic.PlainSerializer(lambda x: str(x))]


class EventPacket(pydantic.BaseModel):
    source: str
    timestamp: int  # timestamp in ms
    span_id: UUID4
    version: str
    message: str | dict[str, typing.Any]
    message_type: str
    session_id: UUID4 | None = None


class EventPackets(pydantic.BaseModel):
    packets: list[EventPacket]


class EventVersion:
    VERSION_PATTERN = re.compile("^v(\\d+).(\\d+).(\\d+)$")

    def __init__(self, major: int, minor: int, patch: int) -> None:
        """Define version of the event.

        Args:
            major (int): version of the Gateway API
            minor (int): breaking changes
            patch (int): non-breaking changes
        """
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other: object) -> bool:
        """Compare version for equality."""
        if not isinstance(other, EventVersion):
            return NotImplemented
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __le__(self, other: "EventVersion") -> bool:
        """Compare version."""
        return (self.major, self.minor, self.patch) <= (other.major, other.minor, other.patch)

    def __str__(self) -> str:
        """Convert to string."""
        return f"v{self.major}.{self.minor}.{self.patch}"

    @staticmethod
    def from_string(value: str) -> "EventVersion":
        m = EventVersion.VERSION_PATTERN.match(value)
        if not m:
            msg: str = f"Could not parse event version from {value}"
            raise ValueError(msg)
        return EventVersion(int(m.group(1)), int(m.group(2)), int(m.group(3)))


class EventType(enum.Enum):
    secret = "secret"  # noqa: S105
    tag = "tag"
    output = "output"
    data_product = "data_product"
    data_source = "data_source"
    data_system = "data_system"
    data_unit = "data_unit"
    spark = "spark"
    builder = "builder"
    journal_note = "journal_note"


class EventScope(enum.Enum):
    secret = EventType.secret.value
    secret_keys = f"{EventType.secret.value}.keys"

    tag = EventType.tag.value

    output = EventType.output.value
    output_info = f"{EventType.output.value}.info"
    output_journal = f"{EventType.output.value}.journal"

    data_product = EventType.data_product.value
    data_product_data = f"{EventType.data_product.value}.data"
    data_product_metadata = f"{EventType.data_product.value}.metadata"
    data_product_output = f"{EventType.data_product.value}.output"
    data_product_data_product = f"{EventType.data_product.value}.data_product"
    data_product_info = f"{EventType.data_product.value}.info"
    data_product_journal = f"{EventType.data_product.value}.journal"
    data_product_schema = f"{EventType.data_product.value}.schema"
    data_product_spark = f"{EventType.data_product.value}.spark"
    data_product_spark_state = f"{EventType.data_product.value}.spark_state"
    data_product_spark_builder = f"{EventType.data_product.value}.spark_builder"
    data_product_expectations = f"{EventType.data_product.value}.expectations"
    data_product_data_quality = f"{EventType.data_product.value}.data_quality"
    data_product_profiling = f"{EventType.data_product.value}.profiling"
    data_product_validation = f"{EventType.data_product.value}.validation"
    data_product_classification = f"{EventType.data_product.value}.classification"
    data_product_classification_configuration = f"{EventType.data_product.value}.classification.configuration"
    data_product_classification_result = f"{EventType.data_product.value}.classification.result"
    data_product_health = f"{EventType.data_product.value}.health"

    data_source = EventType.data_source.value
    data_source_info = f"{EventType.data_source.value}.info"
    data_source_journal = f"{EventType.data_source.value}.journal"
    data_source_connection = f"{EventType.data_source.value}.connection"
    data_source_health = f"{EventType.data_source.value}.health"
    data_source_secret = f"{EventType.data_source.value}.secret"
    data_source_state = f"{EventType.data_source.value}.state"
    data_source_data_unit = f"{EventType.data_source.value}.data_unit"

    data_system = EventType.data_system.value
    data_system_info = f"{EventType.data_system.value}.info"
    data_system_journal = f"{EventType.data_system.value}.journal"
    data_system_data_source = f"{EventType.data_system.value}.data_source"

    data_unit = EventType.data_unit.value
    data_unit_metadata = f"{EventType.data_unit.value}.metadata"
    data_unit_schema = f"{EventType.data_unit.value}.schema"
    data_unit_state = f"{EventType.data_unit.value}.state"
    data_unit_info = f"{EventType.data_unit.value}.info"
    data_unit_journal = f"{EventType.data_unit.value}.journal"
    data_unit_health = f"{EventType.data_unit.value}.health"
    data_unit_profiling = f"{EventType.data_unit.value}.profiling"
    data_unit_config = f"{EventType.data_unit.value}.config"
    data_unit_data_product = f"{EventType.data_unit.value}.data_product"

    spark = EventType.spark.value
    spark_status = f"{EventType.spark.value}.status"

    builder = EventType.builder.value

    journal_note = EventType.journal_note.value


class EventAction(enum.Enum):
    secret_add = f"{EventScope.secret.value}:add"
    secret_update = f"{EventScope.secret.value}:update"
    secret_delete = f"{EventScope.secret.value}:delete"
    secret_keys_delete = f"{EventScope.secret_keys.value}:delete"

    tag_add = f"{EventScope.tag.value}:add"
    tag_delete = f"{EventScope.tag.value}:delete"

    output_create = f"{EventScope.output.value}:create"
    output_update = f"{EventScope.output.value}:update"
    output_delete = f"{EventScope.output.value}:delete"
    output_info_update = f"{EventScope.output_info.value}:update"
    output_journal_add = f"{EventScope.output_journal.value}:add"

    data_product_create = f"{EventScope.data_product.value}:create"
    data_product_update = f"{EventScope.data_product.value}:update"
    data_product_delete = f"{EventScope.data_product.value}:delete"
    data_product_data_delete = f"{EventScope.data_product_data.value}:delete"
    data_product_metadata_update = f"{EventScope.data_product_metadata.value}:update"
    data_product_metadata_remove = f"{EventScope.data_product_metadata.value}:remove"
    data_product_schema_update = f"{EventScope.data_product_schema.value}:update"
    data_product_output_link = f"{EventScope.data_product_output.value}:link"
    data_product_output_unlink = f"{EventScope.data_product_output.value}:unlink"
    data_product_data_product_link = f"{EventScope.data_product_data_product.value}:link"
    data_product_data_product_unlink = f"{EventScope.data_product_data_product.value}:unlink"
    data_product_info_update = f"{EventScope.data_product_info.value}:update"
    data_product_journal_add = f"{EventScope.data_product_journal.value}:add"
    data_product_publish = f"{EventScope.data_product.value}:publish"
    data_product_unpublish = f"{EventScope.data_product.value}:unpublish"
    data_product_spark_update = f"{EventScope.data_product_spark.value}:update"
    data_product_spark_builder_update = f"{EventScope.data_product_spark_builder.value}:update"
    data_product_spark_state_update = f"{EventScope.data_product_spark_state.value}:update"
    data_product_expectations_update = f"{EventScope.data_product_expectations.value}:update"
    data_product_profiling_update = f"{EventScope.data_product_profiling.value}:update"
    data_product_validation_update = f"{EventScope.data_product_validation.value}:update"
    data_product_classification_update = f"{EventScope.data_product_classification.value}:update"
    data_product_classification_configuration_update = (
        f"{EventScope.data_product_classification_configuration.value}:update"
    )
    data_product_classification_result_update = f"{EventScope.data_product_classification_result.value}:update"
    data_product_health_check = f"{EventScope.data_product_health.value}:check"

    data_source_create = f"{EventScope.data_source.value}:create"
    data_source_update = f"{EventScope.data_source.value}:update"
    data_source_delete = f"{EventScope.data_source.value}:delete"
    data_source_info_update = f"{EventScope.data_source_info.value}:update"
    data_source_journal_add = f"{EventScope.data_source_journal.value}:add"
    data_source_connection_update = f"{EventScope.data_source_connection.value}:update"
    data_source_secret_add = f"{EventScope.data_source_secret.value}:add"
    data_source_data_unit_link = f"{EventScope.data_source_data_unit.value}:link"
    data_source_data_unit_unlink = f"{EventScope.data_source_data_unit.value}:unlink"
    data_source_health_check = f"{EventScope.data_source_health.value}:check"
    data_source_state_update = f"{EventScope.data_source_state.value}:update"

    data_system_create = f"{EventScope.data_system.value}:create"
    data_system_update = f"{EventScope.data_system.value}:update"
    data_system_delete = f"{EventScope.data_system.value}:delete"
    data_system_info_update = f"{EventScope.data_system_info.value}:update"
    data_system_info_add = f"{EventScope.data_system_info.value}:add"
    data_system_journal_add = f"{EventScope.data_system_journal.value}:add"
    data_system_data_source_link = f"{EventScope.data_system_data_source.value}:link"
    data_system_data_source_unlink = f"{EventScope.data_system_data_source.value}:unlink"

    data_unit_create = f"{EventScope.data_unit.value}:create"
    data_unit_update = f"{EventScope.data_unit.value}:update"
    data_unit_metadata_update = f"{EventScope.data_unit_metadata.value}:update"
    data_unit_metadata_delete = f"{EventScope.data_unit_metadata.value}:delete"
    data_unit_schema_update = f"{EventScope.data_unit_schema.value}:update"
    data_unit_state_update = f"{EventScope.data_unit_state.value}:update"
    data_unit_delete = f"{EventScope.data_unit.value}:delete"
    data_unit_info_update = f"{EventScope.data_unit_info.value}:update"
    data_unit_journal_add = f"{EventScope.data_unit_journal.value}:add"
    data_unit_config_update = f"{EventScope.data_unit_config.value}:update"
    data_unit_data_product_link = f"{EventScope.data_unit_data_product.value}:link"
    data_unit_data_product_unlink = f"{EventScope.data_unit_data_product.value}:unlink"
    data_unit_health_check = f"{EventScope.data_unit_health.value}:check"
    data_unit_profiling_update = f"{EventScope.data_unit_profiling.value}:update"

    spark_finish = f"{EventScope.spark.value}:finish"
    spark_status_update = f"{EventScope.spark_status.value}:update"

    builder_preview = f"{EventScope.builder.value}:preview"

    journal_note_update = f"{EventScope.journal_note.value}:update"
    journal_note_delete = f"{EventScope.journal_note.value}:delete"


class Emitter(abc.ABC):
    def __init__(self, session_id: uuid.UUID | None = None) -> None:
        self.session_id = session_id

    @abc.abstractmethod
    async def emit(self, event_packet: EventPacket) -> None:
        pass


class SyncEmitter(abc.ABC):
    @abc.abstractmethod
    def emit(self, event_packet: EventPacket) -> None:
        pass


class TmpEmitter(Emitter):
    def __init__(self, max_emit_log_line_length: int = MAX_EMIT_LOG_LINE_LENGTH) -> None:
        self.max_emit_log_line_length = max_emit_log_line_length
        self.root_dir = self.ensure_root_folder_exists()

    @staticmethod
    def split_uuid_to_dirs_and_filename(span_id: uuid.UUID) -> tuple[str, str, str]:
        """Split span_id (uuid) into nested directories.

        Helper function that splits span_id (uuid) into nested directories.

        span_dir  span_subdir  span_filename
           87   /      39    / 0265-e23d-4574-b71e-dd1d61a74496

        for the purpose of storing large amount of files and maintaining performance
        with filesystems and other os tools

        Args:
        ----
        span_id: uuid.uuid4

        Returns: tuple (span_dir, span_subdir, span_filename)
        """
        span_id_str = str(span_id)

        span_dir = span_id_str[0:2]
        span_subdir = span_id_str[2:4]
        span_filename = span_id_str[4:]

        return span_dir, span_subdir, span_filename

    @staticmethod
    def ensure_root_folder_exists() -> Path:
        root_dir = Path(ROOT_DIR)
        root_dir.mkdir(exist_ok=True)

        return root_dir

    def get_event_filepath(self, span_id: uuid.UUID, session_id: uuid.UUID | None = None) -> Path:
        """Generate the file path for the emitted event.

        Args:
            span_id (uuid.UUID): The UUID for the event span.
            session_id (typing.Optional[str], optional): The user session ID,
            if applicable. Defaults to None.

        Returns:
            Path: The file path where the emitted event is saved.
        """
        span_dir, span_subdir, span_filename = self.split_uuid_to_dirs_and_filename(span_id)
        path = self.root_dir / span_dir / span_subdir
        if session_id:
            return path / str(session_id) / span_filename
        return path / span_filename

    def read_event_packets(self, span_id: uuid.UUID, session_id: uuid.UUID | None = None) -> EventPackets:
        """Read event packets from a given file path.

        Args:
            span_id (uuid.UUID): The UUID for the event span.
            session_id (typing.Optional[str], optional): The user session ID, if applicable.
            Defaults to None.

        Returns:
            EventPackets: The event packets read from the file.
        """
        event_filepath = self.get_event_filepath(span_id, session_id)

        if event_filepath.is_file():
            with event_filepath.open("r") as f:
                packets = json.load(f)
                event_packets = EventPackets(**packets)
        else:
            event_packets = EventPackets(packets=[])

        return event_packets

    def save_event_packets(
        self,
        span_id: UUID4,
        event_packets: EventPackets,
        session_id: UUID4 | None = None,
    ) -> None:
        """Save event packets with the given span ID and optional session ID.

        Args:
            span_id (UUID4): Unique identifier for the span of the event.
            event_packets (EventPackets): The event packets to be saved.
            session_id (UUID4 | None, optional): Optional session ID. Defaults to None.
        """
        event_filepath = self.get_event_filepath(span_id, session_id)

        event_filepath.parent.mkdir(parents=True, exist_ok=True)
        with event_filepath.open("w") as f:
            json.dump(event_packets.model_dump(), f)

    def clear_oldest_span_id_event(self, span_id: UUID4, session_id: UUID4 | None = None) -> None:
        # Remove span_id file
        dir_0, dir_1, filename = self.split_uuid_to_dirs_and_filename(span_id)

        # empty oldest info in span file
        event_packets = self.read_event_packets(span_id, session_id)
        if event_packets.packets:
            event_packets.packets.pop(0)

        if not event_packets.packets:
            # remove file
            self.get_event_filepath(span_id, session_id).unlink(missing_ok=True)

            # Remove span subdir if empty
            span_sub_dir = self.root_dir / dir_0 / dir_1
            file_count = len([child for child in span_sub_dir.iterdir() if child.is_file()])
            if file_count == 0:
                span_sub_dir.rmdir()

            # Remove span dir if empty
            span_dir = self.root_dir / dir_0
            dir_count = len([child for child in span_dir.iterdir() if child.is_dir()])
            if dir_count == 0:
                span_dir.rmdir()
        else:
            self.save_event_packets(span_id, event_packets)

    def ensure_emit_log_keep_size(self) -> None:
        history_log = self.root_dir / EMIT_LOG_FILENAME

        random_str = "".join(random.choice(string.ascii_lowercase) for i in range(8))  # noqa: S311
        history_log_tmp = self.root_dir / f"{random_str}_{EMIT_LOG_FILENAME}.tmp"

        if history_log.is_file():
            with history_log.open("r") as f:
                number_of_lines = len(f.readlines())

            diff = number_of_lines - (self.max_emit_log_line_length - 1)

            if diff > 0:
                with history_log.open("r") as original_f:
                    # skip the lines
                    for _i in range(diff):
                        # Remove line from event_log by moving the file pointer
                        line = original_f.readline().rstrip("\n")

                        span_id = uuid.UUID(line.split(" ")[-1])
                        self.clear_oldest_span_id_event(span_id)

                    # copy the rest
                    with history_log_tmp.open("w") as tmp_f:
                        for line in original_f:
                            tmp_f.write(line)

                # remove original and rename tmp file
                history_log.unlink()
                history_log_tmp.rename(history_log)

    def update_emit_log(self, event_packet: EventPacket) -> None:
        history_log = self.root_dir / EMIT_LOG_FILENAME

        self.ensure_emit_log_keep_size()

        with history_log.open("a") as f:
            f.write(
                f"{datetime.datetime.fromtimestamp(event_packet.timestamp / 1000.0, tz=datetime.timezone.utc)} {event_packet.message_type} {event_packet.span_id!s}\n",
            )

    async def emit(self, event_packet: EventPacket) -> None:
        try:
            dir_0, dir_1, filename = self.split_uuid_to_dirs_and_filename(event_packet.span_id)
            directory = self.root_dir / dir_0 / dir_1
            directory.mkdir(parents=True, exist_ok=True)

            event_packets = self.read_event_packets(event_packet.span_id, event_packet.session_id)
            event_packets.packets.append(event_packet)

            self.save_event_packets(event_packet.span_id, event_packets, event_packet.session_id)

            self.update_emit_log(event_packet)
        except Exception:
            logger.exception("Failed to emit event.")


def _prepare_event_packet(
    message: str | typing.Any,  # noqa: ANN401
    source: str,
    version: EventVersion,
    span_id: UUID4 | None = None,
    message_type: str = "unknown",
    session_id: UUID4 | None = None,
) -> EventPacket:
    span_id = span_id or uuid.uuid4()

    try:
        deserialized_message = json.loads(message)
    except (json.JSONDecodeError, TypeError):
        deserialized_message = message

    return EventPacket(
        source=source,
        timestamp=int(time.time() * 1000),  # timestamp in ms
        span_id=span_id,
        version=str(version),
        message=deserialized_message,
        message_type=message_type,
        session_id=session_id,
    )


class Event(abc.ABC):
    def __init__(self, emitter: Emitter, source: str = "source", session_id: UUID4 | None = None) -> None:
        self.emitter = emitter
        self.source = source
        self.session_id = session_id

    @abc.abstractmethod
    def version(self) -> EventVersion: ...

    async def emit(
        self,
        message: str,
        span_id: UUID4 | None = None,
        message_type: str = "unknown",
        session_id: UUID4 | None = None,
    ) -> uuid.UUID:
        span_id = span_id or uuid.uuid4()

        event_packet = _prepare_event_packet(
            message=message,
            source=self.source,
            span_id=span_id,
            version=self.version(),
            message_type=message_type,
            session_id=session_id,
        )

        await self.emitter.emit(event_packet)

        return span_id


class SyncEvent(abc.ABC):
    @abc.abstractmethod
    def version(self) -> EventVersion: ...

    def __init__(self, emitter: SyncEmitter, source: str = "source") -> None:
        self.emitter = emitter
        self.source = source

    def emit(
        self,
        message: str,
        span_id: UUID4 | None = None,
        message_type: str = "unknown",
    ) -> UUID4:
        span_id = span_id or uuid.uuid4()

        event_packet = _prepare_event_packet(
            message=message,
            source=self.source,
            span_id=span_id,
            version=self.version(),
            message_type=message_type,
        )

        self.emitter.emit(event_packet)

        return span_id


class ValidationResult(pydantic.BaseModel):
    """Data Quality validation results model."""

    id_: uuid.UUID = pydantic.Field(alias="id")
    entity_identifier: uuid.UUID
    expectations_id: uuid.UUID
    success: bool
    success_percentage: float
    score: int
    column_score: dict[str, int]
    category_weights: dict
    threshold: float
    field_thresholds: dict
    raw_result: dict
    global_stats: dict
    table_stats: dict
    column_stats: dict


class ProfilingResult(pydantic.BaseModel):
    """Profiling results model."""

    id_: uuid.UUID = pydantic.Field(alias="id")
    created_at: datetime.datetime
    entity_identifier: uuid.UUID
    dataset_type: str
    row_count: int
    column_count: int
    profile_sample: float
    column_stats: list[dict] | dict[str, typing.Any]


class ClassificationResult(pydantic.BaseModel):
    """Data classification results model."""

    id_: uuid.UUID = pydantic.Field(alias="id")
    entity_identifier: uuid.UUID
    dataset_type: str
    config: dict
    column_results: dict
