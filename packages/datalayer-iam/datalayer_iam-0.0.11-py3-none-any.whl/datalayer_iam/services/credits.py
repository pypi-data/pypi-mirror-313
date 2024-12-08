# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Credits service."""

import asyncio
import asyncio.locks
import logging
import sys

from datetime import datetime, timedelta

import pysolr

from datalayer_addons.credits import ABCCreditsAddon, Account, UpdateCredits

from datalayer_solr.accounts import get_account_by_uid

from datalayer_solr.credits import (
    Credits,
    CreditsEvent,
    create_credits,
    create_credits_event,
    get_account_credits,
    update_credits,
    update_quota,
    emit_credits_event,
)
from datalayer_solr.accounts import (
    get_account_by_customer_id,
    update_user,
)
from datalayer_solr.usage import (
    ResourceState,
    Usage,
    start_reservation,
    get_account_reservations,
    end_reservation,
)
from datalayer_solr.utils import (
    new_ulid,
    now,
    now_string,
    normalize_iso_format,
    to_date,
    to_iso_string,
)

from datalayer_common.config import DATALAYER_CDN_URL
from datalayer_iam.services.mails import send_email_service
from datalayer_iam.config import CREDITS_PROVIDER


logger = logging.getLogger("__name__")


async def create_account_credits_service(
    account: dict, token: str | None = None, addon: ABCCreditsAddon | None = None
) -> Credits:
    """Create a credit item for the account."""
    account_uid = account["uid"]
    async with asyncio.Lock():
        credits = get_account_credits(account_uid)
        if credits is None:
            # Create empty credits
            logger.info("💳 Creating credits account for account_uid [%s]", account_uid)
            if addon is not None:
                name = " ".join((account["first_name_t"], account["last_name_t"]))
                customer = await addon.create_credits_customer(
                    Account(uid=account_uid, name=name, email=account["email_s"])
                )
                if customer is not None:
                    update_user(
                        account["handle_s"],
                        {
                            "id": account["id"],
                            "credits_customer_uid": {"set": customer.id},
                        },
                    )
            external_credits = (
                None
                if addon is None
                else await addon.get_account_credits(account_uid, token)
            )
            if external_credits is None:
                credits = create_credits(account_uid)
            else:
                credits = create_credits(
                    account_uid, external_credits.credits, external_credits.limit
                )
        return credits


async def get_account_credits_service(
    account_uid: str, token: str | None = None, addon: ABCCreditsAddon | None = None
) -> Credits:
    """Get the credits for the give account uid."""
    logger.info("💳 Get credits for account_uid [%s]", account_uid)

    account = get_account_by_uid(account_uid)
    if account is None:
        raise ValueError(f"Unknown account_uid {account_uid}")

    external_credits = (
        None if addon is None else await addon.get_account_credits(account_uid, token)
    )

    internal_credits = get_account_credits(account_uid)

    if external_credits is None:
        return internal_credits

    no_quota = external_credits.limit is None

    new_credits = external_credits.credits
    if external_credits.include_reservations:
        reservations = get_account_reservations_service(account_uid)
        new_credits += (1 if no_quota else -1) * sum(
            map(lambda r: r.credits_limit, reservations)
        )

    credits_needs_update = (
        abs(new_credits - internal_credits.credits) > sys.float_info.epsilon
    )
    if no_quota:
        if credits_needs_update:
            create_credits_event(
                CreditsEvent(
                    new_credits,
                    account_uid,
                    "sync-credits",
                    CREDITS_PROVIDER,
                )
            )
            return update_credits(internal_credits._db_id, new_credits)
    else:
        if (
            abs((external_credits.limit or 0.0) - (internal_credits.limit or 0.0))
            > sys.float_info.epsilon
            or credits_needs_update
        ):
            create_credits_event(
                CreditsEvent(
                    new_credits,
                    account_uid,
                    "sync-credits",
                    CREDITS_PROVIDER,
                    limit=external_credits.limit,
                )
            )
            return update_quota(internal_credits, external_credits.limit, new_credits)

    return internal_credits


async def update_account_credits_service(event: CreditsEvent) -> Credits:
    """Add (if > 0) or remove (if < 0) credits to account balance based on the event.credits value."""
    # TODO should this be going through the addon? For now charging is done when ending reservation
    # and increasing credits/user quota should be done through sync
    new_credits = emit_credits_event(event)
    if event.credits > 0:
        # Sending an email.
        # FIXME should we add a flag to silence all emails notification when white labelling?
        # NOTE For white labelled deployment, it may be the case that the SMTP server is not setup.
        account = get_account_by_uid(event.account_uid, public=False)
        send_email_service(
            account["email_s"],
            "Ξ 💳 New credits added to your Datalayer account",
            f"""Great news! {event.credits} credits are added to your Datalayer account.

You can use those credits to run Jupyter Remote Kernels.

See more details for the options on {DATALAYER_CDN_URL}/pricing

Thank you for using Datalayer.""",
        )
    return new_credits


async def update_account_quota_service(
    account_uid: str,
    quota: float,
    reset_credits: bool = True,
    origin_id: str = "",
    token: str | None = None,
    addon: ABCCreditsAddon | None = None,
) -> Credits:
    """Set a new quota to an account.

    By default it will reset the account credits.
    """
    logger.info("💳 Changing account [%s] quota to %s", account_uid, quota)
    credits = await get_account_credits_service(account_uid, token=token, addon=addon)

    emit_credits_event(
        CreditsEvent(
            credits=0.0,  # Changing the quota does not impact the user credits
            account_uid=account_uid,
            event="update-quota",
            origin_id=origin_id,
            limit=quota,
        )
    )

    # FIXME should we send an email?
    return update_quota(credits, quota, reset_credits)


async def set_account_credits_service(data: UpdateCredits) -> Credits:
    account_uid = data.account_uid
    if account_uid is None:
        account = get_account_by_customer_id(data.credits_customer_id)
        if account is None:
            raise ValueError(f"No account for customer ID {data.credits_customer_id}")
        account_uid = account["uid"]

    if data.credits is not None and data.credits > sys.float_info.epsilon:
        credits = await update_account_credits_service(
            CreditsEvent(
                credits=data.credits,
                account_uid=account_uid,
                event="credits",
                origin_id=f"Addon {CREDITS_PROVIDER}",
            )
        )
        return credits

    if data.quota is not None and data.quota > sys.float_info.epsilon:
        # We don't provide the addon here as the changes are triggered from it.
        credits = await update_account_quota_service(
            account_uid=account_uid,
            quota=data.quota,
            reset_credits=True,
            origin_id=f"Addon {CREDITS_PROVIDER}",
        )
        return credits

    raise ValueError(f"Failed to update account credits {data}")


def get_account_reservations_service(
    account_uid: str | None, reservation_type: str | None = None
) -> list[Usage]:
    """Get all account reservations."""
    return get_account_reservations(account_uid, reservation_type)


def get_reservation_service(account_uid: str, id: str) -> Usage | None:
    """Get a account reservation."""
    reservations = get_account_reservations(account_uid)
    return next(filter(lambda r: r.resource_uid == id, reservations), None)


async def start_reservation_service(
    account_uid: str,
    resource_uid: str,
    resource_type: str,
    reservation: float,
    burning_rate: float,
    resource_state: ResourceState | None = None,
    resource_given_name: str | None = None,
    pod_resources: dict[str, str] | None = None,
    token: str | None = None,
    addon: ABCCreditsAddon | None = None,
) -> Usage:
    """Start a reservation

    Raises:
        - ValueError: Not enough credits
    """
    started_at = now_string()
    provision = (
        None
        if addon is None
        else await addon.create_reservation(account_uid, reservation, token)
    )
    reservation = start_reservation(
        account_uid=account_uid,
        burning_rate=burning_rate,
        checkout_uid=None if provision is None else provision.id,
        pod_resources=pod_resources,
        reservation=reservation if provision is None else provision.credits,
        resource_given_name=resource_given_name,
        resource_type=resource_type,
        resource_uid=resource_uid,
        resource_state=resource_state or ResourceState.RUNNING,
        start_date=(
            started_at
            if provision is None
            else normalize_iso_format(provision.created_at)
        ),
    )
    return reservation


async def create_failed_reservation_service(
    account_uid: str,
    resource_type: str,
    reservation: float,
    resource_given_name: str | None = None,
) -> Usage:
    """Create a reservation that failed to be honored.

    This may happen for various reasons such as:
    - No pod available
    """

    reservation = start_reservation(
        account_uid=account_uid,
        resource_uid=new_ulid(),
        burning_rate=0.0,
        reservation=reservation,
        resource_given_name=resource_given_name,
        resource_type=resource_type,
        resource_state=ResourceState.NOT_AVAILABLE_ERROR,
    )
    return reservation


class NoReservation(ValueError):
    """Exception raised if no reservation exists."""


EVENT_TO_STATE = {
    "expired": ResourceState.CREDITS_STOP,
    "culled": ResourceState.CULLED_STOP,
    "deleted": ResourceState.USER_STOP,
    "anomaly": ResourceState.ANOMALY_STOP,
    "no_kernel": ResourceState.UNREACHABLE_ERROR,
}


async def stop_reservation_service(
    account_uid: str,
    reservation_uid: str,
    event: str,
    end_time: datetime | None = None,
    token: str | None = None,
    addon: ABCCreditsAddon | None = None,
) -> None:
    """Stop a reservation and charge the user for it.

    It won't charge the user more than the reservation limit in case
    of anomaly.

    Raises:
        ValueError if no reservation is found
    """
    try:
        reservation = get_reservation_service(account_uid, reservation_uid)
    except pysolr.SolrError as err:
        raise NoReservation(
            f"No reservation with id [{reservation_uid}] for account [{account_uid}]."
        ) from err
    if reservation is None:
        raise NoReservation(
            f"No reservation with id [{reservation_uid}] for account [{account_uid}]."
        )
    logger.info(
        "Stopping reservation [%s] for account [%s] due to event %s.",
        reservation_uid,
        account_uid,
        event,
    )
    # FIXME We have seen reservations without start_date...
    started_at = now() if reservation.start_date is None else to_date(reservation.start_date)
    notify_at = now() if end_time is None else end_time
    limit_time = started_at + timedelta(
        seconds=reservation.credits_limit / reservation.burning_rate
    )
    stopped_at = min(
        limit_time,
        notify_at,
    )
    duration = stopped_at - started_at
    credits = reservation.burning_rate * duration.total_seconds()
    if notify_at > limit_time + timedelta(seconds=1):
        logger.warning(
            "Stop reservation [%s] at [%s] after its expiration time %s. The customer won't be charged the extra time.",
            reservation_uid,
            notify_at.isoformat(),
            limit_time.isoformat(),
        )

    try:
        if addon is not None:
            await addon.end_reservation(
                reservation.checkout_uid,
                None if stopped_at >= limit_time else credits,
                token,
            )
    finally:
        # Whatever happen end the reservation and update the user credits
        try:
            end_reservation(
                reservation.resource_uid,
                EVENT_TO_STATE.get(event, ResourceState.UNKNOWN),
                to_iso_string(stopped_at),
                reservation.credits_limit if stopped_at >= limit_time else credits,
            )
        finally:
            emit_credits_event(
                CreditsEvent(
                    credits=-1.0 * credits,
                    account_uid=reservation.account_uid,
                    event="end_reservation",
                    origin_id=reservation.resource_uid,
                )
            )
