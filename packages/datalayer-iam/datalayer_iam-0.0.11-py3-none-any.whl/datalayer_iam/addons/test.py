# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

import logging
from http import HTTPStatus
from pathlib import Path

from datalayer_addons.credits import (
    ABCCreditsAddon,
    CheckoutPortal,
    PCheckoutPortalRequest,
    UpdateCredits,
)

from ..services.credits import (
    get_account_credits_service,
)


HERE = Path(__file__).parent


logger = logging.getLogger(__name__)


async def checkout_portal_endpoint(uid):
    credits = await get_account_credits_service(uid)
    return f"""<html>
  <head>
    <title>Datalayer IAM Test credits account</title>
  </head>
  <body>
    <h1>Add credits to your account</h1>
    <p>Current balance for user <i>{uid}</i>: {credits.credits}</p>
    <form method="post" action="credits_account">
        <label>
            Credits: 
            <input type="number" name="credits" value="10" />
        </label>
        <label title="If checked, the user will consume the credits up to quota. It will reset the consumed credits.">
            Is it a quota? 
            <input type="checkbox" name="isQuota" />
        </label>
        <input type="submit" value="Submit" />
        <input type="hidden" name="uid" value="{uid}" />
    </form>
    <p>DON'T USE THIS IN PRODUCTION</p>
  </body>
</html>"""


async def credit_user_account(body):
    user_uid = body.get("uid")
    credits = float(body.get("credits", "0"))
    is_quota = body.get("isQuota") == "on"

    try:
        if is_quota:
            await ABCCreditsAddon.set_account_credits(
                UpdateCredits(account_uid=user_uid, quota=credits)
            )
        else:
            await ABCCreditsAddon.set_account_credits(
                UpdateCredits(account_uid=user_uid, credits=credits)
            )

        return {"success": True, "message": "Credits added"}, HTTPStatus.OK
    except Exception as e:
        logger.error(
            "Fail to update account [%s] credits with [%s]",
            user_uid,
            credits,
            exc_info=e,
        )
        return {
            "success": False,
            "message": "Bad request arguments",
        }, HTTPStatus.BAD_REQUEST


class TestAddon(ABCCreditsAddon):
    async def get_checkout_portal(
        self, user_uid: str, request: PCheckoutPortalRequest, token: str | None = None
    ) -> CheckoutPortal:
        return CheckoutPortal(
            url=f"/api/iam/test/v1/checkouts_portal?uid={user_uid}",
        )

    def get_routes(self) -> tuple[str, str] | None:
        """New routes to be register to the service.

        Returns:
            tuple:
                Path to openAPI spec YAML file
                Python module containing the endpoint callback
            None if nothing to add
        """
        return (str(HERE / "test.yaml"), "datalayer_iam.addons.test")


def get_test() -> ABCCreditsAddon:
    logger.critical("Using test addon provider. DON'T USE IT in production!!")
    return TestAddon()
