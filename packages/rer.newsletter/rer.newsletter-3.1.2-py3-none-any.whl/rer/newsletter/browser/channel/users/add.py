# -*- coding: utf-8 -*-
from plone import api
from plone import schema
from rer.newsletter import _
from rer.newsletter import logger
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import SUBSCRIBED
from rer.newsletter.utils import UNHANDLED
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope.component import getMultiAdapter
from zope.interface import Interface


class IAddForm(Interface):
    """define field for add user to a channel"""

    email = schema.Email(
        title=_("add_user_admin", default="Add User"),
        description=_(
            "add_user_admin_description",
            default="Insert email for add user to a Channel",
        ),
        required=True,
    )


class AddForm(form.Form):
    ignoreContext = True
    fields = field.Fields(IAddForm)

    @button.buttonAndHandler(_("add_user_admin_button", default="Add"))
    def handleSave(self, action):
        status = UNHANDLED
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        channel = self.context.id_channel
        mail = data["email"]

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)
        status = channel.addUser(mail)

        if status == SUBSCRIBED:
            status = _("generic_add_message_success", default="User Added.")
            api.portal.show_message(message=status, request=self.request, type="info")
        else:
            logger.exception("unhandled error add user")
            api.portal.show_message(
                message="Problems...{0}".format(status),
                request=self.request,
                type="error",
            )
