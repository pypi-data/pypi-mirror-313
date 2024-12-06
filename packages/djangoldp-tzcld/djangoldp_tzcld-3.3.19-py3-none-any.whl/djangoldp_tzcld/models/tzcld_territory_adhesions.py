from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity


class TzcldTerritoryAdhesion(Model):
    type = models.CharField(verbose_name="Type de structure adhérente", max_length=254, blank=True, null=True, default="")
    name = models.CharField(verbose_name="Nom de la structure adhérente", max_length=254, blank=True, null=True, default="")
    year = models.DateField(
        verbose_name="Année d'adhésion", blank=True, null=True
    )
    community_identity = models.ForeignKey(
        TzcldCommunityIdentity,
        on_delete=models.CASCADE,
        related_name="territories_adhesions",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.community_identity:
            return "{} ({})".format(self.community_identity.urlid, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Adhesions")
        verbose_name_plural = _("TZCLD Territories Adhesions")

        container_path = "tzcld-territories-adhesion/"
        serializer_fields = ["@id", "type", "name", "year", "community_identity"]
        nested_fields = ["community_identity"]
        rdf_type = "tzcld:territoryAdhesion"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["community_identity"]
