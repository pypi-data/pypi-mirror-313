# -*- coding: utf-8 -*-
from plone.batching.browser import PloneBatchView


class ShippableCollectionBatchView(PloneBatchView):
    def __call__(self, batch, batchformkeys=None, minimal_navigation=False):
        """Non voglio il batch per questo tipo di collezioni"""

        return ""
