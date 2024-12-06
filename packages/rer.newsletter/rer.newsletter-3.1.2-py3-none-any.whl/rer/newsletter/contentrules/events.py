# -*- coding: utf-8 -*-
try:
    from zope.component.interfaces import IObjectEvent
    from zope.component.interfaces import ObjectEvent
except ImportError:
    from zope.interface.interfaces import IObjectEvent
    from zope.interface.interfaces import ObjectEvent

from zope.interface import implementer


class ISubscriptionEvent(IObjectEvent):
    """Channel subscription event"""


class IUnsubscriptionEvent(IObjectEvent):
    """Channel unsubscription event"""


@implementer(ISubscriptionEvent)
class SubscriptionEvent(ObjectEvent):
    """A subscriptin has been confirmed"""

    def __init__(self, channel, user):
        super(SubscriptionEvent, self).__init__(channel)
        self.user = user


@implementer(IUnsubscriptionEvent)
class UnsubscriptionEvent(ObjectEvent):
    """An unsubscription has been confirmed"""

    def __init__(self, channel, user):
        super(UnsubscriptionEvent, self).__init__(channel)
        self.user = user
