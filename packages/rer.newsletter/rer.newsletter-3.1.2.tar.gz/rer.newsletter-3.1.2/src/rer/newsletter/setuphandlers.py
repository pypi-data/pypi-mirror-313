# -*- coding: utf-8 -*-
from .transforms.link_transform import link_transform
from .transforms.mimetype import mail
from Products.CMFPlone.interfaces import INonInstallable
from Products.MimetypesRegistry.interfaces import IMimetypesRegistryTool
from Products.PortalTransforms.interfaces import IPortalTransformsTool
from zope.component import getUtility
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return ["rer.newsletter:uninstall", "rer.newsletter:to_1005"]


def post_install(context):
    """Post install script"""

    # registro il nuovo mimetype
    mimetypes_registry = getUtility(IMimetypesRegistryTool)
    mimetypes_registry.register(mail())

    # registro la mia custom transform
    pt = getUtility(IPortalTransformsTool)
    pt.registerTransform(link_transform())


def uninstall(context):
    """Uninstall script"""

    # elimino il mimetype
    mimetypes_registry = getUtility(IMimetypesRegistryTool)
    mimetype_instance = mimetypes_registry.lookup(mail())

    if mimetype_instance:
        mimetypes_registry.unregister(mimetype_instance[0])
