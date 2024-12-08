# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Invites service."""

import logging
import json
import smtplib

import email.utils
from email.mime.text import MIMEText

from datalayer_common.config import (
    DATALAYER_CDN_URL,
    INVITES_MAIL_TOPIC,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
)
from datalayer_iam.services.messaging import messages_producer
from datalayer_solr.invites import (
    create_invite,
    get_invite_by_token,
    get_invites_sent_by_user,
    update_invite,
)
from datalayer_solr.models.user_jwt import UserJWT
from datalayer_solr.utils import new_ulid, new_uuid, now_string


logger = logging.getLogger("__name__")


def send_bulk_invites_service(from_user: UserJWT, invites):
    """Send buld invites."""
    mail_subject: str = invites["MAIL_SUBJECT"]
    mail_recipients = invites["MAIL_RECIPIENTS"]
    if isinstance(mail_recipients, list):
        mail_recipients = mail_recipients[0]
    html_mail_template: str = invites["HTML_MAIL_TEMPLATE"]
    recipients = mail_recipients.split(",")
    logger.info("Invite mail_recipients: [%s]", mail_recipients)
    logger.info("Invite recipients: [%s]", recipients)
    invitees = []
    for a_recipient in recipients:
        for recipient in email.utils.getaddresses([a_recipient]):
            logger.info("Invite is being processed for [%s] [%s] [%s]", recipient, mail_subject, html_mail_template)
            token = new_ulid()
            r = recipient[0]
            parts = r.split(' ')
            if len(parts) == 0:
                recipient_first_name = ""
                recipient_last_name = ""
            if len(parts) == 1:
                recipient_first_name = ""
                recipient_last_name = parts[0]
            if len(parts) > 1:
                recipient_first_name = parts[0]
                recipient_last_name = " ".join(parts[1:])
            recipient_email = recipient[1]
            invitees.append(" " + recipient_email)
            message = ""
            invite_url = f"{DATALAYER_CDN_URL}/invite/{token}"
            html_mail = html_mail_template.replace("MAIL_INVITE_BUTTON_URL", invite_url)
            html_mail = html_mail.replace("MAIL_RECIPIENT", recipient_first_name)
            invite = {
                "id": new_uuid(),
                "uid": new_ulid(),
                "type_s": "invite",
                "from_user_uid": from_user.uid,
                "from_user_handle_s": from_user.handle,
                "from_user_email_s": from_user.email,
                "from_user_first_name_t": from_user.first_name,
                "from_user_last_name_t": from_user.last_name,
                "to_email_s": recipient_email,
                "to_first_name_t": recipient_first_name,
                "to_last_name_t": recipient_last_name,
                "message_t": message,
                "token_s": token,
                "sent_ts_dt": now_string(),
            }
            create_invite(invite)
            with messages_producer(INVITES_MAIL_TOPIC) as producer:
                producer.is_connected()
                message_id = producer.send(
                    json.dumps(
                        {
                            "subject": mail_subject,
                            "recipient": recipient,
                            "recipient_first_name": recipient_first_name,
                            "recipient_last_name": recipient_last_name,
                            "recipient_email": recipient_email,
                            "html_mail": html_mail,
                        }
                    ).encode(errors="replace")
                )
                logger.info("Mail is queued with id [%s]", message_id)
    return invitees


def send_invite_service(from_user: UserJWT, first_name, last_name, mail, message):
    """Invite user."""
    token = new_ulid()
    invite = {
        "id": new_uuid(),
        "uid": new_ulid(),
        "type_s": "invite",
        "from_user_uid": from_user.uid,
        "from_user_handle_s": from_user.handle,
        "from_user_email_s": from_user.email,
        "from_user_first_name_t": from_user.first_name,
        "from_user_last_name_t": from_user.last_name,
        "to_email_s": mail,
        "to_first_name_t": first_name,
        "to_last_name_t": last_name,
        "message_t": message,
        "token_s": token,
        "sent_ts_dt": now_string(),
    }
    create_invite(invite)
    smtp_server = smtplib.SMTP(
        host=SMTP_HOST,
        port=SMTP_PORT,
    )
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
    logger.info(from_user)
    text = f"""This is an invite from {from_user.display_name()} ({from_user.email})

{message}

Please click the link below to create your account on Datalayer:

{DATALAYER_CDN_URL}/invite/{token}

Datalayer is currently an early-release service. We appreciate your
feedback, questions and suggestions. As appropriate, we encourage you 
to email our support group.

You may find the following resources helpful as you familiarize yourself with Datalayer.

- User Guide: https://docs.datalayer.io

- Support: https://github.com/datalayer/support/issues

- Email Support: support@datalayer.io

Happy Data Analysis!

Sincerely, The Datalayer Team.
"""
    logger.info("Sending invite mail to [%s] with content:\n%s", mail, text)
    msg = MIMEText(text)
    msg["Subject"] = "Ξ 👋 A warm invite to Datalayer"
    msg["From"] = f"Datalayer <{SMTP_USERNAME}>"
    msg["To"] = mail
    #    msg["Cc"] = user["email"]
    msg["Bcc"] = "eric@datalayer.io"
    smtp_server.send_message(msg)
    smtp_server.quit()
    return invite


def get_invite_by_token_service(token):
    """Get an invite by token."""
    return get_invite_by_token(token)


def confirm_invite_join_event_service(token):
    """Confirm an invite join event."""
    invite = get_invite_by_token(token)
    invite["join_ts_dt"] = now_string()
    update_invite(invite)


def get_invites_sent_by_user_service(user_uid):
    """Get invites sent by user."""
    return get_invites_sent_by_user(user_uid)


def unsubscribe_invite_from_news_service(token):
    """Unsubscribe an invite from news."""
    invite = get_invite_by_token(token)
    if invite is not None:
        invite["unsubscribe_from_news_b"] = ({"set": True},)
        update_invite(invite)
    return invite
