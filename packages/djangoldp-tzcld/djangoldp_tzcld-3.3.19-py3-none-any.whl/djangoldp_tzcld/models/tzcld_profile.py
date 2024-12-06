from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions, ReadOnly

from djangoldp_tzcld.models.tzcld_territory_department import \
    TzcldTerritoryDepartment
from djangoldp_tzcld.models.tzcld_territory_region import TzcldTerritoryRegion


#############################
# Page d'edition de  l'utilisateur => Etant le modèle User
#############################
class TzcldProfile(Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tzcld_profile"
    )
    last_contribution_year = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    regions = models.ManyToManyField(
        TzcldTerritoryRegion, related_name="profile_regions", blank=True
    )
    departments = models.ManyToManyField(
        TzcldTerritoryDepartment, related_name="profile_department", blank=True
    )
    is_member = models.BooleanField(default=False)
    is_national_referent = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return "{} ({})".format(self.user.get_full_name(), self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD User Profile")
        verbose_name_plural = _("TZCLD Users Profiles")

        ordering = ["user"]
        serializer_fields = [
            "@id",
            "last_contribution_year",
            "jobs",
            "regions",
            "departments",
            "is_member",
            "is_national_referent",
        ]
        rdf_type = "tzcld:profile"
        auto_author = "user"
        depth = 1
        nested_fields = ["jobs", "regions", "departments"]
        permission_classes = [ReadOnly | InheritPermissions]
        inherit_permissions = ["user"]
