# -*- coding: utf-8 -*-
from plone import api
from plone import schema
from plone.protect.authenticator import createToken
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from rer.newsletter import _
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import compose_sender
from rer.newsletter.utils import get_site_title
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from six import PY2
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope.component import getMultiAdapter
from zope.interface import Interface

import logging


logger = logging.getLogger(__name__)


class IUnsubscribeForm(Interface):
    """define field for channel unsubscription"""

    email = schema.Email(
        title=_("unsubscribe_email_title", default="Unsubscription Email"),
        description=_("unsubscribe_email_description", default=""),
        required=True,
    )


class UnsubscribeForm(form.Form):
    ignoreContext = True
    fields = field.Fields(IUnsubscribeForm)

    def isVisible(self):
        if self.context.is_subscribable:
            return True
        else:
            return False

    def getChannelPrivacyPolicy(self):
        return False

    def updateWidgets(self):
        super(UnsubscribeForm, self).updateWidgets()
        if self.request.get("email", None):
            self.widgets["email"].value = self.request.get("email")

    @button.buttonAndHandler(_("unsubscribe_button", default="Unsubscribe"))
    def handleSave(self, action):
        status = UNHANDLED
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        email = data.get("email", None)

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)

        status, secret = channel.unsubscribe(email)

        if status != OK:
            logger.exception("Error: {}".format(status))
            if status == 4:
                msg = _(
                    "unsubscribe_inexistent_mail",
                    default="Mail not found. Unable to unsubscribe.",
                )
            else:
                msg = _(
                    "unsubscribe_generic",
                    default="Unable to perform unsubscription. Please contact site administrators.",  # noqa
                )
            api.portal.show_message(message=msg, request=self.request, type="error")
            return

        # creo il token CSRF
        token = createToken()

        # mando mail di conferma
        url = self.context.absolute_url()
        url += "/confirm-subscription?secret=" + secret
        url += "&_authenticator=" + token
        url += "&action=unsubscribe"

        mail_template = self.context.restrictedTraverse("@@deleteuser_template")

        parameters = {
            "header": self.context.header,
            "footer": self.context.footer,
            "style": self.context.css_style,
            "activationUrl": url,
        }

        mail_text = mail_template(**parameters)

        portal = api.portal.get()
        mail_text = portal.portal_transforms.convertTo("text/mail", mail_text)

        response_email = compose_sender(channel=self.context)
        channel_title = self.context.title
        if PY2:
            channel_title = self.context.title.encode("utf-8")

        mailHost = api.portal.get_tool(name="MailHost")
        mailHost.send(
            mail_text.getData(),
            mto=email,
            mfrom=response_email,
            subject="Conferma la cancellazione dalla newsletter"
            " {channel} del portale {site}".format(
                channel=channel_title, site=get_site_title()
            ),
            charset="utf-8",
            msg_type="text/html",
            immediate=True,
        )

        api.portal.show_message(
            message=_(
                "user_unsubscribe_success",
                default="Riceverai una e-mail per confermare"
                " la cancellazione dalla newsletter",
            ),
            request=self.request,
            type="info",
        )


unsubscribe_view = wrap_form(
    UnsubscribeForm,
    index=ViewPageTemplateFile("templates/unsubscribechannel.pt"),
)
