from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions, ReadOnly


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Députés => Circonscription
#############################
class TzcldTerritoryCirconscription(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    order = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Circonscription")
        verbose_name_plural = _("TZCLD Options Circonscriptions")

        container_path = "tzcld-circonscriptions/"
        serializer_fields = ["@id", "name", "order"]
        ordering = ["order"]
        nested_fields = []
        rdf_type = "tzcld:circonscriptions"
        permission_classes = [ReadOnly | InheritPermissions]
        inherit_permissions = ["territories_deputies_circonscriptions"]
