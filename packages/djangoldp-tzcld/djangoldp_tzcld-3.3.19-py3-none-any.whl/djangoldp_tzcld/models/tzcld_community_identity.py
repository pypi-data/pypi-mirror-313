from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions
from djangoldp_community.models import Community
from djangoldp_conversation.models import Conversation

from djangoldp_tzcld.models.tzcld_territories_origin_mobilization import \
    TzcldTerritoriesOriginMobilization
from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Etat d'avancement => Carte d’identité du territoire
#############################
class TzcldCommunityIdentity(Model):
    community = models.OneToOneField(
        Community,
        on_delete=models.CASCADE,
        related_name="tzcld_profile_identity",
        null=True,
        blank=True,
    )
    origin_mobilization = models.ForeignKey(
        TzcldTerritoriesOriginMobilization,
        on_delete=models.DO_NOTHING,
        related_name="territory_origin_mobilization",
        blank=True,
        null=True,
    )
    application_date = models.DateField(
        verbose_name="Estimated application date", blank=True, null=True
    )
    signatory_structure = models.CharField(
        max_length=254, blank=True, null=True, default=""
    )
    birth_date = models.IntegerField(
        verbose_name="Project birth year", blank=True, null=True
    )
    last_contribution_date = models.DateField(
        verbose_name="Last contribution date", blank=True, null=True
    )
    conversations = models.ManyToManyField(
        Conversation, blank=True, related_name="tzcld_community_identity"
    )
    date = models.DateField(verbose_name="Date", auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    emergence_date = models.DateField(
        verbose_name="Date of recognition of project emergence", blank=True, null=True
    )
    habilitation_date = models.DateField(
        verbose_name="Date of habilitation", blank=True, null=True
    )

    def __str__(self):
        if self.community:
            return "{} ({})".format(self.community.urlid, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        auto_author = "author"
        verbose_name = _("TZCLD Territory Identity")
        verbose_name_plural = _("TZCLD Territories Identities")
        ordering = ["community"]
        container_path = "tzcld-communities-identity/"
        serializer_fields = [
            "@id",
            "community",
            "emergence_date",
            "habilitation_date",
            "origin_mobilization",
            "application_date",
            "signatory_structure",
            "birth_date",
            "last_contribution_date",
            "territories_project_team_members",
            "conversations",
            "tzcld_admins_community_shared_notes",
            "tzcld_admins_community_shared_files",
            "date",
            "author",
            "territories_political_landscape_deputies",
            "territories_political_landscape_senators",
            "territories_adhesions",
        ]
        nested_fields = [
            "community",
            "conversations",
            "tzcld_admins_community_shared_notes",
            "tzcld_admins_community_shared_files",
            "territories_project_team_members",
            "territories_political_landscape_deputies",
            "territories_political_landscape_senators",
            "territories_adhesions",
        ]
        rdf_type = "tzcld:communityIdentity"
        permission_classes = [InheritPermissions | RegionalReferentPermissions]
        inherit_permissions = ["community"]
        depth = 1
