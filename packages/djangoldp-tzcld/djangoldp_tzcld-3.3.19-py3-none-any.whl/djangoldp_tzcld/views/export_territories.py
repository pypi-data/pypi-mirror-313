import csv

import pandas as pd
import validators
from django.http import HttpResponse
from djangoldp.models import Model
from djangoldp.views import NoCSRFAuthentication
from rest_framework.views import APIView


# export csv - Old button (export selected lines)
class ExportTerritories(APIView):
    authentication_classes = (NoCSRFAuthentication,)

    def dispatch(self, request, *args, **kwargs):
        response = super(ExportTerritories, self).dispatch(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = request.headers.get("origin")
        response["Access-Control-Allow-Methods"] = "POST, GET"
        response["Access-Control-Allow-Headers"] = (
            "authorization, Content-Type, if-match, accept, sentry-trace, DPoP"
        )
        response["Access-Control-Expose-Headers"] = "Location, User"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Accept-Post"] = "application/json"
        response["Accept"] = "*/*"

        if request.user.is_authenticated:
            try:
                response["User"] = request.user.webid()
            except AttributeError:
                pass
        return response

    def post(self, request):
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="export.xlsx"'

        if request.method == "POST" and request.data and isinstance(request.data, list):
            user_permissions = request.user.get_user_permissions()
            fields = [
                "Nom du territoire",
                "Type de territoire",
                "Etat d'avancement",
                "Description du territoire",
                "Région",
                "Département",
                "Adresses",
                "année de naissance du projet",
                "origine de la mobilisation",
                "date de reconnaissance en tant que projet émergent",
                "date d'habilitation",
                "type de structure adhérente",
                "nom de la structure adhérente",
                "année d'adhésion",
            ]
            rows = list()

            for urlid in request.data:
                # Check that the array entries are URLs
                if validators.url(urlid):
                    model, instance = Model.resolve(urlid)
                    if instance:
                        row = {
                            'datas': list(),
                            'team_members': list(),
                            'politics': list(),
                        }

                        tzcld_profile = getattr(instance, "tzcld_profile", None) if "djangoldp_tzcld.view_tzcldprofile" in user_permissions else None
                        profile = getattr(instance, "profile", None) if "djangoldp_tzcld.view_tzcldprofile" in user_permissions else None
                        territory_location = getattr(tzcld_profile, "locations", None) if "djangoldp_tzcld.view_tzcldterritorylocation" in user_permissions else None
                        tzcld_profile_identity = getattr(instance, "tzcld_profile_identity", None) if "djangoldp_tzcld.view_tzcldcommunityidentity" in user_permissions else None
                        territories_adhesions = getattr(tzcld_profile_identity, "territories_adhesions", None) if "djangoldp_tzcld.view_tzcldterritoryadhesion" in user_permissions else None
                        territories_project_team_members = getattr(tzcld_profile_identity, "territories_project_team_members", None) if "djangoldp_tzcld.view_tzcldterritoryprojectteammember" in user_permissions else None
                        territories_political_landscape_deputies = getattr(tzcld_profile_identity, "territories_political_landscape_deputies", None) if ("djangoldp_tzcld.view_tzcldterritorypoliticallandscapesenator" in user_permissions and "djangoldp_tzcld.view_tzcldterritorydepartment" in user_permissions) else None
                        territories_political_landscape_senators = getattr(tzcld_profile_identity, "territories_political_landscape_senators", None) if ("djangoldp_tzcld.view_tzcldterritorypoliticallandscapedeputy" in user_permissions and "djangoldp_tzcld.view_tzcldterritorycirconscription" in user_permissions) else None

                        row['datas'].append(getattr(instance, "name", ""))
                        row['datas'].append(getattr(getattr(tzcld_profile, "kind", None), "name", ""))
                        row['datas'].append(getattr(getattr(tzcld_profile, "step_state", None), "name", ""))
                        row['datas'].append(getattr(getattr(profile, "description", None), "name", ""))
                        regions = list()
                        departments = list()
                        if tzcld_profile:
                            for region in tzcld_profile.regions.all():
                                if region:
                                    regions.append(region.name)
                            for department in tzcld_profile.departments.all():
                                if department:
                                    departments.append(department.name)
                        row['datas'].append(", ".join(regions))
                        row['datas'].append(", ".join(departments))
                        locations = list()
                        if territory_location:
                            for location in territory_location.all():
                                loc = list()
                                loc.append(getattr(location, "name", ""))
                                loc.append(getattr(location, "address", ""))
                                loc.append(getattr(location, "postal_code", ""))
                                loc.append(getattr(location, "city", ""))
                                locations.append(", ".join([el for el in loc if el]))
                        row['datas'].append(", ".join(locations))
                        row['datas'].append(getattr(tzcld_profile_identity, "birth_date", ""))
                        row['datas'].append(getattr(getattr(tzcld_profile_identity, "origin_mobilization", None), "name", ""))
                        row['datas'].append(getattr(tzcld_profile_identity, "emergence_date", ""))
                        row['datas'].append(getattr(tzcld_profile_identity, "habilitation_date", ""))
                        types = list()
                        names = list()
                        years = list()
                        if territories_adhesions:
                            for territories_adhesion in territories_adhesions.all():
                                if territories_adhesion:
                                    type = getattr(territories_adhesion, "type", "")
                                    if type:
                                        types.append(type)
                                    name = getattr(territories_adhesion, "name", "")
                                    if name:
                                        names.append(name)
                                    year = getattr(territories_adhesion, "year", "")
                                    if year:
                                        years.append(year.strftime("%d-%m-%Y"))
                        row['datas'].append(", ".join(types))
                        row['datas'].append(", ".join(names))
                        row['datas'].append(", ".join(years))
                        if territories_project_team_members:
                            for member in territories_project_team_members.all():
                                team_member = list()
                                team_member.append(getattr(member, "first_name", ""))
                                team_member.append(getattr(member, "last_name", ""))
                                team_member.append(getattr(member, "mail", ""))
                                team_member.append(getattr(member, "phone", ""))
                                team_member.append(getattr(member, "role", ""))
                                team_member.append(getattr(member, "details", ""))
                                team_member.append(getattr(getattr(member, "user_state", None), "name", ""))
                                team_member.append(getattr(member, "attachment_structure", ""))
                                team_member.append(getattr(member, "etp", ""))
                                team_member.append(getattr(getattr(member, "training_course", None), "name", ""))
                                team_member.append(getattr(getattr(member, "training_promotion", None), "name", ""))
                                row['team_members'].append(team_member)
                        if territories_political_landscape_deputies:
                            for personality in territories_political_landscape_deputies.all():
                                politic = list()
                                politic.append(getattr(personality, "deputy", ""))
                                politic.append(getattr(getattr(personality, "circonscription", None), "name", ""))
                                row['politics'].append(politic)
                        if territories_political_landscape_senators:
                            for personality in territories_political_landscape_senators.all():
                                politic = list()
                                politic.append(getattr(personality, "senator", ""))
                                politic.append(getattr(getattr(personality, "circonscription", None), "name", ""))
                                row['politics'].append(politic)

                        rows.append(row)

            team_member_fields = [
                "prénom",
                "nom",
                "mail",
                "téléphone",
                "rôle",
                "précisions",
                "statut de la personne",
                "structure de rattachement",
                "ETP consacré au projet",
                "Formation suivie",
                "numéro de promotion",
            ]
            how_many_members_cols = max((len(row['team_members']) for row in rows), default=0)
            for _ in range(how_many_members_cols):
                fields += team_member_fields

            politics_fields = [
                "Nom",
                "Circonscription",
            ]
            how_many_politics_cols = max((len(row['politics']) for row in rows), default=0)
            for _ in range(how_many_politics_cols):
                fields += politics_fields

            for row in rows:
                while len(row['team_members']) < how_many_members_cols:
                    row['team_members'].append([""] * len(team_member_fields))
                row['datas'] += [item for sublist in row['team_members'] for item in sublist]
                while len(row['politics']) < how_many_politics_cols:
                    row['politics'].append([""] * len(politics_fields))
                row['datas'] += [item for sublist in row['politics'] for item in sublist]

        df = pd.DataFrame([row['datas'] for row in rows], columns=fields)
        df.to_excel(response, sheet_name="Territoires", index=False)
        if response:
            return response

        return HttpResponse("Not Found")
