# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.browser import add
from rer.newsletter import _
from rer.newsletter import logger
from rer.newsletter.adapter.sender import IChannelSender
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from z3c.form import button
from zope.component import getMultiAdapter


class AddForm(add.DefaultAddForm):
    # button handler
    @button.buttonAndHandler("Salva", name="save")
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # validazione dei campi della form
        status = UNHANDLED
        obj = self.createAndAdd(data)
        if obj:
            self._finishedAdd = True
            # chiamo l'utility per la creazione anche il channel
            channel = getMultiAdapter((obj, self.request), IChannelSender)
            status = channel.addChannel()

            if status == OK:
                api.portal.show_message(
                    message=_("add_channel", default="Channel Created"),
                    request=self.request,
                    type="info",
                )

        if not obj or status != OK:
            logger.exception(
                _(
                    "generic_problem_add_channel",
                    default="Unhandled problem with add of channel.",
                )
            )
            status = "Problems...{status}".format(status=status)
            api.portal.show_message(message=status, request=self.request, type="error")


class AddView(add.DefaultAddView):
    form = AddForm
