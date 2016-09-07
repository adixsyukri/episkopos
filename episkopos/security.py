from kotti.security import (
    Principal,
    ROLES,
    SHARING_ROLES,
    set_roles,
    set_sharing_roles,
    set_user_management_roles,
    )
from kotti.resources import Document, File, Image
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('episkopos')

SITE_ACL = [
    ['Allow', 'system.Everyone', []],
    ['Allow', 'role:viewer', ['view']],
    ['Allow', 'role:editor', ['view', 'add', 'edit', 'state_change']],
    ['Allow', 'role:owner', ['view', 'add', 'edit', 'manage', 'state_change']],
    ['Allow', u'role:staff', ['view',
                              'add', 
                              'episkopos.add_activity',
                              'episkopos.add_document', 
                              'episkopos.add_file',
                              'episkopos.add_image']],
]


def add_role(role_id, role_title):
    """ Add role in share view and user management views """
    UPDATED_ROLES = ROLES.copy()
    UPDATED_ROLES[role_id] = Principal(role_id,
                                       title=role_title)
    UPDATED_SHARING_ROLES = list(SHARING_ROLES)
    UPDATED_SHARING_ROLES.append(role_id)
    set_roles(UPDATED_ROLES)
    set_sharing_roles(UPDATED_SHARING_ROLES)
    set_user_management_roles(UPDATED_SHARING_ROLES + ['role:admin'])

add_role(u'role:staff', _(u'Staff'))
add_role(u'role:customer', _(u'Customer'))
add_role(u'role:partner', _(u'Partner'))

Document.type_info.add_permission = 'episkopos.add_document'
File.type_info.add_permission = 'episkopos.add_file'
Image.type_info.add_permission = 'episkopos.add_image'
