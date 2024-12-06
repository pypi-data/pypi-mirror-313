# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import rer.newsletter


class RerNewsletterLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=rer.newsletter)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "rer.newsletter:default")


RER_NEWSLETTER_FIXTURE = RerNewsletterLayer()


RER_NEWSLETTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RER_NEWSLETTER_FIXTURE,),
    name="RerNewsletterLayer:IntegrationTesting",
)


RER_NEWSLETTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RER_NEWSLETTER_FIXTURE,),
    name="RerNewsletterLayer:FunctionalTesting",
)
