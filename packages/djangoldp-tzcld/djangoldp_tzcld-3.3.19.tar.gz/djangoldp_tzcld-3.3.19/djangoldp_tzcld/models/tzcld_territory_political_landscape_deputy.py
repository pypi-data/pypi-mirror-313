from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity
from djangoldp_tzcld.models.tzcld_territory_circonscription import \
    TzcldTerritoryCirconscription


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Paysage politique / institutionnel : Député-e
#############################
class TzcldTerritoryPoliticalLandscapeDeputy(Model):
    deputy = models.CharField(max_length=254, blank=True, null=True, default="")
    circonscription = models.ForeignKey(
        TzcldTerritoryCirconscription,
        on_delete=models.DO_NOTHING,
        related_name="territories_deputies_circonscriptions",
        blank=True,
        null=True,
    )
    community_identity = models.ForeignKey(
        TzcldCommunityIdentity,
        on_delete=models.CASCADE,
        related_name="territories_political_landscape_deputies",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.community_identity:
            return "{} ({})".format(self.community_identity.urlid, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Political Landscape Deputy")
        verbose_name_plural = _("TZCLD Territories Political Landscape Deputies")

        container_path = "tzcld-territories-political-landscape-deputy/"
        serializer_fields = ["@id", "deputy", "circonscription", "community_identity"]
        nested_fields = ["community_identity"]
        rdf_type = "tzcld:territoryPoliticalLandscapeDeputy"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["community_identity"]
