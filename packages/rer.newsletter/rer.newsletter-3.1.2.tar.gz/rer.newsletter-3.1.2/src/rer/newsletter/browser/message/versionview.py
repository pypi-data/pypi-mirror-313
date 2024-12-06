# -*- coding: utf-8 -*-
from plone.app.versioningbehavior.browser import VersionView
from zope.component import getMultiAdapter


class MessageVersionView(VersionView):
    def __call__(self):
        version_id = self.request.get("version_id", None)
        if not version_id:
            raise ValueError("Missing parameter on the request: version_id")

        content_core_view = getMultiAdapter(
            (self.context, self.request), name="content-core"
        )
        html = content_core_view()
        return self._convert_download_links(html, version_id)
