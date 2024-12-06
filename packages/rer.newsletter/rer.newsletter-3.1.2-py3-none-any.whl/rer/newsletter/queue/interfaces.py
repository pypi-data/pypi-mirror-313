# -*- coding: utf-8 -*-
# from collections import namedtuple
from zope.interface import Interface


# expected types: sent=int, total=int, start=datetime
# Progress = namedtuple('Progress', ['sent', 'total', 'start'])


class IMessageQueue(Interface):
    """Queues message into a queue"""

    def start(message):
        """Queues an IMessage for sendout"""
