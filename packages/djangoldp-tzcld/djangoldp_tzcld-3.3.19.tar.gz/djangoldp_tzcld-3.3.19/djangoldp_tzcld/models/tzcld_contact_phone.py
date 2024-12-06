from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_tzcld.models.tzcld_profile_job import TzcldProfileJob
from djangoldp_tzcld.models.tzcld_territory_location import \
    TzcldTerritoryLocation


#############################
# Page d'edition du territoire => Coordonnées et lieux => Téléphones
#############################
class TzcldContactPhone(Model):
    phone = models.CharField(max_length=255, blank=True, null=True, default="")
    phone_type = models.CharField(max_length=255, blank=True, null=True, default="")
    phone_public = models.BooleanField(default=False)
    job = models.ForeignKey(
        TzcldProfileJob,
        on_delete=models.CASCADE,
        related_name="phones",
        blank=True,
        null=True,
    )
    location = models.ForeignKey(
        TzcldTerritoryLocation,
        on_delete=models.CASCADE,
        related_name="phones",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.id:
            return "{} ({})".format(self.id, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Phone")
        verbose_name_plural = _("TZCLD Phones")
        container_path = "tzcld-contact-phone/"
        serializer_fields = [
            "@id",
            "phone",
            "phone_type",
            "phone_public",
            "job",
            "location",
        ]
        nested_fields = []
        rdf_type = "tzcld:phone"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["job"]
