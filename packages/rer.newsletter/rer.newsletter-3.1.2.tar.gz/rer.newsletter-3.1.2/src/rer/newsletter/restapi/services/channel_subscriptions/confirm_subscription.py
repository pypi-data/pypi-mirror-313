# -*- coding: utf-8 -*-
from plone import api
from plone.protect import interfaces
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from rer.newsletter import logger
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.contentrules.events import SubscriptionEvent
from rer.newsletter.contentrules.events import UnsubscriptionEvent
from rer.newsletter.utils import compose_sender
from rer.newsletter.utils import get_site_title
from rer.newsletter.utils import INEXISTENT_EMAIL
from rer.newsletter.utils import INVALID_SECRET
from rer.newsletter.utils import OK
from zope.component import getMultiAdapter
from zope.event import notify
from zope.interface import alsoProvides


class NewsletterConfirmSubscription(Service):
    def _sendGenericMessage(self, template, receiver, message, message_title):
        mail_template = self.context.restrictedTraverse("@@{0}".format(template))

        parameters = {
            "header": self.context.header,
            "footer": self.context.footer,
            "style": self.context.css_style,
            "portal_name": get_site_title(),
            "channel_name": self.context.title,
        }

        mail_text = mail_template(**parameters)

        portal = api.portal.get()
        mail_text = portal.portal_transforms.convertTo("text/mail", mail_text)

        response_email = compose_sender(self.context)

        # invio la mail ad ogni utente
        mail_host = api.portal.get_tool(name="MailHost")
        mail_host.send(
            mail_text.getData(),
            mto=receiver,
            mfrom=response_email,
            subject=message_title,
            charset="utf-8",
            msg_type="text/html",
        )

        return OK

    def reply(self):
        data = json_body(self.request)
        if "IDisableCSRFProtection" in dir(interfaces):
            alsoProvides(self.request, interfaces.IDisableCSRFProtection)
        secret = data.get("secret")
        action = data.get("action")
        errors = []
        response = None
        status = "error"
        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)

        if action == "subscribe":
            response, user = channel.activateUser(secret=secret)
            # mandare mail di avvenuta conferma
            if response == OK:
                notify(SubscriptionEvent(self.context, user))
                self._sendGenericMessage(
                    template="activeuserconfirm_template",
                    receiver=user,
                    message="Messaggio di avvenuta iscrizione",
                    message_title="Iscrizione confermata",
                )
                status = "generic_activate_message_success"

        elif action == "unsubscribe":
            response, mail = channel.deleteUserWithSecret(secret=secret)
            if response == OK:
                notify(UnsubscriptionEvent(self.context, mail))
                status = "generic_delete_message_success"

        if response != OK:
            # TODO: gestione corretta dei vari errori per informare il frontend
            if response == INVALID_SECRET:
                errors.append("user_secret_not_found")
            elif response == INEXISTENT_EMAIL:
                errors.append("user_not_found")
            else:
                errors.append("unable_to_unsubscribe")

            logger.info(
                'Unable to unsubscribe user with token "{token}" on channel {channel}.'.format(  # noqa
                    token=secret, channel=channel.context.absolute_url()
                )
            )

        return {
            "@id": self.request.get("URL"),
            "status": status if not errors else "error",
            "errors": errors if errors else None,
        }
