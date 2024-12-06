# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets import ViewletBase


class ChannelManagerViewlet(ViewletBase):
    def update(self):
        pass

    def canManageNewsletter(self):
        return api.user.get_permissions(obj=self.context).get(
            "rer.newsletter: Manage Newsletter"
        )

    def render(self):
        return self.index()
