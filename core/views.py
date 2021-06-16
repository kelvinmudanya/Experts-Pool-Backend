from django.contrib.auth.models import Group
from rest_framework import viewsets, permissions

from core.models import Country, Region, Competence, Occupation, Outbreak, ProfileDeployment, ProfileRecommendation, \
    Profile, User
from core.serializers import CountrySerializer, RegionSerializer, CompetenceSerializer, OccupationSerializer, \
    OutbreakSerializer, ProfileDeploymentSerializer, ProfileRecommendationSerializer, ProfileSerializer, UserSerializer, \
    GroupSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = None


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = None


class CompetenceViewSet(viewsets.ModelViewSet):
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    pagination_class = None


class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer
    pagination_class = None


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRecommendationViewSet(viewsets.ModelViewSet):
    queryset = ProfileRecommendation.objects.all()
    serializer_class = ProfileRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class OutbreakViewSet(viewsets.ModelViewSet):
    queryset = Outbreak.objects.all()
    serializer_class = OutbreakSerializer


class ProfileDeploymentsViewSet(viewsets.ModelViewSet):
    queryset = ProfileDeployment.objects.all()
    serializer_class = ProfileDeploymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
