from django.conf import settings
from django.core.management.base import BaseCommand
from djangoldp_circle.models import Circle
from djangoldp_community.models import Community


class Command(BaseCommand):
    help = "Assign all the members/admins to the public circles of the communities they are part of"

    def handle(self, *args, **options):
        communities = Community.objects.all()

        for community in communities:
            community_members = community.members.user_set
            community_admins = community.admins.user_set
            community_public_circles = Circle.objects.filter(
                community=community, public=True
            )

            for member in community_members.all():
                for circle in community_public_circles:
                    circle.members.user_set.add(member)

            for admin in community_admins.all():
                for circle in community_public_circles:
                    circle.members.user_set.add(admin)
                    circle.admins.user_set.add(admin)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Community {community.id}: Assigned {community_members.count()} members and {community_admins.count()} admins to {community_public_circles.count()} public circles"
                )
            )
