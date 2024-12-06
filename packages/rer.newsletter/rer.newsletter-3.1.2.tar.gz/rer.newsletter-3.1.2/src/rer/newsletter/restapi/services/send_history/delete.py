# -*- coding: utf-8 -*-
from persistent.list import PersistentList
from plone import api
from plone.restapi.services import Service
from rer.newsletter import _
from zExceptions import BadRequest
from zope.annotation.interfaces import IAnnotations


KEY = "rer.newsletter.channel.history"


class SendHistoryDelete(Service):
    def reply(self):
        uids = self.request.get("uids", [])
        if not uids:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "delete_history_missing_parameter",
                        default="You need to select at least one history or all.",
                    )
                )
            )
        annotations = IAnnotations(self.context)
        history = annotations.get(KEY, [])
        if history:
            if uids == "all":
                annotations[KEY] = PersistentList({})
            else:
                if isinstance(uids, str):
                    uids = [uids]
                for i, k in enumerate(history):
                    if k["uid"] in uids:
                        del history[i]
        return self.reply_no_content()
