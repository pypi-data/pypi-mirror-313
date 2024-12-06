# -*- coding: utf-8 -*-
from plone import api
from plone import schema
from rer.newsletter import _
from rer.newsletter.content.channel import Channel
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

import re


@provider(IContextAwareDefaultFactory)
def getDefaultChannel(context):
    for obj in context.aq_chain:
        if isinstance(obj, Channel):
            return api.content.get_uuid(obj=obj)


class IPortletTileSchema(Interface):
    header = schema.TextLine(
        title=_("title_portlet_header", default="Header"),
        description=_(
            "description_portlet_header",
            default="Title of the rendered portlet",
        ),
        constraint=re.compile("[^\\s]").match,
        required=False,
    )

    # link_to_archive = schema.ASCIILine(
    #     title=_(u'title_portlet_link', default=u'Details link'),
    #     description=_(
    #         u'description_portlet_link',
    #         default=u'If given, the header and footer will link to this URL.'
    #     ),
    #     required=False)

    css_class = schema.TextLine(
        title=_("title_css_portlet_class", default="Portlet class"),
        description=_(
            "description_css_portlet_class",
            default="CSS class to add at the portlet",
        ),
        required=False,
    )

    newsletter = schema.Choice(
        title=_("title_newsletter", default="Newsletter"),
        description=_("description_newsletter", default="Newsletters"),
        vocabulary="rer.newsletter.subscribablenewsletter.vocabulary",
        defaultFactory=getDefaultChannel,
        required=False,
    )
