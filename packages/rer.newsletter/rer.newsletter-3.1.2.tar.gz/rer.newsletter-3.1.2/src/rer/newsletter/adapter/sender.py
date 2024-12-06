# -*- coding: utf-8 -*-
from datetime import datetime
from DateTime import DateTime
from email.utils import formataddr
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from plone import api
from rer.newsletter import logger
from rer.newsletter.utils import get_site_title
from rer.newsletter.utils import OK
from rer.newsletter.utils import SEND_UID_NOT_FOUND
from rer.newsletter.utils import UNHANDLED
from smtplib import SMTPRecipientsRefused
from transaction import commit
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import Interface


SUBSCRIBERS_KEY = "rer.newsletter.subscribers"
HISTORY_KEY = "rer.newsletter.channel.history"


class IChannelSender(Interface):
    """Marker interface to provide a Channel message sender"""


@implementer(IChannelSender)
class BaseAdapter(object):
    """Adapter standard di base, invio sincrono usando plone"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    #  utils methods

    def get_annotations_for_channel(self, key):
        annotations = IAnnotations(self.context)
        if key not in list(annotations.keys()):
            if key == HISTORY_KEY:
                annotations[key] = PersistentList({})
            else:
                annotations[key] = PersistentDict({})
        return annotations[key]

    @property
    def active_subscriptions(self):
        subscribers = self.get_annotations_for_channel(key=SUBSCRIBERS_KEY)
        return len([x for x in subscribers.values() if x["is_active"]])

    @property
    def channel_history(self):
        return self.get_annotations_for_channel(key=HISTORY_KEY)

    #  utils methods end

    def addChannel(self):
        logger.info("DEBUG: add channel {0}".format(self.context.title))
        return OK

    def _getDate(self):
        # this would be good but it doesn't work, locale not supported
        # try:
        #     locale.setlocale(locale.LC_ALL, 'it_IT.utf8')
        # except Exception:
        #     try:
        #         locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')
        #     except Exception:
        #         locale.setlocale(locale.LC_ALL, 'it_IT')
        return datetime.today().strftime("Newsletter %d-%m-%Y")

    def _getMessage(self, message, footer):
        logger.debug("getMessage %s %s", self.context.title, message.title)
        message_template = message.restrictedTraverse("@@messagepreview_view")
        parameters = {
            "message_subheader": f"""
                <tr>
                    <td align="left" colspan="2">
                      <div class="newsletterTitle">
                        <h1>{message.title}</h1>
                      </div>
                    </td>
                </tr>""",
            "message_unsubscribe_default": footer,
        }

        body = message_template(**parameters)

        # passo la mail per il transform
        portal = api.portal.get()
        body = portal.portal_transforms.convertTo("text/mail", body)

        return body

    def set_start_send_infos(self, message):
        details = self.get_annotations_for_channel(key=HISTORY_KEY)

        now = datetime.today()

        uid = "{time}-{id}".format(
            time=now.strftime("%Y%m%d%H%M%S"), id=message.getId()
        )
        details.append(
            PersistentDict(
                {
                    "uid": uid,
                    "message": message.title,
                    "subscribers": self.active_subscriptions,
                    "send_date_start": now.strftime("%d/%m/%Y %H:%M:%S"),
                    "send_date_end": "---",
                    "completed": False,
                    "running": True,
                }
            )
        )
        self.addToHistory(message)
        # commit transaction, to see the history updated
        commit()
        return uid

    def set_end_send_infos(self, send_uid, completed=True):
        details = self.get_annotations_for_channel(key=HISTORY_KEY)
        send_info = [x for x in details if x["uid"] == send_uid]
        if not send_info:
            return SEND_UID_NOT_FOUND
        send_info[0]["send_date_end"] = datetime.today().strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        send_info[0]["completed"] = completed
        send_info[0]["running"] = False
        return OK

    def prepare_body(self, message):
        # unsubscribe_footer_template = self.context.restrictedTraverse(
        #     "@@unsubscribe_channel_template"
        # )
        # parameters = {
        #     "portal_name": get_site_title(),
        #     "channel_name": self.context.title,
        #     "unsubscribe_link": self.context.absolute_url(),
        #     "enabled": self.context.standard_unsubscribe,
        # }
        # footer = unsubscribe_footer_template(**parameters)
        # return self._getMessage(message=message, footer=footer)
        unsubscribe_footer_template = api.content.get_view(
            name="unsubscribe_channel_template",
            context=self.context,
            request=self.request,
        )
        parameters = {
            "portal_name": get_site_title(),
            "channel_name": self.context.title,
            "unsubscribe_link": self.context.absolute_url(),
            "enabled": self.context.standard_unsubscribe,
        }

        message_template = api.content.get_view(
            context=message, name="messagepreview_view", request=self.request
        )
        parameters = {
            "message_subheader": f"""
                <tr>
                    <td align="left" colspan="2">
                      <div class="newsletterTitle">
                        <h1>{message.title}</h1>
                      </div>
                    </td>
                </tr>""",
            "message_unsubscribe_default": f"""
                <tr>
                    <td align="left" colspan="2">
                    <div class="newsletter-unsubscribe">
                        {unsubscribe_footer_template(**parameters)}
                    </div>
                    </td>
                </tr>
            """,
        }

        body = message_template(**parameters)
        # passo la mail per il transform
        portal = api.portal.get()
        body = portal.portal_transforms.convertTo("text/mail", body)

        return body

    def sendMessage(self, message):
        """This is the primary method to send emails for the channel."""
        logger.debug("sendMessage %s %s", self.context.title, message.title)

        subscribers = self.get_annotations_for_channel(key=SUBSCRIBERS_KEY)

        nl_subject = (
            " - " + self.context.subject_email
            if self.context.subject_email
            else ""
        )
        sender = (
            self.context.sender_name
            and formataddr(  # noqa
                (self.context.sender_name, self.context.sender_email)
            )
            or self.context.sender_email  # noqa
        )
        subject = message.title + nl_subject

        send_uid = self.set_start_send_infos(message=message)
        res = self.doSend(
            body=self.prepare_body(message=message),
            subject=subject,
            subscribers=subscribers,
            sender=sender,
        )
        self.set_end_send_infos(send_uid=send_uid)
        return res

    def doSend(self, body, subject, subscribers, sender):
        """
        Override this method with a new (and more specific) adapter to
        customize the email sending.
        """
        mail_host = api.portal.get_tool(name="MailHost")
        try:
            for subscriber in subscribers.values():
                if subscriber["is_active"]:
                    mail_host.send(
                        body.getData(),
                        mto=subscriber["email"],
                        mfrom=sender,
                        subject=subject,
                        charset="utf-8",
                        msg_type="text/html",
                    )
        except SMTPRecipientsRefused:
            return UNHANDLED

        return OK

    def addToHistory(self, message):
        """Add to history that message is sent"""

        list_history = [
            x for x in message.workflow_history.get("message_workflow")
        ]
        current = api.user.get_current()
        entry = dict(
            action="Invio",
            review_state=api.content.get_state(obj=message),
            actor=current.getId(),
            comments="Inviato il messaggio a {} utenti.".format(
                self.active_subscriptions
            ),
            time=DateTime(),
        )
        list_history.append(entry)
        message.workflow_history["message_workflow"] = tuple(list_history)
