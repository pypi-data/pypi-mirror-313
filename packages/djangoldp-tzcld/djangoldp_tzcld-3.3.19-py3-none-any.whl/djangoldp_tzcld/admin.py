from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin

from djangoldp_tzcld.models import (TzcldCommunity,
                                    TzcldCommunityEvaluationPoint,
                                    TzcldCommunityEvaluationPointPart,
                                    TzcldCommunityFollowedPoint,
                                    TzcldCommunityFollowedPointPart,
                                    TzcldProfile, TzcldProfileJob,
                                    TzcldTerritoriesKind,
                                    TzcldTerritoryLocation,
                                    TzcldTerritoryRegion)


# Register inline locations to territory community on TzcldCommunity
class TzcldTerritoryLocationInline(admin.TabularInline):
    model = TzcldTerritoryLocation
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


# Register inline jobs to user profile on TzcldProfile
class TzcldProfileJobInline(admin.TabularInline):
    model = TzcldProfileJob
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(TzcldProfile)
class TzcldProfileAdmin(DjangoLDPAdmin):
    inlines = [TzcldProfileJobInline]


# Register inline points to parts on TzcldCommunityFollowed
class TzcldCommunityFollowedPointInline(admin.TabularInline):
    model = TzcldCommunityFollowedPoint
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(TzcldCommunityFollowedPointPart)
class TzcldCommunityFollowedPointPartAdmin(DjangoLDPAdmin):
    inlines = [TzcldCommunityFollowedPointInline]


# Register inline points to parts on TzcldCommunityEvaluation
class TzcldCommunityEvaluationPointInline(admin.TabularInline):
    model = TzcldCommunityEvaluationPoint
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


@admin.register(TzcldCommunityEvaluationPointPart)
class TTzcldCommunityEvaluationPointPartAdmin(DjangoLDPAdmin):
    inlines = [TzcldCommunityEvaluationPointInline]


class TzcldCommunityInline(admin.StackedInline):
    model = TzcldCommunity
    exclude = ("urlid", "is_backlink", "allow_create_backlink")
    extra = 0


class TzcldCommunityAdmin(DjangoLDPAdmin):
    list_display = ("community", "urlid")
    inlines = [TzcldTerritoryLocationInline]
    exclude = ("urlid", "slug", "is_backlink", "allow_create_backlink")
    search_fields = ["urlid", "community", "name"]
    ordering = ["community"]


"""
class TzcldOrgsInline(admin.TabularInline):
    model = TzcldProfile.orgs.through
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class TzcldRegionsInline(admin.TabularInline):
    model = TzcldProfile.regions.through
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class TzcldEventsInline(admin.TabularInline):
    model = TzcldProfile.events.through
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    extra = 0


class TzcldProfileAdmin(DjangoLDPAdmin):#
    list_display = ('user', 'urlid')
    exclude = ('urlid', 'user', 'is_backlink', 'allow_create_backlink', 'slug')
    inlines = [TzcldRegionsInline, TzcldOrgsInline, TzcldEventsInline]
    ordering = ['user']

    def get_queryset(self, request):
        queryset = super(TzcldProfileAdmin, self).get_queryset(request)
        internal_ids = [x.pk for x in queryset if not Model.is_external(x)]
        return queryset.filter(pk__in=internal_ids)
"""


class TzcldGenericAdmin(DjangoLDPAdmin):
    list_display = ("name", "urlid")
    exclude = (
        "urlid",
        "slug",
        "is_backlink",
        "allow_create_backlink",
        "tzcldcommunity",
        "tzcldprofile",
    )
    search_fields = ["urlid", "name"]
    ordering = ["name"]


# admin.site.register(TzcldProfile, TzcldProfileAdmin)
admin.site.register(TzcldCommunity, TzcldCommunityAdmin)
admin.site.register(TzcldTerritoriesKind, TzcldGenericAdmin)
admin.site.register(TzcldTerritoryRegion, TzcldGenericAdmin)
# admin.site.register(TzcldProfileOrganisation, TzcldGenericAdmin)
# admin.site.register(TzcldProfileEvent, TzcldGenericAdmin)
# admin.site.register(TzcldProfileRegion, TzcldGenericAdmin)
