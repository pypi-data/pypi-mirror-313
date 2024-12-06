# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.content import Collection
from rer.newsletter.content.message import Message
from rer.newsletter.interfaces import IBlocksToHtml
from zope.component import adapter
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import Interface


class IShippableMarker(Interface):
    """Marker interface for shippable object"""


class IShippable(Interface):
    """Interface for shippable object"""


alsoProvides(IShippable)


@adapter(IShippableMarker)
class Shippable(object):
    def __init__(self, context):
        self.context = context

    @property
    def message_content(self):
        if isinstance(self.context, Collection):
            return api.content.get_view(
                name="collection_sending_view",
                context=self.context,
                request=self.context.REQUEST,
            )()
        elif isinstance(self.context, Message):
            # return self.context.text.output if self.context.text else ""
            blocks_converter = getUtility(IBlocksToHtml)
            return blocks_converter(
                context=self.context,
                blocks=getattr(self.context, "blocks", {}),
                blocks_layout=getattr(self.context, "blocks_layout", {}),
            )
