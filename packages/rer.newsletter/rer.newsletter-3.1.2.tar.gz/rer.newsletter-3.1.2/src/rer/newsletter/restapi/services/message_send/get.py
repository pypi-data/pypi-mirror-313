# -*- coding: utf-8 -*-
from plone.restapi.services import Service
from zope.annotation.interfaces import IAnnotations

import pyotp


NEWSLETTER_COUNTER_KEY = "newsletter-send-counter"


class SendTokenGet(Service):
    def reply(self):
        annotations = IAnnotations(self.context)
        counter = annotations.get(NEWSLETTER_COUNTER_KEY, 1)  # it's first send
        hotp = pyotp.HOTP("base32secret3232")
        token = hotp.at(counter)
        return {"token": token}
