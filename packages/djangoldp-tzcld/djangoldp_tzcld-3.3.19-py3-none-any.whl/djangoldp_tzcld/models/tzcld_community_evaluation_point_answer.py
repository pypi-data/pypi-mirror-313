from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions
from djangoldp_community.models import Community

from djangoldp_tzcld.models.tzcld_community_deliberation import \
    TzcldCommunityDeliberation
from djangoldp_tzcld.models.tzcld_community_evaluation_point import \
    TzcldCommunityEvaluationPoint
from djangoldp_tzcld.models.tzcld_council_department_deliberation import \
    TzcldCouncilDepartmentDeliberation
from djangoldp_tzcld.models.tzcld_other_community_deliberation import \
    TzcldOtherCommunityDeliberation
from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Etat d'avancement => Auto-evaluation => Parties (pointsParts) => Points => Réponse
#############################
class TzcldCommunityEvaluationPointAnswer(Model):
    answer = models.BooleanField(default=False)
    answer_community_deliberation = models.ForeignKey(
        TzcldCommunityDeliberation,
        on_delete=models.DO_NOTHING,
        related_name="community_answer",
        blank=True,
        null=True,
    )
    answer_other_community_deliberation = models.ForeignKey(
        TzcldOtherCommunityDeliberation,
        on_delete=models.DO_NOTHING,
        related_name="community_answer",
        blank=True,
        null=True,
    )
    answer_concil_department_deliberation = models.ForeignKey(
        TzcldCouncilDepartmentDeliberation,
        on_delete=models.DO_NOTHING,
        related_name="community_answer",
        blank=True,
        null=True,
    )
    comment = models.TextField(blank=True, null=True)
    evaluation_point = models.ForeignKey(
        TzcldCommunityEvaluationPoint,
        on_delete=models.CASCADE,
        related_name="evaluation_point_answer",
        blank=True,
        null=True,
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="community_answer",
        blank=True,
        null=True,
    )
    date = models.DateField(verbose_name="Date", auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        if self.id:
            return "{} ({})".format(self.id, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        auto_author = "author"
        verbose_name = _("TZCLD Territory Evaluation Point Answer")
        verbose_name_plural = _("TZCLD Territories Evaluation Point answers")
        container_path = "tzcld-communities-evaluation-point-answers/"
        serializer_fields = [
            "@id",
            "answer",
            "answer_community_deliberation",
            "answer_other_community_deliberation",
            "answer_concil_department_deliberation",
            "comment",
            "evaluation_point",
            "community",
            "date",
            "author",
        ]
        rdf_type = "tzcld:communityEvaluationPointAnswer"
        permission_classes = [InheritPermissions | RegionalReferentPermissions]
        inherit_permissions = ["community"]
        depth = 0
