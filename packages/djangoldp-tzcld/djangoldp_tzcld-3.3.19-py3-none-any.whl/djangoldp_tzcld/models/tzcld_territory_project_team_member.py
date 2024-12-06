from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions

from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity
from djangoldp_tzcld.models.tzcld_territories_team_user_state import \
    TzcldTerritoriesTeamUserState
from djangoldp_tzcld.models.tzcld_territories_training_course import \
    TzcldTerritoriesTrainingCourse
from djangoldp_tzcld.models.tzcld_territories_training_promotion import \
    TzcldTerritoriesTrainingPromotion
from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Equipe projet
#############################
class TzcldTerritoryProjectTeamMember(Model):
    first_name = models.CharField(max_length=255, blank=True, null=True, default="")
    last_name = models.CharField(max_length=255, blank=True, null=True, default="")
    mail = models.CharField(max_length=255, blank=True, null=True, default="")
    phone = models.CharField(max_length=255, blank=True, null=True, default="")
    role = models.CharField(max_length=255, blank=True, null=True, default="")
    details = models.CharField(max_length=255, blank=True, null=True, default="")
    user_state = models.ForeignKey(
        TzcldTerritoriesTeamUserState,
        on_delete=models.DO_NOTHING,
        related_name="team_member_state",
        blank=True,
        null=True,
    )
    etp = models.CharField(max_length=255, blank=True, null=True, default="")
    attachment_structure = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    training_course = models.ForeignKey(
        TzcldTerritoriesTrainingCourse,
        on_delete=models.DO_NOTHING,
        related_name="territories_team_members",
        blank=True,
        null=True,
    )
    training_promotion = models.ForeignKey(
        TzcldTerritoriesTrainingPromotion,
        on_delete=models.DO_NOTHING,
        related_name="territories_team_members",
        blank=True,
        null=True,
    )
    community_identity = models.ForeignKey(
        TzcldCommunityIdentity,
        on_delete=models.CASCADE,
        related_name="territories_project_team_members",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.community_identity:
            return "{} ({})".format(self.community_identity.urlid, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Territory Project Team Member")
        verbose_name_plural = _("TZCLD Territories Project Team Members")

        container_path = "tzcld-territories-project-team-member/"
        serializer_fields = [
            "@id",
            "first_name",
            "last_name",
            "mail",
            "phone",
            "role",
            "details",
            "user_state",
            "etp",
            "attachment_structure",
            "training_course",
            "training_promotion",
            "community_identity",
        ]
        nested_fields = ["community_identity"]
        rdf_type = "tzcld:territoryProjectTeamMember"
        permission_classes = [InheritPermissions | RegionalReferentPermissions]
        inherit_permissions = ["community_identity"]
