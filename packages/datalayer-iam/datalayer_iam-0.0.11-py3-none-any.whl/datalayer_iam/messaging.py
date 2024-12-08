# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from datalayer_addons.credits import ABCCreditsAddon

from datalayer_common.config import PUB_SUB_ENGINE, PULSAR_URL, KERNELS_USAGE_TOPIC

from .services.credits import NoReservation, stop_reservation_service


logger = logging.getLogger(__name__)


async def listen_usage_messages(addon: ABCCreditsAddon | None = None) -> None:
    """Listen for usage messages on pub sub topic."""

    if PUB_SUB_ENGINE != "pulsar":
        return None

    import pulsar
    from pulsar import InitialPosition

    client = pulsar.Client(PULSAR_URL, logger=logger)

    try:
        logger.info("Start listening on topic '%s'.", KERNELS_USAGE_TOPIC)
        consumer: pulsar.Consumer = client.subscribe(
            KERNELS_USAGE_TOPIC,
            "iam",
            consumer_name="datalayer_iam",
            initial_position=InitialPosition.Earliest,
        )

        while True:
            try:
                msg = await asyncio.to_thread(consumer.receive)
                logger.info(
                    "Received message id='%s'",
                    msg.message_id(),
                )
                data = json.loads(msg.data())
                event = data.get("event_type")
                if event == "remote_kernel.end":
                    await stop_reservation_service(
                        data["account_uid"],
                        data["reservation_uid"],
                        data.get("event", "deleted"),
                        end_time=datetime.fromtimestamp(
                            data["created_at"],
                            timezone.utc,
                        ),
                        token=data.get("external_token"),
                        addon=addon,
                    )
                else:
                    logger.warning("Receive event of unknown type [%s]", data)

                await asyncio.to_thread(consumer.acknowledge, msg)
            except NoReservation as e:
                logger.warning(
                    "Skip stopping unknown reservation [%s].",
                    data["reservation_uid"],
                    exc_info=e,
                )
                await asyncio.to_thread(consumer.acknowledge, msg)
            except pulsar.Interrupted:
                logger.info("Stop receiving usage messages")
                break
            except asyncio.CancelledError:
                logger.info("Stop listening for usage messages")
                await asyncio.shield(asyncio.to_thread(consumer.unsubscribe))
                break
            except BaseException as e:
                logger.error(
                    "Failed to process message %s", msg.message_id(), exc_info=e
                )
                await asyncio.to_thread(consumer.negative_acknowledge, msg)
    finally:
        client.close()
