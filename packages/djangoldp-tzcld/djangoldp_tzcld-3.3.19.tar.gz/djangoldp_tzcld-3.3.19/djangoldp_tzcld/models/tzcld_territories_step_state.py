from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions, ReadOnly


#############################
# Page d'edition du territoire => Etat d'avancement
#############################
class TzcldTerritoriesStepState(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory step state")
        verbose_name_plural = _("TZCLD Options Territories step states")

        container_path = "tzcld-territories-step-states/"
        serializer_fields = ["@id", "name"]
        nested_fields = []
        rdf_type = "tzcld:territoryStepState"
        permission_classes = [ReadOnly | InheritPermissions]
        inherit_permissions = ["step_state"]
