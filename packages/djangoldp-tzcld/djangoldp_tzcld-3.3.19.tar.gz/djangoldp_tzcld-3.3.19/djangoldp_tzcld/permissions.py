from djangoldp.permissions import LDPBasePermission


class RegionalReferentPermissions(LDPBasePermission):
    permissions = {"view", "add", "change", "control"}
    """Gives write permissions to regional referents and read permissions to everyone"""

    def check_permission(self, user, model, obj):
        if user.is_anonymous:
            return False

        if user.is_superuser:
            return True

        while not obj.__class__.__name__ == "Community":
            if hasattr(obj, "community_admins") or hasattr(obj, "community_referents"):
                community_admins = getattr(obj, "community_admins", None)
                community_referents = getattr(obj, "community_referents", None)
                obj = community_admins or community_referents
            elif hasattr(obj, "community_identity"):
                obj = getattr(obj, "community_identity", None)
            elif hasattr(obj, "community"):
                obj = getattr(obj, "community", None)
            else:
                return False

        return bool(
            set.intersection(
                set(user.regions.all()), set(obj.tzcld_profile.regions.all())
            )
        )

    def has_object_permission(self, request, view, obj=None):
        return self.check_permission(request.user, view.model, obj)

    def get_permissions(self, user, model, obj=None):
        if not obj or self.check_permission(user, model, obj):
            return self.permissions
        return set()
