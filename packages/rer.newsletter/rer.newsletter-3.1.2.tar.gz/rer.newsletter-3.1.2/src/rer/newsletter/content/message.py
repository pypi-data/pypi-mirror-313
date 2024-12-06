# -*- coding: utf-8 -*-
from Acquisition import aq_chain
from plone import api
from plone.app.contenttypes.content import Folder
from plone.app.layout.viewlets.content import ContentHistoryView
from rer.newsletter.adapter.sender import IChannelSender
from rer.newsletter.content.channel import Channel
from rer.newsletter.interfaces import IMessage
from rer.newsletter.utils import compose_sender
from rer.newsletter.utils import get_site_title
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import implementer

import re


try:
    from collective.taskqueue.interfaces import ITaskQueue
    from rer.newsletter.queue.handler import QUEUE_NAME
    from rer.newsletter.queue.interfaces import IMessageQueue

    HAS_TASKQUEUE = True
except ImportError:
    HAS_TASKQUEUE = False


KEY = "rer.newsletter.message.details"


@implementer(IMessage)
class Message(Folder):
    def get_channel(self):
        for parent in aq_chain(self):
            if isinstance(parent, Channel):
                return parent
        return None

    def can_manage_newsletter(self):
        if not self.get_channel():
            return False

        is_editor = "Editor" in api.user.get_roles(obj=self)
        can_manage = api.user.get_permissions(obj=self).get(
            "rer.newsletter: Manage Newsletter"
        ) and "Gestore Newsletter" not in api.user.get_roles(obj=self)
        if is_editor or can_manage:
            return True
        return False

    def can_send_message(self):
        if not self.get_channel():
            return False

        if api.content.get_state(obj=self) != "published":
            return False
        return api.user.get_permissions(obj=self).get("rer.newsletter: Send Newsletter")

    def message_already_sent(self):
        history = ContentHistoryView(self, self.REQUEST).fullHistory()
        if not history:
            return False
        send_history = [x for x in history if x["action"] == "Invio"]
        return len(send_history) > 0

    def active_subscriptions(self):
        channel = self.get_channel()
        if not channel:
            return 0
        return channel.active_subscriptions()

    # send methods
    def send_message(self):
        if HAS_TASKQUEUE:
            message_queue = queryUtility(IMessageQueue)
            is_queue_present = queryUtility(ITaskQueue, name=QUEUE_NAME)
            if is_queue_present is not None and message_queue is not None:
                # se non riesce a connettersi con redis allora si spacca
                message_queue.start(self)
            else:
                # invio sincrono del messaggio
                status = self.send_syncronous()
        else:
            # invio sincrono del messaggio
            status = self.send_syncronous()
        return {"status": status}

    def send_syncronous(self):
        channel = self.get_channel()
        adapter = getMultiAdapter((channel, self.REQUEST), IChannelSender)
        return adapter.sendMessage(message=self)

    def send_preview(self, email):
        emails = re.compile("[,|;]").split(email)
        channel = self.get_channel()
        if not channel:
            # non riesco a recuperare le info di un channel
            return

        body = self.compose_message(channel=channel)

        sender = compose_sender(channel=channel)

        nl_subject = " - " + channel.subject_email if channel.subject_email else ""

        subject = "Messaggio di prova - " + self.title + nl_subject
        # per mandare la mail non passo per l'utility
        # in ogni caso questa mail viene mandata da plone
        mail_host = api.portal.get_tool(name="MailHost")
        for email in emails:
            mail_host.send(
                body.getData(),
                mto=email.strip(),
                mfrom=sender,
                subject=subject,
                charset="utf-8",
                msg_type="text/html",
                immediate=True,
            )

    def compose_message(self, channel):
        unsubscribe_footer_template = self.restrictedTraverse(
            "@@unsubscribe_channel_template"
        )
        parameters = {
            "portal_name": get_site_title(),
            "channel_name": channel.title,
            "unsubscribe_link": channel.absolute_url(),
            "enabled": channel.standard_unsubscribe,
        }

        message_template = self.restrictedTraverse("@@messagepreview_view")
        parameters = {
            "message_subheader": f"""
                <tr>
                    <td align="left" colspan="2">
                      <div class="newsletterTitle">
                        <h1>{self.title}</h1>
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
