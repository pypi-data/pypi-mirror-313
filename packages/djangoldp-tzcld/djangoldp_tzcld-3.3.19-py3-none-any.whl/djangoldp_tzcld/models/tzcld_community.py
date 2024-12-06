from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions
from djangoldp_community.models import Community

from djangoldp_tzcld.models.tzcld_profiles_membership import \
    TzcldProfilesMembership
from djangoldp_tzcld.models.tzcld_territories_kind import TzcldTerritoriesKind
from djangoldp_tzcld.models.tzcld_territories_step_state import \
    TzcldTerritoriesStepState
from djangoldp_tzcld.models.tzcld_territory_department import \
    TzcldTerritoryDepartment
from djangoldp_tzcld.models.tzcld_territory_region import TzcldTerritoryRegion


#############################
# Page d'edition du territoire => Etant le modèle Community
#############################
class TzcldCommunity(Model):
    community = models.OneToOneField(
        Community,
        on_delete=models.CASCADE,
        related_name="tzcld_profile",
        null=True,
        blank=True,
    )
    kind = models.ForeignKey(
        TzcldTerritoriesKind,
        on_delete=models.DO_NOTHING,
        related_name="kind",
        blank=True,
        null=True,
    )
    step_state = models.ForeignKey(
        TzcldTerritoriesStepState,
        on_delete=models.DO_NOTHING,
        related_name="step_state",
        blank=False,
        null=True,
    )
    regions = models.ManyToManyField(
        TzcldTerritoryRegion, related_name="community_regions", blank=True
    )
    departments = models.ManyToManyField(
        TzcldTerritoryDepartment, related_name="community_departments", blank=True
    )
    membership = models.ForeignKey(
        TzcldProfilesMembership,
        on_delete=models.DO_NOTHING,
        related_name="community",
        blank=False,
        null=True,
    )
    membership_organisation_name = models.CharField(
        max_length=254, blank=True, null=True, default=""
    )
    visible = models.BooleanField(default=True)
    primary_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="primary_contact",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    information = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.community:
            return "{} ({})".format(self.community.urlid, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Profile")
        verbose_name_plural = _("TZCLD Territories Profiles")

        ordering = ["community"]
        container_path = "tzcld-communities/"
        serializer_fields = [
            "@id",
            "community",
            "kind",
            "step_state",
            "kind",
            "departments",
            "regions",
            "locations",
            "primary_contact",
            "membership",
            "membership_organisation_name",
            "visible",
            "information",
        ]
        rdf_type = "tzcld:communityProfile"
        nested_fields = ["regions", "departments", "locations"]
        permission_classes = [InheritPermissions]
        inherit_permissions = ["community"]
        depth = 1
