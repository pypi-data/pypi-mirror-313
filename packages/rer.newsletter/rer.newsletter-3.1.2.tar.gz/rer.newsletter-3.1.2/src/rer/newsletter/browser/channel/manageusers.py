# -*- coding: utf-8 -*-
from Products.CMFPlone.resources import add_bundle_on_request
from Products.Five import BrowserView
from rer.newsletter import logger
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface

import csv
import json


try:
    from StringIO import StringIO
except ImportError:
    # python 3
    from io import StringIO


class IManageUsers(Interface):
    pass


@implementer(IManageUsers)
class ManageUsers(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

        add_bundle_on_request(self.request, "datatables")

    def deleteUser(self):
        status = UNHANDLED

        email = self.request["email"]

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)
        status = channel.deleteUser(email)

        response = {}
        if status == OK:
            response["ok"] = True
        else:
            response["ok"] = False
            logger.exception(
                "Error: {error} - channel: {channel} - email: {email}".format(
                    error=status, channel=channel, email=email
                )
            )

        return json.dumps(response)

    def exportUsersListAsFile(self):
        status = UNHANDLED
        channel = self.context.id_channel

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)
        userList, status = channel.exportUsersList()

        if status == OK:
            # predisporre download del file
            data = StringIO()
            fieldnames = ["id", "email", "is_active", "creation_date"]
            writer = csv.DictWriter(data, fieldnames=fieldnames)

            writer.writeheader()

            userListJson = json.loads(userList)
            for user in userListJson:
                writer.writerow(user)

            filename = "{title}-user-list.csv".format(title=self.context.id)

            self.request.response.setHeader("Content-Type", "text/csv")
            self.request.response.setHeader(
                "Content-Disposition",
                'attachment; filename="{filename}"'.format(filename=filename),
            )

            return data.getvalue()

        else:
            logger.exception(
                "Problems: {error} - channel: {channel}".format(
                    error=status, channel=channel
                )
            )

    def exportUsersListAsJson(self):
        status = UNHANDLED
        channel = self.context.id_channel

        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)
        userList, status = channel.exportUsersList()

        if status == OK:
            return json.dumps(userList)
        else:
            logger.exception(
                "Error: {error} - channel: {channel}".format(
                    error=self.errors, channel=channel
                )
            )
