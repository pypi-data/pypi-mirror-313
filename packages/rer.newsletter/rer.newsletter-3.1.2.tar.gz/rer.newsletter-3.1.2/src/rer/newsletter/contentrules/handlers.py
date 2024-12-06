# -*- coding: utf-8 -*-
from plone.app.contentrules.handlers import execute


def subscribeNotification(event):
    execute(event.object, event)


def unsubscribeNotification(event):
    execute(event.object, event)
