# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.batching import HypermediaBatch
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from rer.newsletter import _
from rer.newsletter.adapter.subscriptions import IChannelSubscriptions
from rer.newsletter.utils import OK
from rer.newsletter.utils import UNHANDLED
from six import StringIO
from zope.component import getMultiAdapter

import csv


KEY = "rer.newsletter.channel.history"


class SubscriptionsGet(Service):
    def reply(self):
        history = self.get_subscriptions()
        batch = HypermediaBatch(self.request, history)
        data = {
            "@id": batch.canonical_url,
            "items": [self.fix_fields(data=x) for x in batch],
            "items_total": batch.items_total,
        }
        links = batch.links
        if links:
            data["batching"] = links

        return data

    def get_subscriptions(self):
        text = self.request.form.get("text", "")

        status = UNHANDLED
        channel = getMultiAdapter((self.context, self.request), IChannelSubscriptions)
        subscriptions, status = channel.exportUsersList()
        if status != OK:
            msg = api.portal.translate(
                _(
                    "subscriptions_retrieve_error",
                    default="There was an error fetching subscribers.",
                )
            )
            raise Exception(msg)

        res = []
        for item in subscriptions:
            if text and text.lower() not in item.get("email", "").lower():
                continue
            res.append(self.fix_fields(item))
        # revert the list
        return res[::-1]

    def fix_fields(self, data):
        for k, v in data.items():
            data[k] = json_compatible(v)
        return data


class ExportSubscriptionsGet(SubscriptionsGet):
    def render(self):
        # predisporre download del file

        data = self.get_data()
        self.request.response.setHeader("Content-Type", "text/comma-separated-values")
        self.request.response.setHeader(
            "Content-Disposition",
            f'attachment; filename="{self.context.id}-user-list.csv"',
        )

        self.request.response.write(data)

    def get_data(self):
        sbuf = StringIO()
        columns = ["id", "email", "is_active", "creation_date"]
        subscriptions = self.get_subscriptions()

        writer = csv.DictWriter(
            sbuf, fieldnames=columns, delimiter=",", quoting=csv.QUOTE_ALL
        )
        writer.writeheader()
        for row in subscriptions:
            writer.writerow(row)

        res = sbuf.getvalue()
        sbuf.close()

        return res.encode()
