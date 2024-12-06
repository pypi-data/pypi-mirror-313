# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from rer.newsletter import _
from rer.newsletter.restapi.services.message_send.get import NEWSLETTER_COUNTER_KEY
from rer.newsletter.utils import OK
from zExceptions import BadRequest
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides

import pyotp


class MessageSendPost(Service):
    def reply(self):
        self.validate_token()
        # Disable CSRF protection
        alsoProvides(self.request, IDisableCSRFProtection)
        res = self.context.send_message()
        status = res.get("status", "")

        # increase counter to generate a new token
        annotations = IAnnotations(self.context)
        counter = annotations.get(NEWSLETTER_COUNTER_KEY, 1)
        annotations[NEWSLETTER_COUNTER_KEY] = counter + 1

        if status != OK:
            msg = api.portal.translate(
                _(
                    "message_send_error",
                    default="Unable to send the message to subscribers. "
                    "Please contact the site administrator.",
                )
            )
            self.request.response.setStatus(500)
            return dict(error=dict(type="InternalServerError", message=msg))

        return self.reply_no_content()

    def validate_token(self):
        data = json_body(self.request)
        request_token = data.get("token", "")
        if not request_token:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "send_missing_token",
                        default="Missing token",
                    )
                )
            )

        annotations = IAnnotations(self.context)
        counter = annotations.get(NEWSLETTER_COUNTER_KEY, 1)  # it's first send
        hotp = pyotp.HOTP("base32secret3232")
        if not hotp.verify(request_token, counter):
            raise BadRequest(
                api.portal.translate(
                    _(
                        "send_wrong_token",
                        default="Invalid token",
                    )
                )
            )
