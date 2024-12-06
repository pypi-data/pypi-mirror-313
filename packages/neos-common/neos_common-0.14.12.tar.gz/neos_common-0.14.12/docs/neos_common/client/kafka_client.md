Module neos_common.client.kafka_client
======================================

Classes
-------

`KafkaClient(host: str, logger_name: str, timing_logger_name: str, poll_timeout: float)`
:   

    ### Methods

    `produce(self, topic: str, value: str | bytes, key: str | bytes | None = None, partition: int | None = None, timestamp: int | None = None, headers: dict | list | None = None) ‑> None`
    :   Produce message to the Kafka topic.