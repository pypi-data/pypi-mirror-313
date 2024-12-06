# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView


class ChannelView(BrowserView):
    def getState(self, message):
        stateDict = {
            "draft": "bozza",
            "review": "in attesa di invio",
            "sent": "inviato",
        }
        return stateDict[api.content.get_state(obj=message)]

    def getMessageList(self):
        if self.context.portal_type == "Channel":
            brainsList = api.content.find(context=self.context, portal_type="Message")

            messageList = []
            for brain in brainsList:
                messageList.append(brain.getObject())

            return messageList
