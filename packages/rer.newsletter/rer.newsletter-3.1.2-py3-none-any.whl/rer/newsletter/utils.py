# -*- coding: utf-8 -*-
from email.utils import formataddr
from plone import api

import json


# STATUS MESSAGES
# general
NOK = -1
UNHANDLED = 0
SUBSCRIBED = OK = 1
INVALID_CHANNEL = 5

# subscribe
ALREADY_SUBSCRIBED = 2
INVALID_EMAIL = 3

# Email
PROBLEM_WITH_MAIL = 11

# unsubscribe
INEXISTENT_EMAIL = 4

# add channel
CHANNEL_USED = 6

# import usersList
FILE_FORMAT = 7

# delete user
MAIL_NOT_PRESENT = 8

# user's activation
ALREADY_ACTIVE = 9
INVALID_SECRET = 10

# channel history
SEND_UID_NOT_FOUND = 11


def get_site_title():
    current_lang = api.portal.get_current_language()
    site_title = api.portal.get_registry_record("plone.site_title")
    try:
        title_json = json.loads(site_title)
    except ValueError:
        #  standard site title, not RER customization
        return site_title
    titles = list(title_json.keys())
    if current_lang not in titles and "default" in titles:
        return title_json.get("default", None)
    elif current_lang in titles:
        return title_json.get(current_lang, None)
    else:
        return "Plone Site"


def compose_sender(channel):
    if not channel.sender_email:
        return "noreply@rer.it"
    if channel.sender_name:
        return formataddr((channel.sender_name, channel.sender_email))
    return channel.sender_email
