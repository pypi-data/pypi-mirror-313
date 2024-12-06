# -*- coding: utf-8 -*-
from plone.restapi.batching import HypermediaBatch
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.annotation.interfaces import IAnnotations


KEY = "rer.newsletter.channel.history"


class SendHistoryGet(Service):
    def reply(self):
        history = self.get_history()
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

    def get_history(self):
        text = self.request.form.get("text", "")

        annotations = IAnnotations(self.context)
        history = []
        for item in annotations.get(KEY, []):
            if text and text.lower() not in item.get("message", "").lower():
                continue
            history.append(self.fix_fields(item.data))
        # revert the list
        return history[::-1]

    def fix_fields(self, data):
        for k, v in data.items():
            data[k] = json_compatible(v)
        return data
