# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from rer.newsletter.testing import RER_NEWSLETTER_FUNCTIONAL_TESTING
from unittest import TestCase

import transaction


class SubscriptionTileTests(TestCase):
    layer = RER_NEWSLETTER_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portalURL = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.browser = Browser(self.layer["app"])
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            "Basic %s:%s" % (TEST_USER_NAME, TEST_USER_PASSWORD),
        )

        self.unprivileged_browser = Browser(self.layer["app"])

        self.channel = api.content.create(
            container=self.portal,
            type="Channel",
            title="Example channel",
            is_subscribable=True,
        )
        transaction.commit()

    def test_unable_to_subscribe_if_channel_is_not_subscribeable(self):
        self.channel.is_subscribable = False
        transaction.commit()
        self.unprivileged_browser.open(
            "{portal_url}/rer.newsletter.tile/unique?newsletter={uid}".format(
                portal_url=self.portalURL, uid=self.channel.UID()
            )
        )

        self.assertNotIn("Subscribe", self.unprivileged_browser.contents)

        # re-set default
        self.channel.is_subscribable = True
        transaction.commit()

    def test_able_to_subscribe_if_channel_is_subscribeable(self):
        self.channel.is_subscribable = True
        transaction.commit()

        self.unprivileged_browser.open(
            "{portal_url}/rer.newsletter.tile/unique?newsletter={uid}".format(
                portal_url=self.portalURL, uid=self.channel.UID()
            )
        )

        self.assertIn("Subscribe", self.unprivileged_browser.contents)
