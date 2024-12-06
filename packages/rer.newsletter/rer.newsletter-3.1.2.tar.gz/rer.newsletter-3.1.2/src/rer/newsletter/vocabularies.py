# -*- coding: utf-8 -*-
from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class SubscribableNewsletter(object):
    """
    Torna la lista di canali attivi
    """

    def __call__(self, context):
        brains = api.content.find(portal_type="Channel")

        newsletter_list = []
        for brain in brains:
            obj = brain.getObject()
            if obj.is_subscribable:
                newsletter_list.append(obj)

        terms = [
            SimpleTerm(value=x.UID(), token=x.UID(), title=x.title)
            for x in newsletter_list
        ]

        return SimpleVocabulary(terms)


SubscribableNewsletterVocabulary = SubscribableNewsletter()
