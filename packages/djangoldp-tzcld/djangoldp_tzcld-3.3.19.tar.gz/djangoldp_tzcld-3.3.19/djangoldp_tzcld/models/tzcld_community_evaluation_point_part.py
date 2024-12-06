from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import OwnerPermissions, ReadOnly


#############################
# Page Etat d'avancement => Auto-evaluation => Partie
#############################
class TzcldCommunityEvaluationPointPart(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    title = models.CharField(max_length=254, blank=True, null=True, default="")
    description = models.TextField(blank=True, null=True)
    subtitle = models.CharField(max_length=254, blank=True, null=True, default="")
    order = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Evaluation Point Part")
        verbose_name_plural = _("TZCLD Territories Evaluation Point Parts")

        container_path = "tzcld-evaluation-point-parts/"
        serializer_fields = ["@id", "name", "title", "description", "subtitle", "order", "part_points"]
        ordering = ["order"]
        nested_fields = ["part_points"]
        rdf_type = "tzcld:evaluationPointPart"
        # FIXME: OwnerPermissions without owner field?
        permission_classes = [ReadOnly | OwnerPermissions]
        depth = 0
