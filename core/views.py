import base64
import csv
import hashlib
import os

import coreapi
import coreschema
import pyotp
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, decorators, serializers, status, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Country, Region, Competence, Occupation, Outbreak, ProfileDeployment, ProfileRecommendation, \
    Profile, User, OccupationCategory, OutbreakType, AcademicQualificationType, ProfileAcademicQualification, \
    AbstractDocument, Specialization, DetailedExperience, ProfileLanguage, Language
from core.permissions import AnonCreateAndUpdateOwnerOnly, AnonReadAdminCreate, \
    ProfileAuthenticatedCreateAndUpdateOwnerOnly, ProfileDeploymentAuthenticatedCreateAndUpdateOwnerOnly
from core.serializers import CountrySerializer, RegionSerializer, CompetenceSerializer, OccupationSerializer, \
    OutbreakSerializer, ProfileDeploymentSerializer, ProfileRecommendationSerializer, ProfileSerializer, UserSerializer, \
    GroupSerializer, OutbreakOptionsSerializer, ProfileCVSerializer, CustomTokenObtainPairSerializer, \
    OccupationCategorySerializer, ProfileDeploymentMiniSerializer, OutbreakTypeSerializer, \
    AcademicQualificationTypeSerializer, ProfileAcademicQualificationSerializer, AbstractDocumentSerializer, \
    OutbreakReportSerializer, SpecializationSerializer, DetailedExperienceSerializer, ProfileLanguageSerializer, \
    LanguageSerializer
from eac_rde_backend.settings import MEDIA_URL

media_dir = MEDIA_URL.replace('/', '')


@decorators.api_view(['GET'])
def confirm_email(request, username=None, otp=None):
    usr = User.objects.filter(username=username, otp=otp, otp_used=False).first()
    if usr is None:
        raise serializers.ValidationError("Could not find the specified user due to bad otp or username")
    usr.email_verified = True
    usr.otp_used = True
    usr.save()
    return Response('Email Verified Successfully')


@decorators.api_view(["POST"])
def send_email(request):
    email_receipient = request.GET.get('receipient')
    message = get_template("confirm_email.html").render(
        {
            'link': 'http://196.41.38.246:81/'
        })

    send_mail(
        subject='Subject here',
        html_message=message,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=['samfastone@gmail.com'],
        fail_silently=False
    )

    return Response()


@decorators.api_view(["POST"])
def request_password_change(request):
    """
    username,
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "username",
                required=True,
                location="form",
                schema=coreschema.Integer()
            ),
        ])

    username = request.data.get('username')
    user = User.objects.filter(username=username).first()
    if user is None:
        return Response({'detail': 'username not correct'})
    secr = hashlib.sha512(user.username.encode("utf-8")).hexdigest()
    secr = base64.b32encode(secr.encode("utf-8"))
    totp = pyotp.TOTP(secr)
    otp = totp.now()
    message = get_template("reset_password.html").render(
        {
            'otp': str(otp)
        })
    user.otp = otp
    user.otp_used = False
    user.save()
    send_mail(
        subject='EAC RDE Password Change',
        html_message=message,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

    return Response({'detail': 'OTP Sent Successfully'})


@decorators.api_view(["POST"])
def complete_password_change(request):
    """

    POST:
    username
    password
    otp
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "username",
                required=True,
                location="form",
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                "password",
                required=False,
                location="form",
                schema=coreschema.String()
            ),
            coreapi.Field(
                "otp",
                required=False,
                location="form",
                schema=coreschema.String()
            ),
        ])
    username = request.data.get('username')
    password = request.data.get('password')
    otp = request.data.get('otp')
    user = User.objects.filter(username=username, otp=otp, otp_used=False).first()
    if user is None:
        raise serializers.ValidationError({'detail': 'Please correct the details and try again'})
    # Prevent users from using their previous password.
    if check_password(password, user.password):
        return Response({"detail": "Can't reuse old password"}, status=status.HTTP_403_FORBIDDEN)

    user.password = make_password(password)
    user.otp_used = True
    user.save()
    return Response({"detail": "Password Changed Successfully"})


class CustomObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = None
    permission_classes = [AnonReadAdminCreate]


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
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
    filterset_fields = ['type', 'specialization']
    pagination_class = None


class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer
    filterset_fields = {'occupation_category'}
    permission_classes = [AnonReadAdminCreate]
    pagination_class = None


class DetailedExperienceViewSet(viewsets.ModelViewSet):
    queryset = DetailedExperience.objects.all()
    serializer_class = DetailedExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class ProfileLanguageViewSet(viewsets.ModelViewSet):
    queryset = ProfileLanguage.objects.all()
    serializer_class = ProfileLanguageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    filterset_fields = {'occupation'}
    permission_classes = [AnonReadAdminCreate]
    pagination_class = None


class OccupationCategoryViewSet(viewsets.ModelViewSet):
    queryset = OccupationCategory.objects.all()
    serializer_class = OccupationCategorySerializer
    permission_classes = [AnonReadAdminCreate]
    pagination_class = None


class AcademicQualificationTypeViewSet(viewsets.ModelViewSet):
    queryset = AcademicQualificationType.objects.all()
    serializer_class = AcademicQualificationTypeSerializer
    permission_classes = [AnonReadAdminCreate]
    pagination_class = None


class ProfileAcademicQualificationViewSet(viewsets.ModelViewSet):
    queryset = ProfileAcademicQualification.objects.all()
    filterset_fields = {'profile': ['exact']}
    serializer_class = ProfileAcademicQualificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "profile",
                required=False,
                location="query",
                type='integer',
                schema=coreschema.String()
            ),
        ])


def handle_uploaded_file(f, storage_location):
    with open(storage_location, 'wb+') as storage_location:
        for chunk in f.chunks():
            storage_location.write(chunk)


class OutbreakReportViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Outbreak.objects.all()
    serializer_class = OutbreakReportSerializer
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "report",
                required=False,
                location="form",
                type='file',
                schema=coreschema.String()
            ),
            coreapi.Field(
                "outbreak_id",
                required=False,
                location="form",
                schema=coreschema.String()
            ),
        ])

    def create(self, request):
        outbreak_id = request.data['outbreak_id']
        outbreak = get_object_or_404(Outbreak.objects.all(), pk=outbreak_id)

        if 'report' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            file = request.FILES['report']
            now = timezone.now()
            reformatted_filename = f"{now:%Y%m%d%H%M%s}" + ''.join(file.name.strip()).replace(' ', '')
            file.name = reformatted_filename
            outbreak.report = file
            outbreak.save()
        return Response({"outbreak_id": outbreak_id}, )

    def destroy(self, request, *args, **kwargs):
        outbreak = self.get_object()
        if os.path.exists(outbreak.report.path):
            os.remove(outbreak.report.path)
        outbreak.report = ''
        outbreak.save()
        return Response({'Deleted Successfully'})


class ProfileDeploymentReportViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "deployment_report",
                required=False,
                location="form",
                type='file',
                schema=coreschema.String()
            ),
            coreapi.Field(
                "profile_deployment_id",
                required=False,
                location="form",
                schema=coreschema.String()
            ),
        ])

    def create(self, request):
        profile_deployment_id = request.data['profile_deployment_id']
        profile_deployment = get_object_or_404(ProfileDeployment.objects.all(), pk=profile_deployment_id)

        if 'deployment_report' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            file = request.FILES['deployment_report']
            now = timezone.now()
            relative_dir = f"{media_dir}/deployment_reports/{now:%Y%m%d}"
            os.makedirs(relative_dir, exist_ok=True)
            final_file_location = f"{relative_dir}/{profile_deployment.id}{file.name}"
            handle_uploaded_file(file, final_file_location)
            profile_deployment.deployment_report = final_file_location
            profile_deployment.save()
        return Response({"profile_deployment_id": profile_deployment_id, "deployment_report": final_file_location}, )


class ProfileCVViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileCVSerializer
    # parser_classes = [MultiPartParser, FormParser]
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
                required=False,
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

    def update(self, request, pk=None):
        cv = request.data['cv']
        profile = get_object_or_404(Profile.objects.all(), pk=pk)
        profile.cv = cv
        profile.save()
        serializer = ProfileCVSerializer(profile)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        if os.path.exists(profile.cv.path):
            os.remove(profile.cv.path)
        profile.cv = ''
        profile.save()
        return Response({'Deleted Successfully'})


'''
Provide a list of RDEs registered within the system
To Return a no paginated result set:
pass no_page query param
'''


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticated, ProfileAuthenticatedCreateAndUpdateOwnerOnly]
    search_fields = ['first_name', 'middle_name', 'phone',
                     'last_name', 'gender', 'email',
                     'user__username', 'id_number']
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "output",
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                "search",
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                "region",
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                "country",
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                "gender",
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                "occupation",
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                "religion",
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                "application_status",
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                "academic_degree",
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                "competencies",
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
        ])

    def paginate_queryset(self, queryset, view=None):
        if 'no_page' in self.request.query_params:
            return None
        else:
            return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_queryset(self):
        auth_user = self.request.user
        if auth_user.is_staff or auth_user.is_superuser:
            if auth_user.attached_region is not None:
                if auth_user.level == 'eac':
                    return Profile.objects.all()
                else:
                    return Profile.objects.filter(region_of_residence__country_id=auth_user.attached_region.country.id)
            else:
                raise serializers.ValidationError({"generic": "No Region attached to your profile. Consult admin. "})

        else:
            return Profile.objects.filter(user=auth_user)

    def list(self, request, *args, **kwargs):
        region_of_residence = request.GET.getlist('region')
        country = request.GET.getlist('country')
        occupation = request.GET.getlist('occupation')
        gender = request.GET.getlist('gender')
        religion = request.GET.getlist('religion')
        application_status = request.GET.getlist('application_status')
        academic_degree = request.GET.getlist('academic_degree')
        competencies = request.GET.getlist('competencies')
        output = request.GET.get('output')
        rde_profiles = self.filter_queryset(self.get_queryset())

        if len(region_of_residence) != 0:
            rde_profiles = rde_profiles.filter(
                region_of_residence_id__in=region_of_residence,
            )
        if len(country) != 0:
            rde_profiles = rde_profiles.filter(
                region_of_residence__country_id__in=country,
            )
        if len(occupation) != 0:
            rde_profiles = rde_profiles.filter(
                occupation_id__in=occupation
            )
        if len(religion) != 0:
            rde_profiles = rde_profiles.filter(
                religion__in=religion
            )
        if len(gender) != 0:
            rde_profiles = rde_profiles.filter(
                gender__in=gender)
        if len(application_status) != 0:
            rde_profiles = rde_profiles.filter(
                application_status__in=application_status
            )
        if len(academic_degree) != 0:
            rde_profiles = rde_profiles.filter(
                profile_academic_qualifications__qualification_type__in=academic_degree
            )
        if len(application_status) != 0:
            rde_profiles = rde_profiles.filter(
                application_status__in=application_status
            )
        if len(competencies) != 0:
            rde_profiles = rde_profiles.filter(
                competencies__in=competencies
            )

        if output == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="rde_profiles.csv"'

            writer = csv.writer(response)
            writer.writerow(["id", "name", "gender", "religion",
                             "occupation", "date_of_birth", "next_of_kin",
                             "email", "phone", "id_type", "id_number", "region_of_residence",
                             "active", "available", "note", "application_status",
                             "competencies", "current_deployment"])
            for profile in rde_profiles:
                writer.writerow([
                    profile.id, f"{profile.first_name} {profile.last_name}", profile.gender, profile.religion,
                    profile.occupation, profile.date_of_birth, profile.next_of_kin, profile.email,
                    profile.phone, profile.id_type, profile.id_number, profile.region_of_residence.name,
                    True if profile.active else False, profile.available, profile.note, profile.application_status,
                    profile.competencies if profile.competencies is not None else "None",
                    profile.deployments.filter(status='deployed').first().outbreak.name
                    if profile.deployments.filter(status='deployed').first() is not None else "None",
                ])
            return response

        queryset = rde_profiles
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(rde_profiles, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractDocumentViewSet(viewsets.ModelViewSet):
    queryset = AbstractDocument.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AbstractDocumentSerializer

    def destroy(self, request, *args, **kwargs):
        abs_document = self.get_object()
        if os.path.exists(abs_document.document.path):
            os.remove(abs_document.document.path)
        abs_document.delete()
        return Response({'Deleted Successfully'})


@decorators.api_view(["GET"])
def get_outbreak_options(request):
    """ get outbreak options in label value pairs """
    return Response(OutbreakOptionsSerializer(Outbreak.objects.all(), many=True).data)


@decorators.api_view(["GET"])
def fetch_stats(request):
    """ fetch stats """
    """ number of all RDEs, Current Active Outbreaks, Currently Deployed RDEs, RDEs not deployed,   """
    # user
    user = request.user
    if user.level == 'eac':
        profile_deployments = ProfileDeployment.objects.prefetch_related('profile')
        all_rdes = Profile.objects.all()
        active_deployments = \
            ProfileDeployment.objects.aggregate(
                Count('profile_id', distinct=True))['profile_id__count']
    else:
        # todo: fix active deployments count
        profile_deployments = ProfileDeployment.objects.prefetch_related('profile',
                                                                         'profile__region_of_residence__country_id') \
            .filter(profile__region_of_residence__country_id=user.attached_region.country.id)
        active_deployments = \
            ProfileDeployment.objects.prefetch_related('profile_id', 'profile__region_of_residence__country_id').filter(
                profile__region_of_residence__country_id=user.attached_region.country.id).aggregate(
                Count('profile_id', distinct=True))['profile_id__count']

        all_rdes = Profile.objects.filter(region_of_residence__country_id=user.attached_region.country.id)
    approved_rdes = all_rdes.filter(application_status='approval_complete').count()
    undeployed_rdes = all_rdes.count() - active_deployments
    result = {
        "active_deployments": active_deployments,
        "approved_rdes": approved_rdes,
        "undeployed_rdes": undeployed_rdes
    }

    return Response(result)


@decorators.api_view(["GET"])
def get_profile_deployments(request, profile_id=None):
    profile = get_object_or_404(Profile.objects.all(), pk=profile_id)
    deployments = profile.deployments
    """ get outbreak options in label value pairs """
    return Response(ProfileDeploymentSerializer(deployments, many=True).data)


class ProfileRecommendationViewSet(viewsets.ModelViewSet):
    queryset = ProfileRecommendation.objects.all()
    serializer_class = ProfileRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None


class OutbreakViewSet(viewsets.ModelViewSet):
    """
        Defines an event of public health concern.
        Below is the proposed structure of the JSON Fields in this model

        "general_information":{
            "type":"onsite/offsite",
            "reserved_for_pwds":"true/false"
        }
        "detailed_information":{
            "mission_and_objectives":"",
            "task_description":""
        }
        "eligibility_creteria":{
            "age":"",
            "nationality":""
        }
        "requirements":{
            "required_experience":"",
            "areas_of_expertise":"",
            "languages":"",
            "required_education_level":"",
            "competencies_and_values":"",
            "driving_license":""
        }
        "other_information":{
            "living_conditions_and_remarks":"",
            "inclusivity_statement":""
        }
        """
    queryset = Outbreak.objects.all()
    serializer_class = OutbreakSerializer

    @action(detail=True, methods=['GET'], name='Get RDEs For Outbreak')
    def get_rdes(self, request, pk=None, *args, **kwargs):
        queryset = ProfileDeployment.objects.filter(outbreak=pk)
        serializer = ProfileDeploymentMiniSerializer(queryset, many=True)
        return Response(serializer.data)


class OutbreakTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [AnonReadAdminCreate]
    queryset = OutbreakType.objects.all()
    serializer_class = OutbreakTypeSerializer


class ProfileDeploymentsViewSet(viewsets.ModelViewSet):
    queryset = ProfileDeployment.objects.all()
    serializer_class = ProfileDeploymentSerializer
    permission_classes = [ProfileDeploymentAuthenticatedCreateAndUpdateOwnerOnly]

    def get_queryset(self):
        auth_user = self.request.user
        if auth_user.attached_region is not None:
            if auth_user.level == 'rde':
                return ProfileDeployment.objects.filter(profile__user=auth_user)
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
