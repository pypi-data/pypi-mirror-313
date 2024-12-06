from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import OwnerPermissions, ReadOnly

from djangoldp_tzcld.models.tzcld_profile import TzcldProfile
from djangoldp_tzcld.models.tzcld_territory_department import \
    TzcldTerritoryDepartment


#############################
# Page d'edition de l'utilisateur => Postes
#############################
class TzcldProfileJob(Model):
    position = models.CharField(max_length=255, blank=True, null=True, default="")
    organisation = models.CharField(max_length=255, blank=True, null=True, default="")
    address = models.CharField(max_length=255, blank=True, null=True, default="")
    postal_code = models.CharField(max_length=255, blank=True, null=True, default="")
    city = models.CharField(max_length=255, blank=True, null=True, default="")
    department = models.ForeignKey(
        TzcldTerritoryDepartment,
        on_delete=models.SET_NULL,
        related_name="job_department",
        blank=True,
        null=True,
    )
    # address_public = models.BooleanField(default=False)
    profile = models.ForeignKey(
        TzcldProfile,
        on_delete=models.CASCADE,
        related_name="jobs",
        blank=True,
        null=True,
    )
    link = models.CharField(max_length=255, blank=True, null=True, default="")

    phone = models.CharField(max_length=255, blank=True, null=True, default="")
    phone_public = models.BooleanField(default=False)
    mobile_phone = models.CharField(max_length=255, blank=True, null=True, default="")
    mobile_phone_public = models.BooleanField(default=False)
    email = models.CharField(max_length=255, blank=True, null=True, default="")
    email_public = models.BooleanField(default=False)

    def __str__(self):
        if self.position:
            return "{} ({})".format(self.position, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD User profile job")
        verbose_name_plural = _("TZCLD Users profiles jobs")

        container_path = "tzcld-profile-job/"
        serializer_fields = [
            "@id",
            "position",
            "organisation",
            "address",
            "postal_code",
            "city",
            "department",
            "profile",
            "link",
            "phone",
            "phone_public",
            "mobile_phone",
            "mobile_phone_public",
            "email",
            "email_public",
        ]
        nested_fields = []
        rdf_type = "tzcld:profileJob"
        permission_classes = [ReadOnly | OwnerPermissions]
