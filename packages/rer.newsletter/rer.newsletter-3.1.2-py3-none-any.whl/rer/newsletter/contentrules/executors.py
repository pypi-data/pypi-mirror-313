# -*- coding: utf-8 -*-
from .interfaces import INotifyOnSubscribe
from .interfaces import INotifyOnUnsubscribe
from plone import api
from plone.contentrules.rule.interfaces import IExecutable
from rer.newsletter.utils import get_site_title
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExecutable)
class NotifyExecutor(object):
    def send_email(self):
        mail_host = api.portal.get_tool(name="MailHost")
        mail_host.send(
            self.element.message,
            mto=self.element.dest_addr,
            mfrom=self.element.source,
            subject=self.element.subject,
            charset="utf-8",
            msg_type="text/html",
        )

    def text_compile(self):
        sub_strings = {
            "channel": ["${channel}", self.event.object.title],
            "url": ["${url}", self.event.object.absolute_url()],
            "portal": ["${portal}", get_site_title()],
            "subscribe": ["${subscribe}", self.event.user],
        }

        for text in ["message", "subject"]:
            for key in sub_strings.keys():
                setattr(
                    self.element,
                    text,
                    getattr(self.element, text).replace(
                        sub_strings[key][0], sub_strings[key][1]
                    ),
                )  # noqa


@adapter(Interface, INotifyOnSubscribe, Interface)
class NotifyOnSubscribeExecutor(NotifyExecutor):
    def __init__(self, context, element, event):
        self.contex = context
        self.element = element
        self.event = event

    def __call__(self):
        """executor code"""
        self.text_compile()
        self.send_email()


@adapter(Interface, INotifyOnUnsubscribe, Interface)
class NotifyOnUnsubscribeExecutor(NotifyExecutor):
    def __init__(self, context, element, event):
        self.contex = context
        self.element = element
        self.event = event

    def __call__(self):
        """executor code"""
        self.text_compile()
        self.send_email()
