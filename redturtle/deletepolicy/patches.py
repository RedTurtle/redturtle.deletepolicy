# Monkey patch for default manage_cutObjects behaviour. 
# We don't want to have ModifyPortalContent permission to be allow to manage_cutObjects.
# So now we are using 'Delete objects'

import logging
from Globals import InitializeClass
from Products.CMFCore import permissions
from Products.CMFPlone.PloneFolder import BasePloneFolder
from Products.Archetypes.BaseFolder import BaseFolderMixin
from Products.Archetypes.BaseBTreeFolder import BaseBTreeFolder
from Products.CMFPlone.Portal import PloneSite
from AccessControl.Permissions import delete_objects, copy_or_move, view_management_screens

logger = logging.getLogger("redturtle.deletepolicy")


def _update_permissionsCut(_class):
    old_permissions = dict(_class.__ac_permissions__).copy()
    try:
        mpc = list(old_permissions[permissions.ModifyPortalContent])
        mpc.remove('manage_cutObjects')
        old_permissions[permissions.ModifyPortalContent] = tuple(mpc)
    except KeyError:
        pass
    _class.__ac_permissions__ = ((delete_objects, ('manage_cutObjects',)),) + tuple(old_permissions.items())
    InitializeClass(_class)
    
_update_permissionsCut(BasePloneFolder)
_update_permissionsCut(BaseFolderMixin)
_update_permissionsCut(BaseBTreeFolder)
logger.warning("*** Monkeypatched default permission for cut objects (from ModifyPortalContent to DeleteObject) ***")


#def _update_permissionsPaste(_class):
#    old_permissions = dict(_class.__ac_permissions__).copy()
#    try:
#        mpc = list(old_permissions[permissions.ModifyPortalContent])
#        mpc.remove('manage_pasteObjects')
#        old_permissions[permissions.ModifyPortalContent] = tuple(mpc)
#    except KeyError:
#        pass
#    _class.__ac_permissions__ = ((permissions.AddPortalContent, ('manage_pasteObjects',)),) + tuple(old_permissions.items())
#    InitializeClass(_class)
#    
#_update_permissionsPaste(BasePloneFolder)
#_update_permissionsPaste(BaseFolderMixin)
#_update_permissionsPaste(BaseBTreeFolder)
#_update_permissionsPaste(PloneSite)
#logger.warning("*** Monkeypatched default permission for paste objects (from ModifyPortalContent to AddPortalContent) ***")

