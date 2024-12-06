from django.db import models
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import InheritPermissions


#############################
# Page d'edition du territoire => Type d'organisation
#############################
class TzcldProfilesMembership(Model):
    name = models.CharField(max_length=255, blank=False, null=True, default="")

    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.urlid)
        else:
            return self.urlid

    class Meta(Model.Meta):
        verbose_name = _("TZCLD Membership type")
        verbose_name_plural = _("TZCLD Options Membership types")

        container_path = "tzcld-profile-membership/"
        serializer_fields = ["@id", "name"]
        nested_fields = []
        rdf_type = "tzcld:profileMembership"
        permission_classes = [InheritPermissions]
        inherit_permissions = ["community"]
