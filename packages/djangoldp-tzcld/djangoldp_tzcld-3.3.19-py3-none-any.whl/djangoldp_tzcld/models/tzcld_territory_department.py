from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions, ReadOnly


#############################
# Page d'edition du territoire => Départements
# Page Etat d'avancement => Carte d’identité du territoire => Sénateurs => Département
# Page d'edition de  l'utilisateur => Départements
# Page d'edition de  l'utilisateur => Postes => Département
#############################
class TzcldTerritoryDepartment(Model):
    name = models.CharField(max_length=254, blank=True, null=True, default="")

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Department")
        verbose_name_plural = _("TZCLD Options Departments")

        container_path = "tzcld-departments/"
        serializer_fields = ["@id", "name", "job_department"]
        ordering = ["name"]
        nested_fields = []
        rdf_type = "tzcld:departments"
        permission_classes = [ReadOnly | InheritPermissions]
        inherit_permissions = [
            "territories_senators_departments",
            "community_departments",
            "job_department",
            "profile_department",
        ]
