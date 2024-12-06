from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from djangoldp.models import Model
from djangoldp_account.models import LDPUser as User
from djangoldp_circle.models import Circle
from djangoldp_community.models import Community

from djangoldp_tzcld.models.tzcld_community import TzcldCommunity
from djangoldp_tzcld.models.tzcld_community_evaluation_point import \
    TzcldCommunityEvaluationPoint
from djangoldp_tzcld.models.tzcld_community_evaluation_point_answer import \
    TzcldCommunityEvaluationPointAnswer
from djangoldp_tzcld.models.tzcld_community_followed_point import \
    TzcldCommunityFollowedPoint
from djangoldp_tzcld.models.tzcld_community_followed_point_answer import \
    TzcldCommunityFollowedPointAnswer
from djangoldp_tzcld.models.tzcld_community_identity import \
    TzcldCommunityIdentity
from djangoldp_tzcld.models.tzcld_contact_email import TzcldContactEmail
from djangoldp_tzcld.models.tzcld_contact_phone import TzcldContactPhone
from djangoldp_tzcld.models.tzcld_profile import TzcldProfile
from djangoldp_tzcld.models.tzcld_profile_job import TzcldProfileJob
from djangoldp_tzcld.models.tzcld_territory_department import \
    TzcldTerritoryDepartment
from djangoldp_tzcld.models.tzcld_territory_location import \
    TzcldTerritoryLocation
from djangoldp_tzcld.models.tzcld_territory_synthesis_followed import \
    TzcldTerritorySynthesisFollowed

#############################
# Signals
#############################


# Create tzcld user profile, job instance and contact email/phone when user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_tzcld_profile(sender, instance, created, **kwargs):
    if not Model.is_external(instance) and created:
        tzcld_profile = TzcldProfile.objects.create(user=instance)
        profile_job = TzcldProfileJob.objects.create(profile=tzcld_profile)
        TzcldContactEmail.objects.create(job=profile_job)
        TzcldContactPhone.objects.create(job=profile_job)

        # add the user to the first (tzcld) community
        community = Community.objects.order_by("id").first()
        if community:
            community.members.user_set.add(instance)
            community_public_circles = community.circles.filter(public=True)
            for circle in community_public_circles:
                circle.members.user_set.add(instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_primary_contact_on_user_disable(sender, instance, **kwargs):
    if instance.is_active is False:
        TzcldCommunity.objects.filter(primary_contact=instance).update(primary_contact=None)


# Create tzcld community profile, job instance and contact email/phone when community is created
@receiver(post_save, sender=Community)
def create_tzcld_community(instance, created, **kwargs):
    if not Model.is_external(instance) and created:
        # FIXME: Use get_or_create instead of checking created, avoid useless datas
        tzCommunity = TzcldCommunity.objects.create(community=instance)
        territory_location = TzcldTerritoryLocation.objects.create(
            name="Adresse à renseigner", community=tzCommunity
        )
        TzcldContactEmail.objects.create(
            email="brad@example.com", location=territory_location
        )
        TzcldContactPhone.objects.create(
            phone="0606060606", location=territory_location
        )

        # create empty community evaluation points answers
        evaluationPoints = TzcldCommunityEvaluationPoint.objects.all()
        for evaluationPoint in evaluationPoints:
            TzcldCommunityEvaluationPointAnswer.objects.create(
                evaluation_point=evaluationPoint, community=instance
            )

        # create empty community followed points answers
        followedPoints = TzcldCommunityFollowedPoint.objects.all()
        for followedPoint in followedPoints:
            TzcldCommunityFollowedPointAnswer.objects.create(
                followed_point=followedPoint, community=instance
            )

        # create empty TzcldCommunityIdentity instance
        TzcldCommunityIdentity.objects.create(community=instance)

        # create empty TzcldTerritorySynthesisFollowed instance
        TzcldTerritorySynthesisFollowed.objects.create(community=instance)


# Create empty TzcldCommunityEvaluationPointAnswer instance for every existing Territory when TzcldCommunityEvaluationPoint is created
@receiver(post_save, sender=TzcldCommunityEvaluationPoint)
def create_evaluation_point_answers(sender, instance, created, **kwargs):
    if created:
        communities = Community.objects.all()
        for community in communities:
            # Create TzcldCommunityEvaluationPointAnswer
            evaluation_point_answer = (
                TzcldCommunityEvaluationPointAnswer.objects.create(
                    community=community, evaluation_point=instance
                )
            )


# Create empty TzcldCommunityFollowedPointAnswer instance for every existing Territory when TzcldCommunityFollowedPoint is created
@receiver(post_save, sender=TzcldCommunityFollowedPoint)
def create_followed_point_answers(sender, instance, created, **kwargs):
    if created:
        communities = Community.objects.all()
        for community in communities:
            # Create TzcldCommunityFollowedPointAnswer
            followed_point_answer = TzcldCommunityFollowedPointAnswer.objects.create(
                community=community, followed_point=instance
            )


# Assign all the community members to the circle when a public circle is created
@receiver(post_save, sender=Circle)
def assign_community_members_to_circle(sender, instance, created, **kwargs):
    if not created or not instance.public or not instance.community:
        return

    # Get all the users for its community
    community_members = instance.community.members.user_set
    community_admins = instance.community.admins.user_set

    # Get all the users for this circle
    circle_members = instance.members.user_set
    circle_admins = instance.admins.user_set

    for community_member in community_members.all():
        if community_member not in circle_members.all():
            circle_members.add(community_member)

    for community_admin in community_admins.all():
        if community_admin not in circle_members.all():
            circle_members.add(community_admin)

        if community_admin not in circle_admins.all():
            circle_admins.add(community_admin)


# If a community is added to a user, add the user to the public circles of the community
# If a community is removed from a user, remove the user from the public circles of the community
@receiver(m2m_changed, sender=User.groups.through)
def assign_user_to_community_public_circles(sender, instance, action, pk_set, **kwargs):
    if not isinstance(instance, User):
        return

    if action == "pre_add":
        for pk in pk_set:
            group = Group.objects.get(id=pk)

            community = Community.objects.filter(members=group).first()
            if community:
                community_public_circles = community.circles.filter(public=True)
                for circle in community_public_circles:
                    circle.members.user_set.add(instance)

            community = Community.objects.filter(admins=group).first()
            if community:
                community_public_circles = community.circles.filter(public=True)
                for circle in community_public_circles:
                    circle.admins.user_set.add(instance)

    if action == "pre_remove":
        for pk in pk_set:
            group = Group.objects.get(id=pk)

            community = Community.objects.filter(members=group).first()
            if community:
                community_public_circles = community.circles.filter(public=True)
                for circle in community_public_circles:
                    circle.members.user_set.remove(instance)

            community = Community.objects.filter(admins=group).first()
            if community:
                community_public_circles = community.circles.filter(public=True)
                for circle in community_public_circles:
                    circle.admins.user_set.remove(instance)

@receiver(post_save, sender=TzcldTerritoryDepartment)
def no_empty_department(sender, instance, created, **kwargs):
    if not Model.is_external(instance) and created:
        if not instance.name:
            instance.delete()
