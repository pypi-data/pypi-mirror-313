# -*- coding: utf-8 -*-
from .interfaces import INotifyOnSubscribe
from .interfaces import INotifyOnUnsubscribe
from OFS.SimpleItem import SimpleItem
from plone.contentrules.rule.interfaces import IRuleElementData
from zope.interface import implementer


@implementer(INotifyOnSubscribe, IRuleElementData)
class NotifyOnSubscribeAction(SimpleItem):
    subject = ""
    source = ""
    dest_addr = ""
    message = ""

    element = "plone.actions.NotificationOnSubscribe"

    @property
    def summary(self):
        return "Send email for user subscribe"


@implementer(INotifyOnUnsubscribe, IRuleElementData)
class NotifyOnUnsubscribeAction(SimpleItem):
    subject = ""
    source = ""
    dest_addr = ""
    message = ""

    element = "plone.actions.NotificationOnUnsubscribe"

    @property
    def summary(self):
        return "Send email for user unsubscribe"
