# -*- coding: utf-8 -*-
from base64 import b64decode
from io import StringIO
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from rer.newsletter import _
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import ALREADY_SUBSCRIBED
from rer.newsletter.utils import INVALID_EMAIL
from rer.newsletter.utils import OK
from rer.newsletter.utils import SUBSCRIBED
from zExceptions import BadRequest
from zope.component import getMultiAdapter

import csv


class AddSubscriptionsPost(Service):
    def reply(self):
        data = json_body(self.request)

        email = data.get("email", "")
        if not email:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "missing_email_label",
                        default="Missing required parameter: email.",
                    )
                )
            )

        channel = getMultiAdapter(
            (self.context, self.request), IChannelSubscriptions
        )
        status = channel.addUser(email)

        if status != SUBSCRIBED:
            if status == ALREADY_SUBSCRIBED:
                raise BadRequest(
                    api.portal.translate(
                        _(
                            "add_subscription_already_subscribed",
                            default="There is already an active subscription for ${email}.",
                            mapping={"email": email},
                        )
                    )
                )
            if status == INVALID_EMAIL:
                raise BadRequest(
                    api.portal.translate(
                        _(
                            "add_subscription_invalid_email",
                            default="Email not valid: ${email}.",
                            mapping={"email": email},
                        )
                    )
                )
            raise BadRequest(
                api.portal.translate(
                    _(
                        "add_subscription_generic_error",
                        default="Error adding ${email}.",
                        mapping={"email": email},
                    )
                )
            )
        return self.reply_no_content()


class ImportSubscriptionsPost(Service):
    def reply(self):
        data = json_body(self.request)
        self.validate_form(data)

        channel = getMultiAdapter(
            (self.context, self.request), IChannelSubscriptions
        )
        remove_from_list = data.get("remove_from_list", False)
        reset_list = data.get("reset_list", False)

        subscriptions = self.extract_subscriptions(data)

        # devo svuotare la lista di utenti del channel
        if reset_list and not remove_from_list:
            channel.emptyChannelUsersList()

        if remove_from_list:
            status = channel.deleteUserList(subscriptions)
        else:
            status = channel.importUsersList(subscriptions)

        if status != OK:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "import_subscriptions_generic_error",
                        default="Error importing subscriptions.",
                    )
                )
            )
        return self.reply_no_content()

    def validate_form(self, data):
        file = data.get("file", "")
        if not file:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "missing_file_label",
                        default="Missing required parameter: file.",
                    )
                )
            )

    def extract_subscriptions(self, data):
        file_data = data.get("file", "")
        csv_separator = data.get("csv_separator", ",")
        has_header = data.get("has_header", False)

        data_type, encoded_data = file_data.split(";base64,")
        csv_text = b64decode(encoded_data)
        csv_file = StringIO(csv_text.decode("utf-8"))
        reg_tool = api.portal.get_tool(name="portal_registration")

        reader = csv.reader(
            csv_file, delimiter=csv_separator, dialect="excel", quotechar='"'
        )
        index = 1
        if has_header:
            header = next(reader)

            # leggo solo la colonna della email
            index = None
            for i, v in enumerate(header):
                if v == "email":
                    index = i
                    break
        if not index:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "import_subscriptions_invalid_header",
                        default='Uploaded file does not have "email" column.',
                    )
                )
            )

        subscriptions = []
        for row in reader:
            mail = row[index]
            if reg_tool.isValidEmail(mail):
                subscriptions.append(mail)

        return subscriptions
