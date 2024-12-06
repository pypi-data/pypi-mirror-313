# -*- coding: utf-8 -*-
from datetime import datetime
from plone import api
from plone import schema
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from rer.newsletter import _
from smtplib import SMTPRecipientsRefused
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope.interface import Interface


class IMessageSendingTest(Interface):
    """define field for sending test of message"""

    email = schema.Email(
        title=_("Email", default="Email"),
        description=_(
            "email_sendingtest_description",
            default="Email to send the test message",
        ),
        required=True,
    )


class MessageSendingTest(form.Form):
    ignoreContext = True
    fields = field.Fields(IMessageSendingTest)

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

    @button.buttonAndHandler(_("send_sendingtest", default="Send"))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        try:
            # prendo l'email dai parametri
            self.context.send_preview(email=data["email"])

        except SMTPRecipientsRefused:
            self.errors = "problemi con l'invio del messaggio"

        # da sistemare la gestione degli errori
        if "errors" in list(self.__dict__.keys()):
            api.portal.show_message(
                message=self.errors, request=self.request, type="error"
            )
        else:
            api.portal.show_message(
                message="Messaggio inviato correttamente!",
                request=self.request,
                type="info",
            )


message_sending_test = wrap_form(
    MessageSendingTest, index=ViewPageTemplateFile("templates/sendingtest.pt")
)
