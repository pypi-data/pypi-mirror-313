# -*- coding: utf-8 -*-
from plone import api
from plone.tiles import Tile


class SubscribeTile(Tile):
    def getPortletClass(self):
        classes = "tile tileNewsletter"
        if self.data.get("css_class", None):
            classes += " {0}".format(self.data.get("css_class"))
        return classes

    def getNewsletterUrl(self):
        if self.data.get("newsletter", None):
            newsletter_obj = api.content.get(UID=self.data.get("newsletter"))
            if newsletter_obj.is_subscribable:
                return newsletter_obj.absolute_url()
        elif self.context.portal_type == "Channel":
            return self.context.absolute_url()
        else:
            return None

    def is_subscribable(self):
        if self.data.get("newsletter", None):
            if api.content.get(UID=self.data.get("newsletter")).is_subscribable:
                return True

        elif self.context.portal_type == "Channel" and self.context.is_subscribable:
            return True
        else:
            return False
