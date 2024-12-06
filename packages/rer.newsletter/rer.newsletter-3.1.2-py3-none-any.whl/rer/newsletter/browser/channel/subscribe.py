# -*- coding: utf-8 -*-
from plone import api
from plone import schema
from plone.autoform.form import AutoExtensibleForm
from plone.protect.authenticator import createToken
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from rer.newsletter import _
from rer.newsletter import logger
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import compose_sender
from rer.newsletter.utils import get_site_title
from rer.newsletter.utils import SUBSCRIBED
from rer.newsletter.utils import UNHANDLED
from six import PY2
from z3c.form import button
from z3c.form import form
from zope.component import getMultiAdapter
from zope.interface import Interface


class ISubscribeForm(Interface):
    """define field for channel subscription"""

    email = schema.Email(
        title=_("subscribe_user", default="Subscription Mail"),
        description=_(
            "subscribe_user_description",
            default="Mail for subscribe to a channel",
        ),
        required=True,
    )


class SubscribeForm(AutoExtensibleForm, form.Form):
    ignoreContext = True
    schema = ISubscribeForm

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def isVisible(self):
        if self.context.is_subscribable:
            return True
        else:
            return False

    def getChannelPrivacyPolicy(self):
        if self.context.privacy:
            return self.context.privacy.output

    def update(self):
        super(SubscribeForm, self).update()

    @button.buttonAndHandler(_("subscribe_submit_label", default="Subscribe"))
    def handleSave(self, action):
        status = UNHANDLED
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            if self.status:
                self.status = (
                    "Indirizzo email non inserito o non "
                    + "valido, oppure controllo di sicurezza non "  # noqa
                    + "inserito."  # noqa
                )
            return

        email = data.get("email", "").lower()

        if self.context.is_subscribable:
            channel = getMultiAdapter(
                (self.context, self.request), IChannelSubscriptions
            )
            status, secret = channel.subscribe(email)

        if status == SUBSCRIBED:
            # creo il token CSRF
            token = createToken()

            # mando mail di conferma
            url = self.context.absolute_url()
            url += "/confirm-subscription?secret=" + secret
            url += "&_authenticator=" + token
            url += "&action=subscribe"

            mail_template = self.context.restrictedTraverse("@@activeuser_template")

            parameters = {
                "title": self.context.title,
                "header": self.context.header,
                "footer": self.context.footer,
                "style": self.context.css_style,
                "activationUrl": url,
                "portal_name": get_site_title(),
            }

            mail_text = mail_template(**parameters)

            portal = api.portal.get()
            mail_text = portal.portal_transforms.convertTo("text/mail", mail_text)
            sender = compose_sender(channel=self.context)

            channel_title = self.context.title
            if PY2:
                channel_title = self.context.title.encode("utf-8")

            mailHost = api.portal.get_tool(name="MailHost")
            mailHost.send(
                mail_text.getData(),
                mto=email,
                mfrom=sender,
                subject="Conferma la tua iscrizione alla Newsletter {channel}"
                " del portale {site}".format(
                    channel=channel_title, site=get_site_title()
                ),
                charset="utf-8",
                msg_type="text/html",
                immediate=True,
            )

            api.portal.show_message(
                message=_(
                    "status_user_subscribed",
                    default="Riceverai una e-mail per confermare "
                    "l'iscrizione alla newsletter.",
                ),
                request=self.request,
                type="info",
            )

        else:
            if status == 2:
                logger.exception("user already subscribed")
                api.portal.show_message(
                    message=_(
                        "user_already_subscribed",
                        default="Sei già iscritto a questa newsletter, "
                        "oppure non hai ancora"
                        " confermato l'iscrizione.",
                    ),
                    request=self.request,
                    type="error",
                )
            else:
                logger.exception("unhandled error subscribe user")
                api.portal.show_message(
                    message="Problems...{0}".format(status),
                    request=self.request,
                    type="error",
                )


subscribe_view = wrap_form(
    SubscribeForm, index=ViewPageTemplateFile("templates/subscribechannel.pt")
)
