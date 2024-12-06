# -*- coding: utf-8 -*-
from datetime import datetime
from persistent.dict import PersistentDict
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from rer.newsletter import logger
from rer.newsletter.adapter.sender import IChannelSender
from rer.newsletter.content.channel import Channel
from rer.newsletter.content.message import Message
from rer.newsletter.utils import addToHistory
from rer.newsletter.utils import get_site_title
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


KEY = "rer.newsletter.message.details"


class ProcessQueue(BrowserView):
    def _sendNotification(self, status, channel, message):
        """send notification to user when asynch call is finished"""
        portal = api.portal.get()
        if channel.sender_email:
            message_template = None
            if status == OK:
                message_template = message.restrictedTraverse(
                    "@@{0}".format("asynch_send_success")
                )
            else:
                message_template = message.restrictedTraverse(
                    "@@{0}".format("asynch_send_fail")
                )
            parameters = {
                "header": channel.header if channel.header else "",
                "footer": channel.footer if channel.footer else "",
                "style": channel.css_style if channel.css_style else "",
                "portal_name": portal.title,
                "channel_name": channel.title,
                "message_title": message.title,
            }
            mail_text = message_template(**parameters)
            mail_text = portal.portal_transforms.convertTo(
                "text/mail", mail_text
            )

            # response_email = None
            # if channel.response_email:
            #     response_email = channel.response_email

            subject = "Risultato invio asincrono di {0} del {1} del ".format(
                message.title, channel.title
            ) + "portale {0}".format(get_site_title())

            mail_host = api.portal.get_tool(name="MailHost")
            mail_host.send(
                mail_text.getData(),
                mto=channel.sender_email,
                mfrom=channel.sender_email,
                subject=subject,
                charset="utf-8",
                msg_type="text/html",
            )
        else:
            logger.exception("Non è stato impostato l'indirizzo del mittente")

    def _getChannel(self):
        channel = None
        for obj in self.aq_chain:
            if isinstance(obj, Channel):
                channel = obj
                break
        else:
            if not channel:
                return
        return channel

    def _getMessage(self):
        message = None
        for obj in self.aq_chain:
            if isinstance(obj, Message):
                message = obj
                break
        else:
            if not message:
                return
        return message

    def __call__(self):
        """asynchronous call"""
        # la disabilito perchè in questa vista ci possono arrivare soltanto i
        # processi asincroni di collective.taskqueue
        alsoProvides(self.request, IDisableCSRFProtection)

        status = UNHANDLED
        message = self._getMessage()
        channel = getMultiAdapter(
            (self._getChannel(), self.request), IChannelSender
        )

        unsubscribe_footer_template = message.restrictedTraverse(
            "@@unsubscribe_channel_template"
        )

        parameters = {
            "portal_name": get_site_title(),
            "channel_name": channel.title,
            "unsubscribe_link": channel.absolute_url(),
        }
        unsubscribe_footer_text = unsubscribe_footer_template(**parameters)
        status = channel.sendMessage(message, unsubscribe_footer_text)

        # i dettagli sull'invio del messaggio per lo storico
        annotations = IAnnotations(message)
        if KEY not in list(annotations.keys()):
            annotations[KEY] = PersistentDict({})

        annotations = annotations[KEY]
        now = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        if status == OK:
            active_users, status = channel.getNumActiveSubscribers()

        if status != OK:
            logger.exception(
                "Problemi con la richiesta: {0}".format(
                    self.request.get("HTTP_X_TASK_ID")
                )
            )
        else:
            annotations[message.title + str(len(list(annotations.keys())))] = {
                "num_active_subscribers": active_users,
                "send_date": now,
            }
            # aggiungo all'history dell'oggetto messaggio il suo invio
            addToHistory(message, active_users)

        self._sendNotification(status=status, channel=channel, message=message)
