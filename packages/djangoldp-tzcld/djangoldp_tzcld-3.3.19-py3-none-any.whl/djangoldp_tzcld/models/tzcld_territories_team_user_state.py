from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions, ReadOnly


#############################
# Page Etat d'avancement => Carte d’identité du territoire => Equipe projet => Statut de la personne
#############################
class TzcldTerritoriesTeamUserState(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")
    order = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Team User State")
        verbose_name_plural = _("TZCLD Options Team User States")

        ordering = ["order"]
        container_path = "tzcld-team-user-states/"
        serializer_fields = ["@id", "name", "order"]
        nested_fields = []
        rdf_type = "tzcld:territoryTeamUserState"
        permission_classes = [ReadOnly | InheritPermissions]
        inherit_permissions = ["team_member_state"]
