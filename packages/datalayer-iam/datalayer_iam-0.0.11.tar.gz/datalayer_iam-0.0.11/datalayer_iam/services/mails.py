# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

"""Datalayer Mailing service."""

import logging
import smtplib

from email.mime.text import MIMEText

from datalayer_solr.utils import to_display_name

from datalayer_common.config import (
    SUPPORT_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USERNAME,
)


logger = logging.getLogger("__name__")


def send_email_service(to: str, subject: str, message: str, from_: str = "", bcc: str = "") -> None:
    """Send an email ``to`` with ``message``."""
    if SMTP_HOST and SMTP_PORT:
        smtp_server = smtplib.SMTP(
            host=SMTP_HOST,
            port=SMTP_PORT,
        )
        smtp_server.starttls()
        try:
            smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = from_ or f"Datalayer <{SMTP_USERNAME}>"
            msg["To"] = to
            msg["Bcc"] = bcc or "eric@datalayer.io"
            smtp_server.send_message(msg)
        finally:
            smtp_server.quit()
    else:
        logger.warning("No server SMTP defined - unable to send email.")


def send_message_by_email_service(account_handle, first_name, last_name, email_address, message):
    """Send an email."""
    display_name = to_display_name(first_name, last_name)
    smtp_server = smtplib.SMTP(
        host=SMTP_HOST,
        port=SMTP_PORT,
    )
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
    text = f"""Message from {display_name} <{email_address}> (handle: {account_handle})

First name: {first_name}
Last name: {last_name}

{message}
    """
    msg = MIMEText(text)
    msg["Subject"] = f"Ξ ✍️ Message from {display_name} to Datalayer"
    msg["From"] = f"Datalayer <{SMTP_USERNAME}>"
    msg["To"] = f"Datalayer <{SMTP_USERNAME}>"
    msg["Cc"] = f"{display_name} <{email_address}>"
    msg["Bcc"] = "eric@datalayer.io"
    smtp_server.send_message(msg)
    smtp_server.quit()


def send_waitinglist_email_service(first_name, last_name, email, affiliation):
    """Registing to the waiting list."""
    display_name = to_display_name(first_name, last_name)
    smtp_server = smtplib.SMTP(
        host=SMTP_HOST,
        port=SMTP_PORT,
    )
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
    text = f"""Hi {display_name} <{email}>

Congratulations. You are on the Datalayer waiting list. We keep you updated.

First name: {first_name}
Last name: {last_name}
Email: {email}
Affiliation: {affiliation}

Eric Charles
@echarles
    """
    msg = MIMEText(text)
    msg["Subject"] = "Ξ Welcome to the Datalayer waiting list"
    msg["From"] = f"Datalayer <{SMTP_USERNAME}>"
    msg["To"] = f"{display_name} <{email}>"
    msg["Cc"] = "eric@datalayer.io"
    smtp_server.send_message(msg)
    smtp_server.quit()


def send_support_email_service(subject: str, message: str, from_: str = "") -> None:
    """Send an email to the platform support.
    
    Args:
        subject: Email subject
        message: Email body
        from_: Expeditor user - `Name <email>`
    """
    smtp_server = smtplib.SMTP(
        host=SMTP_HOST,
        port=SMTP_PORT,
    )
    smtp_server.starttls()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)

    msg = MIMEText(f"""From: {from_}

Message:

{message}
""")
    msg["Subject"] = subject
    # TODO Discuss the From field (cfr SMTP rules)
#    msg["From"] = from_ or f"Datalayer <{SUPPORT_EMAIL}>"
    msg["From"] = f"Datalayer <{SMTP_USERNAME}>"
    msg["To"] = f"Datalayer <{SUPPORT_EMAIL}>"
    smtp_server.send_message(msg)
    smtp_server.quit()
