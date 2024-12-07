import logging
import time
from functools import partial

from confluent_kafka import KafkaException, Producer, cimpl


class KafkaClient:
    def __init__(
        self,
        host: str,
        logger_name: str,
        timing_logger_name: str,
        poll_timeout: float,
    ) -> None:
        self.host = host
        self.logger = logging.getLogger(logger_name)
        self.timing_logger = logging.getLogger(timing_logger_name)
        self.poll_timeout = poll_timeout
        self._producer = Producer(self._render_config(self.host))

    def _render_config(self, host: str) -> dict:
        return {
            "bootstrap.servers": host,
        }

    def _ack(
        self,
        start: float,
        topic: str,
        err: KafkaException,
        _: cimpl.Message,
    ) -> None:
        duration = (time.time() - start) * 1000

        if err:
            self.logger.exception(str(err))
            self.timing_logger.info(
                f"TIMING: Wall: {duration:.2f}ms | {err!s}",
            )
        else:
            self.logger.info(f"Kafka produce to topic: {topic}")
            self.timing_logger.info(
                f"TIMING: Wall: {duration:.2f}ms | Kafka produce to topic: {topic}",
            )

    def produce(
        self,
        topic: str,
        value: str | bytes,
        key: str | bytes | None = None,
        partition: int | None = None,
        timestamp: int | None = None,
        headers: dict | list | None = None,
    ) -> None:
        """Produce message to the Kafka topic."""
        start = time.time()

        kwargs = {
            k: v
            for k, v in {
                "key": key,
                "partition": partition,
                "on_delivery": partial(self._ack, start, topic),
                "timestamp": timestamp,
                "headers": headers,
            }.items()
            if v is not None
        }

        self._producer.produce(topic, value, **kwargs)
        self._producer.poll(self.poll_timeout)


__all__ = [
    "KafkaClient",
]
