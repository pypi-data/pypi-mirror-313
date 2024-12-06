from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp_community.models import Community

from djangoldp_tzcld.permissions import RegionalReferentPermissions


#############################
# Page Suivi du territoire => Synthèse
#############################
class TzcldTerritorySynthesisFollowed(Model):
    transverses = models.TextField(
        blank=True, null=True, verbose_name="Éléments transverses"
    )
    actions = models.TextField(blank=True, null=True, verbose_name="Actions à suivre")
    mobilisation = models.TextField(
        blank=True, null=True, verbose_name="Mobilisation des acteurs du territoire"
    )
    formalisation = models.TextField(
        blank=True, null=True, verbose_name="Formalisation du consensus"
    )
    ppde = models.TextField(
        blank=True,
        null=True,
        verbose_name="Identification, rencontre des PPDE, stratégie d'atteinte de l'exhaustivité",
    )
    ebe = models.TextField(
        blank=True,
        null=True,
        verbose_name="Identification des travaux utiles, préfiguration des emplois supplémentaires et d'une ou plusieurs EBE",
    )
    targetdate = models.DateField(
        verbose_name="Date estimée de candidature", blank=True, null=True
    )
    community = models.OneToOneField(
        Community,
        on_delete=models.CASCADE,
        related_name="tzcld_community_synthesis_followed",
        blank=True,
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
        verbose_name = _("TZCLD Territory Synthesis Followed")
        verbose_name_plural = _("TZCLD Territories Synthesis Followed")

        container_path = "tzcld-territory-synthesis-followed/"
        serializer_fields = [
            "@id",
            "transverses",
            "actions",
            "mobilisation",
            "formalisation",
            "ppde",
            "ebe",
            "targetdate",
            "community",
            "tzcld_referents_community_shared_notes",
            "date",
            "author",
            "tzcld_referents_community_shared_files",
        ]
        nested_fields = [
            "community",
            "tzcld_referents_community_shared_notes",
            "tzcld_referents_community_shared_files",
        ]
        rdf_type = "tzcld:territorySynthesisFollowed"
        permission_classes = [RegionalReferentPermissions]
