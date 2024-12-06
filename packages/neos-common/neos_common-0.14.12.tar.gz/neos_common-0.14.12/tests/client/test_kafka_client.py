import time
from unittest import mock

import pytest

kafka_client = pytest.importorskip("neos_common.client.kafka_client")


@pytest.fixture
def mock_confluent_kafka(monkeypatch):
    producer_mock = mock.Mock(name="producer_mock")
    monkeypatch.setattr(kafka_client, "Producer", producer_mock)
    return producer_mock


@pytest.fixture
def client(mock_confluent_kafka):  # noqa: ARG001
    return kafka_client.KafkaClient(
        host="kafka-cluster-host",
        logger_name="logger",
        timing_logger_name="timing_logger",
        poll_timeout=5,
    )


class TestKafkaClient:
    def test_init(self, mock_confluent_kafka):
        c = kafka_client.KafkaClient(
            host="kafka-cluster-host",
            logger_name="logger",
            timing_logger_name="timing_logger",
            poll_timeout=5,
        )

        assert c.host == "kafka-cluster-host"
        assert c.logger.name == "logger"
        assert c.timing_logger.name == "timing_logger"
        assert c.poll_timeout == 5

        assert mock_confluent_kafka.call_args == mock.call({"bootstrap.servers": "kafka-cluster-host"})

    def test_produce(self, client, monkeypatch):
        test_time = int(time.time())
        monkeypatch.setattr("neos_common.client.kafka_client.time.time", mock.Mock(return_value=test_time))

        ack_mock = mock.Mock()
        monkeypatch.setattr(kafka_client.KafkaClient, "_ack", ack_mock)

        client.produce(
            topic="topic",
            value="value",
            key="key",
            partition=None,
            timestamp=None,
            headers={"header-key": "header-value"},
        )

        produce_call = client._producer.mock_calls[0]
        assert produce_call.args == ("topic", "value")
        assert produce_call.kwargs["key"] == "key"
        assert produce_call.kwargs["headers"] == {"header-key": "header-value"}
        assert len(produce_call.kwargs) == 3
        assert client._producer.mock_calls[1] == mock.call.poll(5)

    def test_ack_message(self, client, monkeypatch):
        test_time = int(time.time())
        monkeypatch.setattr("neos_common.client.kafka_client.time.time", mock.Mock(return_value=test_time))

        logger_mock = mock.Mock()
        monkeypatch.setattr(client, "logger", logger_mock)

        client._ack(test_time, "topic", None, "msg")

        assert logger_mock.mock_calls == [mock.call.info("Kafka produce to topic: topic")]

    def test_ack_error(self, client, monkeypatch):
        test_time = int(time.time())
        monkeypatch.setattr("neos_common.client.kafka_client.time.time", mock.Mock(return_value=test_time))

        logger_mock = mock.Mock()
        monkeypatch.setattr(client, "logger", logger_mock)

        client._ack(test_time, "topic", "exception", None)

        assert logger_mock.mock_calls == [mock.call.exception("exception")]
