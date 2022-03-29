"""
  For deleting a content you must have:

    "Delete objects" permission on the parent folder
    "Delete objects" permission on the content itself
    Beeing able to modify the content (all the contents) you want to delete

  Code inspired by collective.deletepermission

"""


from AccessControl import Unauthorized
from AccessControl import getSecurityManager
from AccessControl.Permissions import delete_objects
from AccessControl.Permissions import copy_or_move
from AccessControl.PermissionRole import PermissionRole

from plone.dexterity.content import Container

def protect_del_objects(self, ids=None):
    #import pdb; pdb.set_trace()
    sm = getSecurityManager()
    if not sm.checkPermission('Delete objects', self):      # delete_objects
        raise Unauthorized(
            "Do not have permissions to remove this object")

    if ids is None:
        ids = []
    if isinstance(ids, str):
        ids = [ids]
    for id_ in ids:
        item = self._getOb(id_)
        if not sm.checkPermission("Delete objects", item) or \
           not sm.checkPermission("Modify portal content", item):
            raise Unauthorized(
                "Do not have permissions to remove this object")

def manage_delObjects(self, ids=None, REQUEST=None):
    """We need to enforce security."""
    protect_del_objects(self, ids)
    return super(Container, self).manage_delObjects(ids, REQUEST=REQUEST)

# Patch manage_cutObjects and manage_pasteObjects security
# By default Dexterity Container sets the permission of manage_cutObjects and
# manage_pasteObjects to ModifyPortalContent
#  https://github.com/plone/plone.dexterity/blob/master/plone/dexterity/content.py
def apply_delete_objects_permission_role(klass, name, replacement):
    setattr(klass, name, PermissionRole('Delete objects', None))


def dummy_replacement():
    pass
