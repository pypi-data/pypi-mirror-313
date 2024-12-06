from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp_community.models import Community

from djangoldp_tzcld.models.tzcld_community_followed_point import \
    TzcldCommunityFollowedPoint
from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Suivi du territoire => Critères de suiv => Parties (pointsParts) => Points => Répnse
#############################
class TzcldCommunityFollowedPointAnswer(Model):
    answer = models.TextField(blank=False, null=True)
    followed_point = models.ForeignKey(
        TzcldCommunityFollowedPoint,
        on_delete=models.CASCADE,
        related_name="followed_point_answer",
        blank=False,
        null=True,
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="tzcld_community_followed_answer",
        blank=False,
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
        verbose_name = _("TZCLD Territory Followed Point Answer")
        verbose_name_plural = _("TZCLD Territories Followed Point answers")
        container_path = "tzcld-communities-followed-point-answers/"
        serializer_fields = [
            "@id",
            "answer",
            "followed_point",
            "community",
            "date",
            "author",
        ]
        rdf_type = "tzcld:communityFollowedPointAnswer"
        depth = 0
        permission_classes = [RegionalReferentPermissions]
