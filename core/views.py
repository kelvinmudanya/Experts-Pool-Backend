import coreapi
import coreschema
from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions, decorators, serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Country, Region, Competence, Occupation, Outbreak, ProfileDeployment, ProfileRecommendation, \
    Profile, User, OccupationCategory
from core.permissions import AnonCreateAndUpdateOwnerOnly, AnonReadAdminCreate, AdminOnly
from core.serializers import CountrySerializer, RegionSerializer, CompetenceSerializer, OccupationSerializer, \
    OutbreakSerializer, ProfileDeploymentSerializer, ProfileRecommendationSerializer, ProfileSerializer, UserSerializer, \
    GroupSerializer, OutbreakOptionsSerializer, ProfileCVSerializer, CustomTokenObtainPairSerializer, \
    OccupationCategorySerializer


class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = None
    permission_classes = [AnonReadAdminCreate]


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [AnonReadAdminCreate]
    filterset_fields = {'country': ['exact']}
    pagination_class = None


class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [AnonReadAdminCreate]
    pagination_class = None


class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer
    permission_classes = [AnonReadAdminCreate]
    pagination_class = None


class OccupationCategoryViewSet(viewsets.ModelViewSet):
    queryset = OccupationCategory.objects.all()
    serializer_class = OccupationCategorySerializer
    permission_classes = [AnonReadAdminCreate]
    pagination_class = None


class ProfileCVViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "profile_id",
                required=True,
                location="form",
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                "cv",
                required=True,
                location="form",
                schema=coreschema.String()
            ),
        ])

    """
    retrieve:
    Return cv for the specified user profile.

    create:
    Create a cv against a profile

    update:
    Change A profile's cv

    """

    def retrieve(self, request, pk=None):
        """ just pass the normal /id without these details"""
        profile = get_object_or_404(Profile.objects.all(), pk=pk)
        serializer = ProfileCVSerializer(profile)
        return Response(serializer.data)

    def create(self, request):
        cv = request.data['cv']
        profile_id = request.data['profile_id']
        profile = get_object_or_404(Profile.objects.all(), pk=profile_id)
        profile.cv = cv
        profile.save()
        serializer = ProfileCVSerializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        cv = request.data['cv']
        profile = get_object_or_404(Profile.objects.all(), pk=pk)
        profile.cv = cv
        profile.save()
        serializer = ProfileCVSerializer(profile)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        auth_user = self.request.user
        if auth_user.is_staff or auth_user.is_superuser:
            if auth_user.attached_region is not None:
                if auth_user.level == 'eac':
                    return Profile.objects.all()
                else:
                    return Profile.objects.filter(region_of_residence=auth_user.attached_region)
            else:
                raise serializers.ValidationError({"generic": "No Region attached to your profile. Consult admin. "})

        else:
            return Profile.objects.filter(user=auth_user)


@decorators.api_view(["POST"])
def suggest_rdes(request):
    """Suggest RDEs Based on Competencies. pass competencies=[id1, id2] """
    try:
        competencies = request.data['competencies']
    except KeyError:
        competencies = []

    if competencies == []:
        suggested_profiles = Profile.objects.all()
    else:
        suggested_profiles = Profile.objects.filter(competencies__in=competencies)
    return Response(ProfileSerializer(suggested_profiles, many=True).data)


@decorators.api_view(["GET"])
def get_outbreak_options(request):
    """ get outbreak options in label value pairs """
    return Response(OutbreakOptionsSerializer(Outbreak.objects.all(), many=True).data)


@decorators.api_view(["GET"])
def get_profile_deployments(request, profile_id=None):
    profile = get_object_or_404(Profile.objects.all(), pk=profile_id)
    deployments = profile.deployments
    """ get outbreak options in label value pairs """
    return Response(ProfileDeploymentSerializer(deployments, many=True).data)


# class RdeSuggestionViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#
#     # @action(detail=True, methods=['post'])
#     # def retrieve(self, request, *args, **kwargs):
#     #     pass
#     #
#     # @action(detail=True, methods=['patch'])
#     # def partial_update(self, request, *args, **kwargs):
#     #     pass
#     #
#     # @action(detail=True, methods=['put'])
#     # def update(self, request, *args, **kwargs):
#     #     pass
#     #
#     # @action(detail=True, methods=['delete'])
#     # def delete(self, request, *args, **kwargs):
#     #     pass
#
#     @action(detail=False, methods=['post'])
#     def suggest_rde_list(self, request):
#         try:
#             competencies = request.data['competencies']
#         except KeyError:
#             competencies = []
#         suggested_profiles = Profile.objects.filter(competencies__in=competencies)
#
#         ## adding pagination
#         # page = self.paginate_queryset(recent_users)
#         # if page is not None:
#         #     serializer = self.get_serializer(page, many=True)
#         #     return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(suggested_profiles, many=True)
#         return Response(serializer.data)
#

class ProfileRecommendationViewSet(viewsets.ModelViewSet):
    queryset = ProfileRecommendation.objects.all()
    serializer_class = ProfileRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class OutbreakViewSet(viewsets.ModelViewSet):
    queryset = Outbreak.objects.all()
    serializer_class = OutbreakSerializer

    # def retrieve(self, request, pk=None):
    #     """ get deployments for this outbreak """
    #     queryset =


class ProfileDeploymentsViewSet(viewsets.ModelViewSet):
    queryset = ProfileDeployment.objects.all()
    serializer_class = ProfileDeploymentSerializer
    permission_classes = [AdminOnly]

    def get_queryset(self):
        auth_user = self.request.user
        if auth_user.attached_region is not None:
            if auth_user.level == 'eac':
                return ProfileDeployment.objects.all()
            else:
                return ProfileDeployment.objects.filter(profile__region_of_residence=auth_user.attached_region)
        else:
            raise serializers.ValidationError({"generic": "No Region attached to your profile. Consult admin. "})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [AnonCreateAndUpdateOwnerOnly]

    def get_queryset(self):
        auth_user = self.request.user
        if auth_user.is_staff:
            return User.objects.filter(is_active=True)
        else:
            return User.objects.filter(pk=auth_user.id)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
