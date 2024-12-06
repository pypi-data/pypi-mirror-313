from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import OwnerPermissions, ReadOnly

from djangoldp_tzcld.models.tzcld_community_evaluation_point_part import \
    TzcldCommunityEvaluationPointPart


#############################
# Page Etat d'avancement => Auto-evaluation => Parties (pointsParts) => Point
#############################
class TzcldCommunityEvaluationPoint(Model):
    TYPE_FALSE = "checkboxe"
    TYPE_DELIBERATION = "tzcld-communities-deliberations"
    TYPE_OTHER_DELIBERATION = "tzcld-others-communities-deliberations"
    TYPE_CONCILS_DELIBERATION = "tzcld-councils-departments-deliberations"
    TYPE_OF_FIELD_CHOICES = [
        (TYPE_FALSE, "Checkboxe"),
        (TYPE_DELIBERATION, "TZCLD Territory deliberation"),
        (TYPE_OTHER_DELIBERATION, "TZCLD Other Territory deliberation"),
        (TYPE_CONCILS_DELIBERATION, "TZCLD Council department deliberation"),
    ]

    name = models.CharField(max_length=1024, blank=True, null=True, default="")
    description = models.CharField(max_length=1024, blank=True, null=True, default="")
    order = models.IntegerField(blank=True, null=True, default=1)
    part = models.ForeignKey(
        TzcldCommunityEvaluationPointPart,
        on_delete=models.CASCADE,
        related_name="part_points",
        blank=True,
        null=True,
    )
    points = models.IntegerField(blank=True, null=True, default=0)
    fieldType = models.CharField(
        max_length=125,
        choices=TYPE_OF_FIELD_CHOICES,
        default=TYPE_FALSE,
    )

    def __str__(self):
        if self.id:
            return "{} ({})".format(self.id, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Evaluation Point")
        verbose_name_plural = _("TZCLD Territories Evaluation Points")

        ordering = ["order"]
        container_path = "tzcld-communities-evaluation-points/"
        serializer_fields = [
            "@id",
            "name",
            "description",
            "order",
            "part",
            "points",
            "fieldType",
            "evaluation_point_answer",
        ]
        rdf_type = "tzcld:communityEvaluationPoint"
        # FIXME: OwnerPermissions without owner field?
        permission_classes = [ReadOnly | OwnerPermissions]
        depth = 0
