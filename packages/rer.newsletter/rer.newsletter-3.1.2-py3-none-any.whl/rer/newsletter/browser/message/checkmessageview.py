# -*- coding: utf-8 -*-
# from .sendmessageview import KEY
# from rer.newsletter.content.message import Message
# from zope.annotation.interfaces import IAnnotations
from Products.Five.browser import BrowserView


class CheckMessage(BrowserView):
    def __call__(self):
        # for obj in self.aq_chain:
        #     if isinstance(obj, Message):
        #         annotations = IAnnotations(obj)
        #         if KEY in annotations.keys():
        #             return True
        # return False
        return True
