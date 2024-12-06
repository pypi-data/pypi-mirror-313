# -*- coding: utf-8 -*-
from plone import api
from plone.namedfile.field import NamedBlobFile
from rer.newsletter import _
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from six import PY2
from six.moves import range
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import Interface

import csv
import re


try:
    from StringIO import StringIO
except ImportError:
    # python 3
    from io import StringIO


def check_separator(value):
    match = re.match("^,|^;", value)
    if match:
        return True
    else:
        return False


class IUsersImport(Interface):
    userListFile = NamedBlobFile(
        title=_("title_users_list_file", default="Users List File"),
        description=_("description_file", default="File must be a CSV"),
        required=True,
    )

    # se questo e ceccato allora i dati non vengono inseriti
    emptyList = schema.Bool(
        title=_("title_empty_list", default="Empties users list"),
        description=_("description_empty_list", default="Empties channel users list"),
        required=False,
    )

    # se e ceccato sia questo dato che 'emptyList'
    # allora do precedenza a emptyList
    removeSubscribers = schema.Bool(
        title=_(
            "title_remove_subscribers",
            default="Remove subscribers of the list",
        ),
        description=_(
            "description_remove_subscribers",
            default="Remove users of CSV from channel",
        ),
        required=False,
    )

    headerLine = schema.Bool(
        title=_("title_header_line", default="Header Line"),
        description=_(
            "description_header_line",
            default=_("if CSV File contains a header line"),
        ),
        required=False,
    )

    separator = schema.TextLine(
        title=_("title_separator", default="CSV separator"),
        description=_("description_separator", default=_("Separator of CSV file")),
        default=",",
        required=True,
        constraint=check_separator,
    )


def _mailValidation(mail):
    reg_tool = api.portal.get_tool(name="portal_registration")
    return reg_tool.isValidEmail(mail)


class UsersImport(form.Form):
    ignoreContext = True
    fields = field.Fields(IUsersImport)

    def processCSV(self, data, headerline, separator):
        try:
            input_data = data.decode()
        except UnicodeDecodeError:
            input_data = data.decode("utf-8")
        input_separator = separator.encode("ascii", "ignore").decode()
        if PY2:
            input_data = data
            input_separator = separator.encode("ascii", "ignore")

        io = StringIO(input_data)

        reader = csv.reader(
            io, delimiter=input_separator, dialect="excel", quotechar="'"
        )
        index = 1
        if headerline:
            header = next(reader)

            # leggo solo la colonna della email
            index = None
            for i in range(0, len(header)):
                header_value = header[i]
                if PY2:
                    header_value = header[i].decode("utf-8-sig")

                if header_value == "email":
                    index = i
            if index is None:
                api.portal.show_message(
                    message="Il CSV non ha la colonna email oppure il "
                    "separatore potrebbe non essere corretto",
                    request=self.request,
                    type="error",
                )

        if index is not None:
            usersList = []
            line_number = 0
            for row in reader:
                line_number += 1
                row_value = row[index]
                if PY2:
                    row_value = row[index].decode("utf-8-sig")

                mail = row_value
                if _mailValidation(mail):
                    usersList.append(row_value)

            return usersList

    @button.buttonAndHandler(_("charge_userimport", default="Import"))
    def handleSave(self, action):
        status = UNHANDLED
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)

        # devo svuotare la lista di utenti del channel
        if data["emptyList"]:
            status = channel.emptyChannelUsersList()

        csv_file = data["userListFile"].data
        # esporto la lista di utenti dal file
        try:
            usersList = self.processCSV(csv_file, data["headerLine"], data["separator"])
        except IndexError:
            api.portal.show_message(
                message=_(
                    "import_error_index",
                    default="Error parsing CSV file. Probably it has a "
                    "different separator.",
                ),
                request=self.request,
                type="error",
            )
            return

        # controllo se devo eliminare l'intera lista di utenti
        # invece di importarla
        if data["removeSubscribers"] and not data["emptyList"]:
            # chiamo l'api per rimuovere l'intera lista di utenti
            if usersList:
                status = channel.deleteUserList(usersList)

        else:
            if usersList:
                # mi connetto con le api di mailman
                status = channel.importUsersList(usersList)

        if status == OK:
            status = _(
                "generic_subscribe_message_success",
                default="User Subscribed",
            )
            api.portal.show_message(message=status, request=self.request, type="info")
