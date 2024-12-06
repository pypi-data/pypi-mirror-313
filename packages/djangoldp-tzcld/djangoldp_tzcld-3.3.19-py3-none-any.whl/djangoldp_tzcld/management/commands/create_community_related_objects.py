from django.core.management.base import BaseCommand
from djangoldp_community.models import Community

from djangoldp_tzcld.models import (TzcldCommunityIdentity,
                                    TzcldTerritorySynthesisFollowed)


class Command(BaseCommand):
    help = "Create associated TzcldCommunityIdentity and TzcldTerritorySynthesisFollowed objects for existing Community objects"

    def handle(self, *args, **options):
        communities = Community.objects.all()

        for community in communities:
            # Check if TzcldCommunityIdentity already exists for this Community
            if not TzcldCommunityIdentity.objects.filter(community=community).exists():
                TzcldCommunityIdentity.objects.create(community=community)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created TzcldCommunityIdentity for Community {community.id}"
                    )
                )

            # Check if TzcldTerritorySynthesisFollowed already exists for this Community
            if not TzcldTerritorySynthesisFollowed.objects.filter(
                community=community
            ).exists():
                TzcldTerritorySynthesisFollowed.objects.create(community=community)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created TzcldTerritorySynthesisFollowed for Community {community.id}"
                    )
                )

            if (
                TzcldCommunityIdentity.objects.filter(community=community).exists()
                and TzcldTerritorySynthesisFollowed.objects.filter(
                    community=community
                ).exists()
            ):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Related objects already exist for Community {community.id}"
                    )
                )
