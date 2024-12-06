# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.services import Service
from rer.newsletter import _
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import MAIL_NOT_PRESENT
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from zExceptions import BadRequest
from zope.component import getMultiAdapter


class SubscriptionsDelete(Service):
    def reply(self):
        status = UNHANDLED

        email = self.request["email"]

        if not email:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "delete_subscriptions_missing_parameter",
                        default="You need to select at least one subscription or all.",
                    )
                )
            )

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)

        if email == "all":
            channel.deleteAllUsers()
        else:
            if isinstance(email, str):
                email = [email]
            for x in email:
                status = channel.deleteUser(x)
                if status != OK:
                    if status == MAIL_NOT_PRESENT:
                        raise BadRequest(
                            api.portal.translate(
                                _(
                                    "delete_subscriptions_wrong_email",
                                    default="Addess ${email} not found. Process stopped.",
                                    mapping={email: x},
                                )
                            )
                        )
                    raise BadRequest(
                        api.portal.translate(
                            _(
                                "delete_subscriptions_generic_error",
                                default="Error deleting ${email}. Process stopped.",
                                mapping={email: x},
                            )
                        )
                    )

        return self.reply_no_content()
