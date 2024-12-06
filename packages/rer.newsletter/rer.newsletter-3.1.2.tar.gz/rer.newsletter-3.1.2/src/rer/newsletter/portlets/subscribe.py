# -*- coding: utf-8 -*-
from .interface import IPortletTileSchema
from plone import api
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer


@implementer(IPortletTileSchema)
class Assignment(base.Assignment):
    def __init__(self, header="", link_to_archive="", css_class="", newsletter=None):
        self.header = header
        self.link_to_archive = link_to_archive
        self.css_class = css_class
        self.newsletter = newsletter

    @property
    def title(self):
        if self.header:
            return self.header
        else:
            return "RER portlet newsletter"


class Renderer(base.Renderer):
    render = ViewPageTemplateFile("subscribe.pt")

    def getPortletClass(self):
        classes = "portlet NewsletterSubscribePortlet"
        if self.data.css_class:
            classes += " {0}".format(self.data.css_class)
        return classes

    def getNewsletterUrl(self):
        if self.data.newsletter:
            newsletter_obj = api.content.get(UID=self.data.newsletter)
            if newsletter_obj.is_subscribable:
                return newsletter_obj.absolute_url()

        elif self.context.portal_type == "Channel":
            return self.context.absolute_url()
        else:
            return None

    def is_subscribable(self):
        if self.data.newsletter:
            if api.content.get(UID=self.data.newsletter).is_subscribable:
                return True

        elif self.context.portal_type == "Channel" and self.context.is_subscribable:
            return True
        else:
            return False


class AddForm(base.AddForm):
    schema = IPortletTileSchema

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    schema = IPortletTileSchema
