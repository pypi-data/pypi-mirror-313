# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

from __future__ import annotations


import contextlib
import logging
import typing

import pulsar
from pulsar import InitialPosition

from datalayer_common.config import PULSAR_URL


logger = logging.getLogger(__name__)


@contextlib.contextmanager
def messages_producer(topic: str) -> typing.Iterator[pulsar.Producer]:
    """Queue message producer."""
    client = pulsar.Client(PULSAR_URL, logger=logger)
    try:
        yield client.create_producer(
            topic, properties={"mail-producer": "datalayer_mailer"}
        )
    finally:
        client.close()


@contextlib.contextmanager
def messages_consumer(topic: str) -> typing.Iterator[pulsar.Consumer]:
    """Queue message consumer."""
    client = pulsar.Client(PULSAR_URL, logger=logger)
    try:
        yield client.subscribe(
            topic, "test_subscription", consumer_name="mail-consumer", initial_position=InitialPosition.Earliest
        )
    finally:
        client.close()
