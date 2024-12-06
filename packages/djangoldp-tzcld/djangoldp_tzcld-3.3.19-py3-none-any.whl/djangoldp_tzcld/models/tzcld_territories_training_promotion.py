from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions, ReadOnly


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Participation aux formations TZCLD => Numéro de promotion
#############################
class TzcldTerritoriesTrainingPromotion(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Training Promotion")
        verbose_name_plural = _("TZCLD Options Training Promotions")

        container_path = "tzcld-training-promotions/"
        serializer_fields = ["@id", "name"]
        nested_fields = []
        rdf_type = "tzcld:territoryTrainingPromotion"
        permission_classes = [ReadOnly | InheritPermissions]
        inherit_permissions = ["territories_team_members"]
