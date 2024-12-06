from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions
from djangoldp_community.models import Community


#############################
# Page Suivi du territoire => Historique des échanges
#############################
class TzcldTerritoryRequest(Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name="Interlocuteurs")
    date = models.DateField(verbose_name="Date")
    contactType = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
        verbose_name="Canal d'échange",
    )
    contactQualification = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
        verbose_name="Qualification de l'échange",
    )
    subject = models.TextField(blank=True, null=True, verbose_name="Synthèse des échanges")
    comments = models.TextField(blank=True, null=True, verbose_name="Commentaires et actions à suivre")
    files = models.URLField(blank=True, null=True, verbose_name="Fichier")
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="tzcld_community_requests",
        blank=False,
        null=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="territory_request_author",
    )

    def __str__(self):
        if self.id:
            return "{} ({})".format(self.id, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        auto_author = "author"
        verbose_name = _("TZCLD Territory Request")
        verbose_name_plural = _("TZCLD Territories Requests")

        container_path = "tzcld-territory-request/"
        serializer_fields = [
            "@id",
            "user",
            "date",
            "contactType",
            "contactQualification",
            "subject",
            "comments",
            "files",
            "community",
            "author",
        ]
        nested_fields = ["user", "community"]
        rdf_type = "tzcld:territoryRequest"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["community"]
