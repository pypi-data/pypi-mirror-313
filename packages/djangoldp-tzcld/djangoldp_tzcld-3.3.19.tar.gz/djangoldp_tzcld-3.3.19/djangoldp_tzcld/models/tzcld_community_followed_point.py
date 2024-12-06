from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import ReadOnly

from djangoldp_tzcld.models.tzcld_community_followed_point_part import \
    TzcldCommunityFollowedPointPart


#############################
# Page Suivi du territoire => Critères de suiv => Parties (pointsParts) => Point
#############################
class TzcldCommunityFollowedPoint(Model):

    TYPE_TEXT = "text"
    TYPE_TEXTAREA = "textarea"
    TYPE_OF_FIELD_CHOICES = [
        (TYPE_TEXT, "Text"),
        (TYPE_TEXTAREA, "Textearea"),
    ]

    name = models.CharField(max_length=1024, blank=True, null=True, default="")
    order = models.IntegerField(blank=True, null=True, default=1)
    part = models.ForeignKey(
        TzcldCommunityFollowedPointPart,
        on_delete=models.CASCADE,
        related_name="followed_part_points",
        blank=True,
        null=True,
    )
    fieldType = models.CharField(
        max_length=25,
        choices=TYPE_OF_FIELD_CHOICES,
        default=TYPE_TEXTAREA,
    )
    helpComment = models.TextField(
        blank=True, null=True, verbose_name="Questions to ask"
    )

    def __str__(self):
        if self.id:
            return "{} ({})".format(self.id, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Followed Point")
        verbose_name_plural = _("TZCLD Territories Followed Points")
        ordering = ["order"]
        container_path = "tzcld-communities-followed-points/"
        serializer_fields = ["@id", "name", "order", "part", "fieldType", "helpComment"]
        rdf_type = "tzcld:communityFollowedPoint"
        depth = 0
        permission_classes = [ReadOnly]
