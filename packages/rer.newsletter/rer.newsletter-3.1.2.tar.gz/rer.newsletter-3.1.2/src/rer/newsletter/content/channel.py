# -*- coding: utf-8 -*-
from plone.app.contenttypes.content import Folder
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.interfaces import IChannel
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(IChannel)
class Channel(Folder):
    def active_subscriptions(self):
        channel = getMultiAdapter((self, self.REQUEST), IChannelSubscriptions)
        return channel.active_subscriptions
