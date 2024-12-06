from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import ReadOnly


#############################
# Page Suivi du territoire => Critères de suiv => Partie
#############################
class TzcldCommunityFollowedPointPart(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    title = models.CharField(max_length=254, blank=True, null=True, default="")
    order = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Followed Point Part")
        verbose_name_plural = _("TZCLD Territories Followed Point Parts")
        container_path = "tzcld-followed-point-parts/"
        serializer_fields = ["@id", "name", "title", "order", "followed_part_points"]
        ordering = ["order"]
        nested_fields = ["followed_part_points"]
        rdf_type = "tzcld:followedPointPart"
        depth = 0
        permission_classes = [ReadOnly]
