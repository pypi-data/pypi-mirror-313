# -*- coding: utf-8 -*-
from plone import api
from plone.protect import interfaces
from plone.protect.authenticator import createToken
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from rer.newsletter import _
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import compose_sender
from rer.newsletter.utils import get_site_title
from rer.newsletter.utils import INEXISTENT_EMAIL
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from six import PY2
from zExceptions import BadRequest
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class NewsletterUnsubscribe(Service):
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

        self.handle_unsubscribe(email=email)

        return self.reply_no_content()

    def handle_unsubscribe(self, email):
        status = UNHANDLED

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)

        status, secret = channel.unsubscribe(email)
        if status != OK:
            if status == INEXISTENT_EMAIL:
                raise BadRequest(
                    api.portal.translate(
                        _(
                            "unsubscribe_inexistent_mail",
                            default="Mail not found. Unable to unsubscribe.",
                        )
                    )
                )
            raise BadRequest(
                api.portal.translate(
                    _(
                        "unsubscribe_generic",
                        default="Unable to perform unsubscription. Please contact site administrators.",
                    )
                )
            )

        # creo il token CSRF
        token = createToken()

        # mando mail di conferma
        url = f"{self.context.absolute_url()}/confirm-subscription?secret={secret}&_authenticator={token}&action=unsubscribe"

        mail_template = self.context.restrictedTraverse("@@deleteuser_template")

        parameters = {
            "header": self.context.header,
            "title": self.context.title,
            "footer": self.context.footer,
            "style": self.context.css_style,
            "activationUrl": url,
        }

        mail_text = mail_template(**parameters)

        portal = api.portal.get()
        mail_text = portal.portal_transforms.convertTo("text/mail", mail_text)

        response_email = compose_sender(channel=self.context)
        channel_title = self.context.title
        if PY2:
            channel_title = self.context.title.encode("utf-8")

        mailHost = api.portal.get_tool(name="MailHost")
        mailHost.send(
            mail_text.getData(),
            mto=email,
            mfrom=response_email,
            subject=f"Conferma la cancellazione dalla newsletter {channel_title} del portale {get_site_title()}",
            charset="utf-8",
            msg_type="text/html",
            immediate=True,
        )
