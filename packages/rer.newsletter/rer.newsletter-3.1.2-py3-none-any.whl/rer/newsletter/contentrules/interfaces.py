# -*- coding: utf-8 -*-
from rer.newsletter import _
from zope import schema
from zope.interface import Interface


class Notify(Interface):
    subject = schema.TextLine(
        title=_("Subject"),
        description=_("Subject of the message"),
        required=True,
    )

    source = schema.TextLine(
        title=_("Sender email"),
        description=_(
            "The email address that sends the email. If no email is"
            " provided here, it will use the portal from address."
        ),
        required=True,
    )

    dest_addr = schema.TextLine(
        title=_("Receiver email"),
        description=_("The address where you want to send the e-mail message."),
        required=True,
    )

    message = schema.Text(
        title=_("Message"),
        description=_(
            "Type in here the message that you want to mail. Some defined "
            "content can be replaced: ${portal} will be replaced by the title"
            " of the portal. ${url} will be replaced by the URL of the "
            "newsletter.${channel} will be replaced by the newsletter channel"
            " name. ${subscriber} will be replaced by subscriber name."
        ),
        required=True,
    )


class INotifyOnSubscribe(Notify):
    """notify on subscribe"""


class INotifyOnUnsubscribe(Notify):
    """notify on unsubscribe"""
