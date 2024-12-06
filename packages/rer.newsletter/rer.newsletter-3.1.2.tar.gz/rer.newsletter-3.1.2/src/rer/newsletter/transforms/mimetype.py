# -*- coding: utf-8 -*-
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem


class mail(MimeTypeItem):
    __name__ = "Mimetype for mail channel"
    mimetypes = ("text/mail",)
    binary = 0
