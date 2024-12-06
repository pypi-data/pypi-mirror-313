from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import OwnerPermissions, ReadAndCreate
from djangoldp_conversation.models import Conversation

from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity
from djangoldp_tzcld.models.tzcld_territory_synthesis_followed import \
    TzcldTerritorySynthesisFollowed
from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Échanges avec mes référent-es => Notes partagées (via relation community_admins)
# Page Suivi du territoire => Notes partagées (via relation community_referents)
#############################
class TzcldTerritorySharedNote(Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    longdesc = models.TextField(blank=True, null=True)
    community_admins = models.ForeignKey(
        TzcldCommunityIdentity,
        on_delete=models.DO_NOTHING,
        related_name="tzcld_admins_community_shared_notes",
        blank=True,
        null=True,
    )
    community_referents = models.ForeignKey(
        TzcldTerritorySynthesisFollowed,
        on_delete=models.DO_NOTHING,
        related_name="tzcld_referents_community_shared_notes",
        blank=True,
        null=True,
    )
    conversations = models.ManyToManyField(
        Conversation, blank=True, related_name="tzcld_shared_notes"
    )
    date = models.DateField(verbose_name="Date", auto_now=True)

    def __str__(self):
        if self.id:
            return "{} ({})".format(self.id, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        auto_author = "author"
        owner_field = "author"
        verbose_name = _("TZCLD Territory Shared Note")
        verbose_name_plural = _("TZCLD Territories Shared Notes")
        container_path = "tzcld-territory-shared-notes/"
        serializer_fields = [
            "@id",
            "author",
            "longdesc",
            "community_admins",
            "community_referents",
            "conversations",
            "date",
        ]
        nested_fields = [
            "author",
            "community_admins",
            "community_referents",
            "conversations",
        ]
        rdf_type = "tzcld:territorySharedNote"
        permission_classes = [
            ReadAndCreate | OwnerPermissions | RegionalReferentPermissions
        ]
