# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from plone import schema
from plone.app.contenttypes.interfaces import ICollection
from plone.namedfile import field as namedfile
from plone.supermodel import model
from rer.newsletter import _
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import six
import uuid


def default_id_channel():
    return six.text_type(uuid.uuid4())


class IShippableCollection(ICollection):
    pass


class IRerNewsletterLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IChannel(Interface):
    """Marker interface that define a channel of newsletter"""


class IChannelSchema(model.Schema):
    """a dexterity schema for channel of newsletter"""

    sender_name = schema.TextLine(
        title=_("sender_name", default="Sender Fullname"),
        description=_("description_sender_name", default="Fullname of sender"),
        required=False,
    )

    sender_email = schema.Email(
        title=_("sender_email", default="Sender email"),
        description=_("description_sender_email", default="Email of sender"),
        required=True,
    )

    subject_email = schema.TextLine(
        title=_("subject_email", default="Subject email"),
        description=_(
            "description_subject_mail", default="Subject for channel message"
        ),
        required=False,
    )

    response_email = schema.Email(
        title=_("response_email", default="Response email"),
        description=_(
            "description_response_email", default="Response email of channel"
        ),
        required=False,
    )

    privacy = BlocksField(
        title=_("privacy_channel", default="Informativa sulla privacy"),
        description=_(
            "description_privacy_channel",
            default="Informativa sulla privacy per questo canale",
        ),
        required=True,
    )

    header = schema.Text(
        title=_("header_channel", default="Header of message"),
        description=_(
            "description_header_channel",
            default="Header for message of this channel",
        ),
        required=False,
    )

    footer = schema.Text(
        title=_("footer_channel", default="Footer of message"),
        description=_(
            "description_footer_channel",
            default="Footer for message of this channel",
        ),
        required=False,
    )

    css_style = schema.Text(
        title=_("css_style", default="CSS Style"),
        description=_("description_css_style", default="style for mail"),
        required=False,
        default="",
    )

    # probabilemente un campo che va nascosto
    id_channel = schema.TextLine(
        title=_("idChannel", default="Channel ID"),
        description=_("description_IDChannel", default="Channel ID"),
        required=True,
        defaultFactory=default_id_channel,
    )

    is_subscribable = schema.Bool(
        title=_("is_subscribable", default="Is Subscribable"),
        default=False,
        required=False,
    )
    standard_unsubscribe = schema.Bool(
        title=_("standard_unsubscribe", default="Standard unsubscribe link"),
        description=_(
            "descriptin_standard_unsubscribe",
            default="Se selezionato, verrà usato un testo standard nelle mail, per la disiscrizione. In alternativa, andrà messo a mano nella configurazione del footer.",
        ),
        default=True,
        required=False,
    )

    logo_header_mail = namedfile.NamedBlobImage(
        title=_("logo_header_mail", default="Logo per l'header delle e-mail"),
        description=_(
            "description_logo_header_mail",
            default="Aggiungi il logo da inserire nell'header della mail, "
            "copia il link e inseriscilo a mano nel campo HTML "
            "dell'header",
        ),
        required=False,
    )

    logo_footer_mail = namedfile.NamedBlobImage(
        title=_("logo_footer_mail", default="Logo per il footer delle e-mail"),
        description=_(
            "description_logo_footer_mail",
            default="Aggiungi il logo da inserire nel footer della mail, "
            "copia il link e inseriscilo a mano nel campo HTML "
            "del footer",
        ),
        required=False,
    )


class IMessage(Interface):
    """Marker interface that define a message"""


class IMessageSchema(model.Schema):
    """a dexterity schema for message"""


class IBlocksToHtml(Interface):
    """
    Utility that converts blocks to html
    """
