from __future__ import annotations

import json
import logging
import os
import random
from time import sleep

from kafka import KafkaProducer
from kafka.errors import KafkaError

from generator.message import generate_api_event


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(levelname)s %(asctime)s: %(message)s",
)


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "synthetic-api-events")
INTERVAL_MIN_SEC = float(os.getenv("INTERVAL_MIN_SEC", "0.3"))
INTERVAL_MAX_SEC = float(os.getenv("INTERVAL_MAX_SEC", "2.5"))


def build_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        retries=5,
    )


def run() -> None:
    if INTERVAL_MIN_SEC <= 0 or INTERVAL_MAX_SEC <= 0:
        raise ValueError("INTERVAL_MIN_SEC and INTERVAL_MAX_SEC must be positive")
    if INTERVAL_MIN_SEC > INTERVAL_MAX_SEC:
        raise ValueError("INTERVAL_MIN_SEC cannot be greater than INTERVAL_MAX_SEC")

    while True:
        producer: KafkaProducer | None = None
        try:
            producer = build_producer()
            logging.info(
                "Producer started, topic=%s, bootstrap=%s",
                KAFKA_TOPIC,
                KAFKA_BOOTSTRAP_SERVERS,
            )

            while True:
                event = generate_api_event().as_dict()
                delivery = producer.send(KAFKA_TOPIC, value=event)
                delivery.get(timeout=10)
                logging.info(
                    "Published event %s %s %s",
                    event["source_service"],
                    event["method"],
                    event["endpoint"],
                )
                sleep(random.uniform(INTERVAL_MIN_SEC, INTERVAL_MAX_SEC))
        except KafkaError:
            logging.exception("Kafka error. Retrying producer startup in 3 seconds...")
            sleep(3)
        except Exception:
            logging.exception("Unexpected producer error. Retrying in 3 seconds...")
            sleep(3)
        finally:
            if producer is not None:
                producer.close()


if __name__ == "__main__":
    run()
