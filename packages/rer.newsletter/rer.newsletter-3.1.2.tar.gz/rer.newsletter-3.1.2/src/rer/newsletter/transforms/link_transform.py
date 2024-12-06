# -*- coding: utf-8 -*-
# from lxml import etree
from plone import api
from premailer import Premailer
from Products.PortalTransforms.interfaces import ITransform
from rer.newsletter.browser.settings import ISettingsSchema
from zope.interface import implementer

import re


# capire come usare questa classe
@implementer(ITransform)
class link_transform(object):
    """
    convert all source_link in destination_link and apply all style
    """

    __name__ = "link_transform"
    inputs = ("text/html",)
    output = "text/mail"

    def __init__(self, name=None):
        self.config_metadata = {
            "inputs": (
                "list",
                "Inputs",
                "Input(s) MIME type. Change with care.",
            ),
        }
        if name:
            self.__name__ = name

    def name(self):
        return self.__name__

    def convert(self, orig, data, **kwargs):
        p = Premailer(orig, strip_important=False)
        orig = p.transform()

        source_link = api.portal.get_registry_record("source_link", ISettingsSchema)
        if not source_link:
            source_link = api.portal.get().absolute_url()

        # If volto frontend_domain is set, use it as destination link
        try:
            destination_link = api.portal.get_registry_record(
                "volto.frontend_domain", default=""
            )
        except KeyError:
            destination_link = ""
        if destination_link.endswith("/"):
            destination_link = destination_link[:-1]
        if not destination_link:
            # otherwise, use the newsletter one
            destination_link = api.portal.get_registry_record(
                "destination_link", ISettingsSchema
            )

        # non è questo il modo migliore per fare il replace...
        # 1. non serve usare re.sub ma basta il replace di string
        # 2. forse sarebbe più corretto usare un metodo di lxml
        if source_link and destination_link:
            orig = re.sub(source_link, destination_link, orig)

        # tree = etree.HTML(orig)
        # tagList = tree.xpath('//a')
        # for tag in tagList:
        #     href = tag.get('href')
        #     href = href.replace(source_link, destination_link)
        #      tag.set('href', href)
        # data.setData(etree.tostring(tree))
        data.setData(orig)

        return data


def register():
    return link_transform()
