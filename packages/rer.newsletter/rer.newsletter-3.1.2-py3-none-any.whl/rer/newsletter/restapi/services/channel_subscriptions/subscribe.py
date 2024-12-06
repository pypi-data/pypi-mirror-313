# -*- coding: utf-8 -*-
from plone import api
from plone.protect import interfaces
from plone.protect.authenticator import createToken
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from rer.newsletter import _
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import ALREADY_SUBSCRIBED
from rer.newsletter.utils import compose_sender
from rer.newsletter.utils import get_site_title
from rer.newsletter.utils import INVALID_EMAIL
from rer.newsletter.utils import SUBSCRIBED
from rer.newsletter.utils import UNHANDLED
from six import PY2
from zExceptions import BadRequest
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class NewsletterSubscribe(Service):
    def handle_subscribe(self, email):
        status = UNHANDLED

        if not self.context.is_subscribable:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "channel_not_subscribable",
                        default="Subscriptions to this channel are disabled.",
                    )
                )
            )

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)
        status, secret = channel.subscribe(email)

        if status != SUBSCRIBED:
            if status == ALREADY_SUBSCRIBED:
                raise BadRequest(
                    api.portal.translate(
                        _(
                            "channel_already_subscribed_error",
                            default="There is already a subscription to this newsletter for address ${email}."
                            " If you didn't have confirmed your subscription, it can be expired."
                            " Try to unsubscribe and subscribe again.",
                            mapping={"email": email},
                        )
                    )
                )
            elif status == INVALID_EMAIL:
                raise BadRequest(
                    api.portal.translate(
                        _(
                            "invalid_email",
                            default="Invalid email address",
                        )
                    )
                )
            else:
                raise BadRequest(
                    api.portal.translate(
                        _(
                            "error_subscription",
                            default="Unable to subscribe to this channel. Try to contact site administator.",
                        )
                    )
                )
        else:
            # creo il token CSRF
            token = createToken()

            # mando mail di conferma
            url = f"{self.context.absolute_url()}/confirm-subscription?secret={secret}&_authenticator={token}&action=subscribe"

            mail_template = self.context.restrictedTraverse("@@activeuser_template")

            parameters = {
                "title": self.context.title,
                "header": self.context.header,
                "footer": self.context.footer,
                "style": self.context.css_style,
                "activationUrl": url,
                "portal_name": get_site_title(),
            }

            mail_text = mail_template(**parameters)

            portal = api.portal.get()
            mail_text = portal.portal_transforms.convertTo("text/mail", mail_text)
            sender = compose_sender(channel=self.context)

            channel_title = self.context.title
            if PY2:
                channel_title = self.context.title.encode("utf-8")

            mailHost = api.portal.get_tool(name="MailHost")
            mailHost.send(
                mail_text.getData(),
                mto=email,
                mfrom=sender,
                subject="Conferma la tua iscrizione alla Newsletter {channel}"
                " del portale {site}".format(
                    channel=channel_title, site=get_site_title()
                ),
                charset="utf-8",
                msg_type="text/html",
                immediate=True,
            )

    def reply(self):
        data = json_body(self.request)
        email = data.get("email", "").lower()
        if not email:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "missing_email_label",
                        default="Missing required parameter: email.",
                    )
                )
            )

        if "IDisableCSRFProtection" in dir(interfaces):
            alsoProvides(self.request, interfaces.IDisableCSRFProtection)

        self.handle_subscribe(email=email)

        return self.reply_no_content()
