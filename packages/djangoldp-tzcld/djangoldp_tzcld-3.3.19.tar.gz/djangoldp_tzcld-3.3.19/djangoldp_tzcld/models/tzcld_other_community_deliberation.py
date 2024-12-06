from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import OwnerPermissions, ReadOnly


#############################
# Page Etat d'avancement => Auto-evaluation => Parties (pointsParts) => Points => Réponses => valeur de la réponse
#############################
class TzcldOtherCommunityDeliberation(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Other Territory deliberation")
        verbose_name_plural = _("TZCLD Options Other Community deliberations")

        container_path = "tzcld-others-communities-deliberations/"
        serializer_fields = ["@id", "name"]
        nested_fields = []
        rdf_type = "tzcld:otherCommunityDeliberation"
        # FIXME: OwnerPermissions without owner field?
        permission_classes = [ReadOnly | OwnerPermissions]
