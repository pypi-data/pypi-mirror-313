from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions, ReadAndCreate


#############################
# Page d'edition du territoire => Régions
# Page d'edition de  l'utilisateur => Régions
#############################
class TzcldTerritoryRegion(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    referents = models.ManyToManyField(
        get_user_model(), related_name="regions", blank=True
    )

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Région")
        verbose_name_plural = _("TZCLD Régions")

        container_path = "tzcld-regions/"
        serializer_fields = ["@id", "name", "referents"]
        ordering = ["name"]
        nested_fields = ["referents"]
        rdf_type = "tzcld:regions"
        permission_classes = [ReadAndCreate | InheritPermissions]
        inherit_permissions = ["community_regions", "profile_regions"]
