## Controller Python Script "folder_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Delete objects from a folder
##

from Products.CMFPlone import PloneMessageFactory as _
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFCore.utils import getToolByName

req = context.REQUEST
paths=req.get('paths', [])

putils = context.plone_utils

status='failure'
message=_(u'Please select one or more items to delete.')

# a hint to the link integrity code to indicate the number of events to
# expect, so that all integrity breaches can be handled in a single form
# only;  normally the adapter (LinkIntegrityInfo) should be used here, but
# this would make CMFPlone depend on an import from LinkIntegrity, which
# it shouldn't...
context.REQUEST.set('link_integrity_events_to_expect', len(paths))

canModifyPaths = []
undeletablePaths = []
member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
for opath in paths:
    tobj = context.restrictedTraverse(opath)
    if member.has_permission('Modify portal content', tobj):
        canModifyPaths.append(opath)
    else:
        undeletablePaths.append(opath)
success, failure = putils.deleteObjectsByPaths(canModifyPaths, REQUEST=req)
if undeletablePaths:
    message = _(u'${items} could not be deleted.',
                    mapping={u'items' : ', '.join(undeletablePaths)})
    context.plone_utils.addPortalMessage(message)

if success:
    status='success'
    message = _(u'Item(s) deleted.')

if failure:
    message = _(u'${items} could not be deleted.',
                mapping={u'items' : ', '.join(failure.keys())})

context.plone_utils.addPortalMessage(message)
return state.set(status=status)
