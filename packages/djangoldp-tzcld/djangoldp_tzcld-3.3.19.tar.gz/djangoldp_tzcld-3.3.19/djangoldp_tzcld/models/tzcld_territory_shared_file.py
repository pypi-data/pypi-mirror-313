from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import OwnerPermissions, ReadAndCreate

from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity
from djangoldp_tzcld.models.tzcld_territory_synthesis_followed import \
    TzcldTerritorySynthesisFollowed
from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Échanges avec mes référent-es => Fichiers de suivi (via relation community_admins)
# Page Échanges avec mes référent-es => Partagés avec la grappe (via relation community_referents)
#############################
class TzcldTerritorySharedFile(Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Interlocuteur",
    )
    name = models.CharField(max_length=1024, blank=True, null=True, default="")
    date = models.DateField(verbose_name="Date", auto_now=True)
    document = models.URLField(blank=True, null=True, verbose_name="Document")
    community_admins = models.ForeignKey(
        TzcldCommunityIdentity,
        on_delete=models.DO_NOTHING,
        related_name="tzcld_admins_community_shared_files",
        blank=True,
        null=True,
    )
    community_referents = models.ForeignKey(
        TzcldTerritorySynthesisFollowed,
        on_delete=models.DO_NOTHING,
        related_name="tzcld_referents_community_shared_files",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        auto_author = "author"
        owner_field = "author"
        verbose_name = _("TZCLD Territory Shared File")
        verbose_name_plural = _("TZCLD Territories Shared Files")

        container_path = "tzcld-territory-shared-files/"
        serializer_fields = [
            "@id",
            "author",
            "name",
            "date",
            "document",
            "community_admins",
            "community_referents",
        ]
        nested_fields = ["author", "community_admins", "community_referents"]
        rdf_type = "tzcld:territorySharedFile"
        permission_classes = [
            ReadAndCreate | OwnerPermissions | RegionalReferentPermissions
        ]
