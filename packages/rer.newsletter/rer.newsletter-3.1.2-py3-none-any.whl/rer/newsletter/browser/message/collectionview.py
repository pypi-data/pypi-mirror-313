# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.app.contenttypes.browser.collection import CollectionView as View


class CollectionView(View):
    def item_has_image(self, item):
        obj = aq_base(item)
        if obj.image:
            return True
        return False

    def item_has_preview_image(self, item):
        obj = aq_base(item)
        if obj.preview_image:
            return True
        return False
