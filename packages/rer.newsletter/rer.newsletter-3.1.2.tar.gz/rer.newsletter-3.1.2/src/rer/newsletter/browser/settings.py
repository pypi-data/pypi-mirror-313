# -*- coding: utf-8 -*-
from plone import schema
from plone.app.registry.browser import controlpanel
from rer.newsletter import _
from zope.interface import Interface


def checkExpiredTimeToken(value):
    if value > 0:
        return True


class ISettingsSchema(Interface):
    """Schema for channel settings"""

    source_link = schema.TextLine(
        title=_("source_link", default="Link sorgente"),
        description=_("description_source_link", default="Indirizzo da sostituire"),
        default="",
        required=False,
    )

    destination_link = schema.TextLine(
        title=_("destination_link", default="Link di destinazione"),
        description=_(
            "description_destination_link",
            default="Indirizzo da sostituire. Se plone.volto è installato e il frontend_domain configurato, questo valore è ignorato.",
        ),
        required=False,
    )

    expired_time_token = schema.Int(
        title=_("expired_time_token", default="Validità del token in ore"),
        required=False,
        default=48,
        # constraint=checkExpiredTimeToken,
    )


class ChannelSettings(controlpanel.RegistryEditForm):
    schema = ISettingsSchema
    id = "ChannelSettings"
    label = _("channel_setting", default="Channel Settings")

    def updateFields(self):
        super(ChannelSettings, self).updateFields()

    def updateWidgets(self):
        super(ChannelSettings, self).updateWidgets()


class ChannelSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ChannelSettings
