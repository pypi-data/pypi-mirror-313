from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import ReadOnly


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Origine de la mobilisation
#############################
class TzcldTerritoriesOriginMobilization(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Origin Mobilization")
        verbose_name_plural = _("TZCLD Options Origins Mobilization")

        container_path = "tzcld-origins-mobilization/"
        serializer_fields = ["@id", "name"]
        nested_fields = []
        rdf_type = "tzcld:territoryOriginMobilization"
        permission_classes = [ReadOnly]
