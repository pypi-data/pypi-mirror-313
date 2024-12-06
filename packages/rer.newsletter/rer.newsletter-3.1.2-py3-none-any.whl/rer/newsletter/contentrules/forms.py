# -*- coding: utf-8 -*-
from .actions import NotifyOnSubscribeAction
from .actions import NotifyOnUnsubscribeAction
from .interfaces import INotifyOnSubscribe
from .interfaces import INotifyOnUnsubscribe
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from rer.newsletter import _


# Subscribe


class NotificationOnSubscribeAddForm(ActionAddForm):
    """An add form for the mail group action"""

    schema = INotifyOnSubscribe
    label = _("Add Rule for newsletter's subscribe")
    form_name = _("Configure element")
    Type = NotifyOnSubscribeAction


class NotificationOnSubscribeAddFormView(ContentRuleFormWrapper):
    form = NotificationOnSubscribeAddForm


class NotificationOnSubscribeEditForm(ActionEditForm):
    """An edit form for the mail group action"""

    schema = INotifyOnSubscribe
    label = _("Edit Rule for newsletter's subscribe")
    form_name = _("Configure element")


class NotificationOnsubscribeEditFormView(ContentRuleFormWrapper):
    form = NotificationOnSubscribeEditForm


# Unsubscribe


class NotificationOnUnsubscribeAddForm(ActionAddForm):
    """An add form for the mail group action"""

    schema = INotifyOnUnsubscribe
    label = _("Add Rule for newsletter's unsubscribe")
    form_name = _("Configure element")
    Type = NotifyOnUnsubscribeAction


class NotificationOnUnsubscribeAddFormView(ContentRuleFormWrapper):
    form = NotificationOnUnsubscribeAddForm


class NotificationOnUnsubscribeEditForm(ActionEditForm):
    """An edit form for the mail group action"""

    schema = INotifyOnUnsubscribe
    label = _("Edit Rule for newsletter's subscribe")
    form_name = _("Configure element")


class NotificationOnUnsubscribeEditFormView(ContentRuleFormWrapper):
    form = NotificationOnSubscribeEditForm
