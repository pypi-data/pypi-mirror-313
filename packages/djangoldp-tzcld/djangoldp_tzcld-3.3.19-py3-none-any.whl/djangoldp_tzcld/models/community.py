from djangoldp.permissions import (ACLPermissions, AnonymousReadOnly,
                                   ReadAndCreate)
from djangoldp_community.models import Community

from djangoldp_tzcld.permissions import RegionalReferentPermissions

Community._meta.nested_fields += [
    "tzcld_community_requests",
    "community_answer",
    "tzcld_community_followed_answer",
]
Community._meta.permission_classes = [
    AnonymousReadOnly,
    ReadAndCreate | ACLPermissions | RegionalReferentPermissions,
]
