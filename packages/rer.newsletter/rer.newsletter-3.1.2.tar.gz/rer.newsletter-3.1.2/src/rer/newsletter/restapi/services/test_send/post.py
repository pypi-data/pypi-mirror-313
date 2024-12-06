# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from rer.newsletter import _
from zExceptions import BadRequest


class TestSendPost(Service):
    def reply(self):
        data = json_body(self.request)

        email = data.get("email", "")
        if not email:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "missing_email_label",
                        default="Missing required parameter: email.",
                    )
                )
            )

        self.context.send_preview(email=email)

        return self.reply_no_content()
