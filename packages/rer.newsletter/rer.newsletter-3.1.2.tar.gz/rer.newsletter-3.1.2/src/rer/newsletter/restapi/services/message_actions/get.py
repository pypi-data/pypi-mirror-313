# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class MessageActions:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=True):
        # we set "expand" True by default because it's callable only on Messages
        # and we assume it is always expanded
        if self.context.portal_type != "Message":
            return {}
        result = {
            "message-actions": {
                "@id": f"{self.context.absolute_url()}/@message-actions"
            }
        }

        can_manage = self.context.can_manage_newsletter()
        can_send = self.context.can_send_message()
        if not can_manage and not can_send:
            return result

        result["message-actions"]["can_manage"] = can_manage
        result["message-actions"]["can_send"] = can_send
        result["message-actions"]["already_sent"] = self.context.message_already_sent()
        result["message-actions"][
            "active_subscriptions"
        ] = self.context.active_subscriptions()

        return result


class MessageActionsGet(Service):
    def reply(self):
        actions = MessageActions(self.context, self.request)
        return actions()["message-actions"]
