from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from djangoldp_community.models import Community

from .views import (ExportTerritories, MemberOfCommunitiesView,
                    MyTerritoriesView)

urlpatterns = [
    path(
        "myterritories/",
        MyTerritoriesView.as_view({"get": "list"}, model=Community),
        name="myterritories",
    ),
    path(
        "communities/export/xls/",
        csrf_exempt(ExportTerritories.as_view()),
        name="export_communities",
    ),
    path(
        "myterritories/export/xls/",
        csrf_exempt(ExportTerritories.as_view()),
        name="export_territories",
    ),
    path(
        "memberofcommunities/",
        MemberOfCommunitiesView.as_view({"get": "list"}, model=Community),
        name="memberofcommunities",
    ),
]
