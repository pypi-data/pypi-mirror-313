# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from rer.newsletter import logger
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from six.moves import map
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class DeleteExpiredUsersView(BrowserView):
    """Delete expired users from channels"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.user_removed = 0

    def update_annotations(self, brain):
        channel = brain.getObject()
        expired_date = datetime.now()
        expired_time_token = self.context.portal_registry.get(
            "rer.newsletter.browser.settings.ISettingsSchema.expired_time_token",  # noqa
            None,
        )

        adapter = getMultiAdapter((channel, self.request), IChannelSubscriptions)
        keys = [x for x in adapter.channel_subscriptions.keys()]
        for key in keys:
            subscription = adapter.channel_subscriptions[key]
            creation_date = datetime.strptime(
                subscription["creation_date"], "%d/%m/%Y %H:%M:%S"
            )
            if (
                creation_date + timedelta(hours=expired_time_token)
                < expired_date  # noqa
                and not subscription["is_active"]  # noqa
            ):
                del adapter.channel_subscriptions[key]
                self.user_removed += 1

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        logger.info("START:Remove expired user from channels")

        pc = getToolByName(self.context, "portal_catalog")  # noqa
        channels_brain = pc.unrestrictedSearchResults({"portal_type": "Channel"})

        list(map(lambda x: self.update_annotations(x), channels_brain))
        logger.info(
            "DONE:Remove {0} expired user from channels".format(self.user_removed)
        )
        return True
