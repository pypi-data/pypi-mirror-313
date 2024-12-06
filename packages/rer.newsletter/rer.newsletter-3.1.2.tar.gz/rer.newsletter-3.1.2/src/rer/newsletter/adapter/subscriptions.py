# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from persistent.dict import PersistentDict
from plone import api
from rer.newsletter import logger
from rer.newsletter.utils import ALREADY_ACTIVE
from rer.newsletter.utils import ALREADY_SUBSCRIBED
from rer.newsletter.utils import INEXISTENT_EMAIL
from rer.newsletter.utils import INVALID_EMAIL
from rer.newsletter.utils import INVALID_SECRET
from rer.newsletter.utils import MAIL_NOT_PRESENT
from rer.newsletter.utils import OK
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer
from zope.interface import Interface

import re
import six
import transaction
import uuid


KEY = "rer.newsletter.subscribers"


def mailValidation(mail):
    reg_tool = api.portal.get_tool(name="portal_registration")
    return reg_tool.isValidEmail(mail)


def uuidValidation(uuid_string):
    try:
        uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True


def isCreationDateExpired(creation_date):
    # settare una data di scadenza di configurazione
    cd_datetime = datetime.strptime(creation_date, "%d/%m/%Y %H:%M:%S")
    t = datetime.today() - cd_datetime
    if t < timedelta(days=2):
        return True
    return False


class IChannelSubscriptions(Interface):
    """Marker interface to provide a Channel subscriptions management"""


@implementer(IChannelSubscriptions)
class BaseAdapter(object):
    """Adapter standard di base"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def channel_subscriptions(self):
        annotations = IAnnotations(self.context)
        if KEY not in list(annotations.keys()):
            annotations[KEY] = PersistentDict({})
        return annotations[KEY]

    @property
    def active_subscriptions(self):
        return len([x for x in self.channel_subscriptions.values() if x["is_active"]])

    def subscribe(self, mail):
        subscriptions = self.channel_subscriptions

        if not mailValidation(mail):
            return INVALID_EMAIL, None

        # always store in lowercase
        mail = mail.lower()
        uuid_activation = six.text_type(uuid.uuid4())
        for subscriber in subscriptions.values():
            if (mail == subscriber["email"] and subscriber["is_active"]) or (
                mail == subscriber["email"]
                and not subscriber["is_active"]  # noqa
                and isCreationDateExpired(subscriber["creation_date"])  # noqa
            ):
                return ALREADY_SUBSCRIBED, None
        else:
            subscriptions[mail] = {
                "email": mail,
                "is_active": False,
                "token": uuid_activation,
                "creation_date": datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
            }

            transaction.commit()

        return OK, uuid_activation

    def activateUser(self, secret):
        logger.info("DEBUG: active user in %s", self.context.title)

        subscriptions = self.channel_subscriptions

        # valido il secret
        if not uuidValidation(secret):
            return INVALID_SECRET, None

        # attivo l'utente
        element_id = None
        for key, subscriber in subscriptions.items():
            if subscriber["token"] == secret:
                if subscriber["is_active"]:
                    return ALREADY_ACTIVE, key
                else:
                    element_id = key
                    break

        if element_id is not None:
            # riscrivo l'utente mettendolo a attivo
            subscriptions[element_id] = {
                "email": element_id,
                "is_active": True,
                "token": subscriptions[element_id]["token"],
                "creation_date": subscriptions[element_id]["creation_date"],
            }

            transaction.commit()

            return OK, element_id
        else:
            return INVALID_SECRET, element_id

    def deleteUserWithSecret(self, secret):
        subscriptions = self.channel_subscriptions
        if not uuidValidation(secret):
            return INVALID_SECRET, None
        user_found = False
        # cancello l'utente con il secret
        for key, subscriber in subscriptions.items():
            if subscriber["token"] == six.text_type(secret):
                del subscriptions[key]
                return OK, key

        transaction.commit()

        # caso in cui non trovo l'utente
        if not user_found:
            return INEXISTENT_EMAIL, None
        return INVALID_SECRET, None

    def deleteUser(self, mail=None):
        logger.info("delete user %s from channel %s", mail, self.context.title)
        subscriptions = self.channel_subscriptions

        # cancello l'utente con la mail (Admin)
        if mail not in list(subscriptions.keys()):
            return MAIL_NOT_PRESENT

        del subscriptions[mail]
        transaction.commit()

        return OK

    def deleteAllUsers(self):
        logger.info("delete all users from channel %s", self.context.title)
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict({})
        transaction.commit()

        return OK

    def addUser(self, mail):
        logger.info("DEBUG: add user: %s %s", self.context.title, mail)
        subscriptions = self.channel_subscriptions

        if not mailValidation(mail):
            return INVALID_EMAIL

        # controllo che la mail non sia gia presente e attiva nel db
        for subscriber in list(subscriptions.values()):
            if (mail == subscriber["email"] and subscriber["is_active"]) or (
                mail == subscriber["email"]
                and not subscriber["is_active"]  # noqa
                and isCreationDateExpired(subscriber["creation_date"])  # noqa
            ):
                return ALREADY_SUBSCRIBED
        else:
            subscriptions[mail] = {
                "email": mail,
                "is_active": True,
                "token": six.text_type(uuid.uuid4()),
                "creation_date": datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
            }

            transaction.commit()

        return OK

    def unsubscribe(self, mail):
        """
        do not unsubscribe directly, but return user token
        """
        logger.info("DEBUG: unsubscribe %s %s", self.context.title, mail)
        subscriptions = self.channel_subscriptions

        subscription = subscriptions.get(mail, None)

        transaction.commit()

        if not subscription:
            return INEXISTENT_EMAIL, None
        return OK, subscription["token"]

    def exportUsersList(self):
        response = []
        subscriptions = self.channel_subscriptions

        for i, subscriber in enumerate(subscriptions.values()):
            element = {}
            element["id"] = i
            element["email"] = subscriber["email"]
            element["is_active"] = subscriber["is_active"]
            element["creation_date"] = subscriber["creation_date"]
            response.append(element)

        return response, OK

    def importUsersList(self, usersList):
        logger.info("DEBUG: import userslist in %s", self.context.title)

        subscriptions = self.channel_subscriptions
        for user in usersList:
            user = user.lower()
            match = re.match(
                "^[_a-z0-9-]+(\\.[_a-z0-9-]+)*@[a-z0-9-]"
                + "+(\\.[a-z0-9-]+)*(\\.[a-z]{2,10})$",  # noqa
                user,
            )
            if match is not None:
                subscriptions[user] = {
                    "email": user,
                    "is_active": True,
                    "token": six.text_type(uuid.uuid4()),
                    "creation_date": datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
                }
            else:
                logger.info("INVALID_EMAIL: %s", user)

        transaction.commit()

        return OK

    def deleteUserList(self, usersList):
        # manca il modo di far capire se una mail non e presente nella lista
        logger.info("delete userslist from %s", self.context.title)
        subscriptions = self.channel_subscriptions

        for user in usersList:
            if user in list(subscriptions.keys()):
                del subscriptions[user]

        transaction.commit()

        return OK

    def emptyChannelUsersList(self):
        logger.info("DEBUG: emptyChannelUsersList %s", self.context.title)

        subscriptions = self.channel_subscriptions
        subscriptions.clear()

        transaction.commit()

        return OK
