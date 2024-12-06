from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_tzcld.models.tzcld_community import TzcldCommunity


#############################
# Page d'edition du territoire => Coordonnées et lieux (alias EBE)
#############################
class TzcldTerritoryLocation(Model):
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    address = models.CharField(max_length=255, blank=True, null=True, default="")
    postal_code = models.CharField(max_length=255, blank=True, null=True, default="")
    city = models.CharField(max_length=255, blank=True, null=True, default="")
    community = models.ForeignKey(
        TzcldCommunity,
        on_delete=models.CASCADE,
        related_name="locations",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory location")
        verbose_name_plural = _("TZCLD Territories locations")

        container_path = "tzcld-territories-location/"
        serializer_fields = [
            "@id",
            "name",
            "address",
            "postal_code",
            "city",
            "phones",
            "emails",
            "community",
        ]
        nested_fields = ["emails", "phones"]
        rdf_type = "tzcld:territoryLocation"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["community"]
