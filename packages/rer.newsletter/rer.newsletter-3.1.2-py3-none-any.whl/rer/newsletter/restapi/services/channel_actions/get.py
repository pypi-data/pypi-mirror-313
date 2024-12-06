# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class ChannelActions:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=True):
        # we set "expand" True by default because it's callable only on Channels
        # and we assume it is always expanded
        if self.context.portal_type != "Channel":
            return {}
        result = {
            "channel-actions": {
                "@id": f"{self.context.absolute_url()}/@channel-actions"
            }
        }

        can_manage = api.user.get_permissions(obj=self.context).get(
            "rer.newsletter: Manage Newsletter"
        )
        if can_manage:
            result["channel-actions"]["can_manage"] = can_manage

        return result


class ChannelActionsGet(Service):
    def reply(self):
        actions = ChannelActions(self.context, self.request)
        return actions()["channel-actions"]
