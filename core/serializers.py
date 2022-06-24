import base64
import datetime
import hashlib

import pyotp
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import Occupation, Country, Region, Competence, Profile, ProfileRecommendation, Outbreak, \
    ProfileDeployment, User, OccupationCategory, OutbreakType, AcademicQualificationType, ProfileAcademicQualification, \
    AbstractDocument, DetailedExperience, ProfileLanguage, Language
from eac_rde_backend.settings import EMAIL_HOST_USER, APP_URL, MEDIA_URL

media_dir = MEDIA_URL.replace('/', '')


def handle_uploaded_file(f, storage_location):
    with open(storage_location, 'wb+') as storage_location:
        for chunk in f.chunks():
            storage_location.write(chunk)


class CountrySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)
    rde_count = serializers.SerializerMethodField('get_rde_count',
                                                  read_only=True)
    deployed_count = serializers.SerializerMethodField('get_deployed_rde_count',
                                                       read_only=True)
    pending_approval = serializers.SerializerMethodField('get_pending_approval_rde_count',
                                                         read_only=True)

    class Meta:
        model = Country
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name

    def get_rde_count(self, obj):
        return Profile.objects.filter(region_of_residence__country_id=obj.id).count()

    def get_pending_approval_rde_count(self, obj):
        return Profile.objects.filter(region_of_residence__country_id=obj.id,
                                      application_status='pending_approval'
                                      ).count()

    def get_deployed_rde_count(self, obj):
        return Profile.objects.filter(region_of_residence__country_id=obj.id,
                                      deployments__status__exact='initiated'
                                      ).count()


class AcademicQualificationTypeSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = AcademicQualificationType
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.degree_level


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class DetailedExperienceSerializer(serializers.ModelSerializer):
    occupation_name = serializers.SerializerMethodField('get_experience_name', read_only=True)

    def get_experience_name(self, obj):
        if obj.occupation is not None:
            return obj.occupation.name
        else:
            return ''

    class Meta:
        model = DetailedExperience
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Country.objects.all())

    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'country', 'country_id', 'value', 'label']

    def create(self, validated_data):
        country = validated_data.pop('country_id')
        region = Region.objects.create(country=country, **validated_data)
        region.save()
        return region

    def update(self, instance, validated_data):
        country = validated_data.pop('country_id')

        region = super().update(instance, validated_data)
        region.country = country
        region.save()
        return region

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return f"{obj.name} - {obj.country.name}"


class CompetenceSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Competence
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name


class DetailedCompetenceSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    specialization_name = serializers.SerializerMethodField('get_specialization_name', read_only=True)
    occupation_id = serializers.SerializerMethodField('get_occupation_id', read_only=True)
    occupation_name = serializers.SerializerMethodField('get_occupation_name', read_only=True)
    occupation_category_name = serializers.SerializerMethodField('get_occupation_category_name', read_only=True)

    class Meta:
        model = Competence
        fields = ['name', 'type', 'description', 'specialization', 'specialization_id', 'value',
                  'label', 'specialization_name', 'occupation_name', 'occupation_id',
                  'occupation_category_name']

    def get_specialization_name(self, obj):
        return obj.specialization.name

    def get_occupation_name(self, obj):
        return obj.specialization.occupation.name

    def get_occupation_id(self, obj):
        return obj.specialization.occupation.id

    def get_occupation_category_name(self, obj):
        return obj.specialization.occupation.occupation_category.name

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name


class SpecializationSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Competence
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name


class OccupationCategorySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = OccupationCategory
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name


class OccupationSerializer(serializers.ModelSerializer):
    occupation_category = OccupationCategorySerializer(read_only=True)
    occupation_category_id = serializers.PrimaryKeyRelatedField(write_only=True,
                                                                queryset=OccupationCategory.objects.all())

    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Occupation
        fields = ['value', 'label', 'name', 'occupation_category', 'occupation_category_id']

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name

    def create(self, validated_data):
        occupation_category = validated_data.pop('occupation_category_id')
        occupation = Occupation.objects.create(occupation_category=occupation_category, **validated_data)
        occupation.save()
        return occupation


class GroupSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'value', 'label']

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password',
                                                                            'placeholder': 'Password'})
    groups_objects = serializers.SerializerMethodField('get_groups_objects',
                                                       read_only=True)
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                                many=True)
    attached_region = serializers.PrimaryKeyRelatedField(
        read_only=True)
    attached_region_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Region.objects.all())

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'password', 'phone_number', 'groups', 'groups_objects', 'email_verified',
                  'staff_number', 'attached_region_id', 'other_region', 'attached_region', 'email']

    def get_groups_objects(self, obj):
        return GroupSerializer(obj.groups, many=True).data

    def create(self, validated_data):
        groups = validated_data.pop('groups')
        # try:
        #     staff_number = validated_data.pop('staff_number')
        # except:
        #     staff_number = ''

        attached_region = validated_data.pop('attached_region_id')

        if not self.context['request'].user.is_staff:
            # cannot add groups since user is not admin
            groups = []
            staff_number = ''

        phone_number = validated_data.pop('phone_number', None)
        if phone_number:
            phone_number = phone_number

        user = User.objects.create_user(phone_number=phone_number, attached_region=attached_region,
                                        **validated_data)
        for group in groups:
            user.groups.add(group)
        # try sending email

        secr = hashlib.sha512(user.username.encode("utf-8")).hexdigest()
        secr = base64.b32encode(secr.encode("utf-8"))
        totp = pyotp.TOTP(secr)
        otp = totp.now()
        user.otp = otp
        user.save()
        message = get_template("confirm_email.html").render(
            {
                'username': str(user.username),
                'otp': str(user.otp),
                'app_url': APP_URL
            })
        send_mail(
            subject='Confirm Your Email Address',
            html_message=message,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True
        )
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        try:
            staff_number = validated_data.pop('staff_number')
        except KeyError:
            pass
        if not self.context['request'].user.is_staff:
            # cannot add groups since user is not admin
            groups = None
        try:
            attached_region = validated_data.pop('attached_region_id')
        except:
            attached_region = ''

        user = super().update(instance, validated_data)
        if attached_region != '':
            user.attached_region = attached_region
            user.save()

        if password:
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()

        if groups is not None:
            user.groups.clear()
            for group in groups:
                user.groups.add(group)

        return user


class ProfileRecommendationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = ProfileRecommendation
        fields = ['profile', 'comment', 'author']

    def create(self, validated_data):
        author = self.context['request'].user
        recommendation = ProfileRecommendation.objects.create(author=author, **validated_data)
        recommendation.save()
        return recommendation


class AbstractDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractDocument
        fields = '__all__'

    def create(self, validated_data):
        document = validated_data.pop('document')
        now = timezone.now()
        reformatted_filename = f"{now:%Y%m%d%H%M%s}" + ''.join(document.name.strip()).replace(' ', '')
        document.name = reformatted_filename
        abstract_doc_record = AbstractDocument.objects.create(**validated_data)
        abstract_doc_record.document = document
        abstract_doc_record.save()
        return abstract_doc_record

    def update(self, instance, validated_data):
        document = validated_data.pop('document', None)
        abs_document = super().update(instance, validated_data)
        if document is not None:
            now = timezone.now()
            reformatted_filename = f"{now:%Y%m%d%H%M%s}" + ''.join(document.name.strip()).replace(' ', '')
            document.name = reformatted_filename
            abs_document.document = document
        abs_document.save()
        return abs_document


class ProfileCVSerializer(serializers.ModelSerializer):
    cv = serializers.FileField(max_length=None, allow_empty_file=False)
    cv_upload_status = serializers.SerializerMethodField('get_cv_upload_status',
                                                         read_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Profile.objects.all())

    def get_cv_upload_status(self, obj):
        return True if obj.cv else False

    class Meta:
        model = Profile
        fields = [
            'cv', 'cv_upload_status', 'profile_id']

    def create(self, validated_data):
        cv = validated_data.pop('cv')
        now = timezone.now()
        reformatted_filename = f"{now:%Y%m%d%H%M%s}" + ''.join(cv.name.strip()).replace(' ', '')
        cv.name = reformatted_filename
        print(cv)
        profile = validated_data.pop('profile_id')
        profile.cv = cv
        profile.save()
        return Profile


class ProfileSerializer(serializers.ModelSerializer):
    detailed_experience = serializers.SerializerMethodField('get_detailed_experience', read_only=True)
    languages = serializers.SerializerMethodField('get_languages', read_only=True)
    occupation = OccupationSerializer(read_only=True)
    occupation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Occupation.objects.all())
    region_of_residence = RegionSerializer(read_only=True)
    region_of_residence_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Region.objects.all())
    competencies_objects = serializers.SerializerMethodField('get_competencies_objects',
                                                             read_only=True)

    competencies = serializers.PrimaryKeyRelatedField(queryset=Competence.objects.all(),
                                                      many=True)

    recommendations = ProfileRecommendationSerializer(many=True, read_only=True)

    cv_upload_status = serializers.SerializerMethodField('get_cv_upload_status',
                                                         read_only=True)
    active_deployments = serializers.SerializerMethodField('get_active_deployments', read_only=True)
    current_deployment = serializers.SerializerMethodField('get_current_deployment', read_only=True)

    def get_detailed_experience(self, obj):
        return []

    def get_languages(self, obj):
        return []

    def get_cv_upload_status(self, obj):
        return True if obj.cv else False

    def get_active_deployments(self, obj):
        active_deployments = ProfileDeployment.objects.filter(profile=obj.id, status='initiated').count()
        return active_deployments

    def get_current_deployment(self, obj):
        current_deployment = ProfileDeployment.objects.filter(profile=obj.id, status='initiated').first()
        return current_deployment.outbreak.name if current_deployment is not None else 'No Active Deployment'

    class Meta:
        model = Profile
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'gender', 'religion', 'occupation',
            'occupation_id', 'date_of_birth', 'next_of_kin', "passport_photo",
            'email', 'phone', 'user', 'id_type', 'id_number', 'region_of_residence',
            'region_of_residence_id', 'cv', 'cv_upload_status', 'active', 'available', 'note',
            'application_status', 'competencies', 'other_occupation', 'competencies_objects', 'recommendations',
            'active_deployments', 'current_deployment', 'references', 'languages', 'professional_experience',
            'detailed_experience', 'managerial_experience', 'previous_deployment_experience'
        ]
        extra_kwargs = {
            'cv': {'write_only': True}
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Profile.objects.all(),
                fields=['id_type', 'id_number']
            )
        ]

    def get_competencies_objects(self, obj):
        return []

    def validate(self, data):
        try:
            date_of_birth = data['date_of_birth']
            age = datetime.date.today() - date_of_birth
            if age < datetime.timedelta(days=18 * 365) or datetime.timedelta(days=75 * 365) < age:
                raise serializers.ValidationError({"date_of_birth": "age must be between 18 and 75"})
            return data
        except KeyError:
            return data

    def create(self, validated_data):
        competencies = validated_data.pop('competencies', None)
        occupation = validated_data.pop('occupation_id')
        region_of_residence = validated_data.pop('region_of_residence_id')
        validated_data.pop('user', None)

        user_account = self.context['request'].user
        print("user level", user_account.level)
        if user_account.level == 'rde':
            print("user is rde")
            profile = Profile.objects.create(occupation=occupation,
                                             region_of_residence=region_of_residence,
                                             **validated_data)
            profile.save()
            profile.user = user_account
            profile.save()
        else:
            print("user is admin")
            profile = Profile.objects.create(occupation=occupation, region_of_residence=region_of_residence,
                                             **validated_data)
            profile.save()

        if competencies is not None:
            for competence in competencies:
                profile.competencies.add(competence)

        return profile

    def update(self, instance, validated_data):
        competencies = validated_data.pop('competencies_list', None)
        occupation = validated_data.pop('occupation_id', instance.occupation)
        region_of_residence = validated_data.pop('region_of_residence_id', instance.region_of_residence)

        profile = super().update(instance, validated_data)
        profile.occupation = occupation
        profile.region_of_residence = region_of_residence
        profile.save()
        if competencies is not None:
            profile.competencies.clear()
            for competence in competencies:
                profile.competencies.add(competence)
        return profile


class ProfileLanguageSerializer(serializers.ModelSerializer):
    language_name = serializers.SerializerMethodField('get_language_name', read_only=True)

    def get_language_name(self, obj):
        if obj.language is not None:
            return obj.language.name
        else:
            return ''

    class Meta:
        model = ProfileLanguage
        fields = "__all__"


class ProfileAcademicQualificationSerializer(serializers.HyperlinkedModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    qualification_type = AcademicQualificationTypeSerializer(read_only=True)

    qualification_type_id = serializers.PrimaryKeyRelatedField(write_only=True,
                                                               queryset=AcademicQualificationType.objects.all())
    profile = serializers.HyperlinkedRelatedField(
        view_name='profile-detail',
        read_only=True
    )

    class Meta:
        model = ProfileAcademicQualification
        fields = ['id', 'qualification_type', 'profile_id', 'start_date', 'end_date',
                  'field_of_study', 'institution', 'qualification_type_id', 'profile']

    def validate(self, data):
        """
        check if start date is before end date
        :param data:
        :return: true/false
        """
        try:
            data['start_date']
        except KeyError:
            return data
        try:
            data['end_date']
        except KeyError:
            return data
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('end date has to be later than start date')
        return data

    def create(self, validated_data):
        profile = validated_data.pop('profile_id', None)
        qualification_type = validated_data.pop('qualification_type_id', None)
        profile_academic_qualification = ProfileAcademicQualification.objects.create(
            profile=profile,
            qualification_type=qualification_type,
            **validated_data)
        profile_academic_qualification.save()
        return profile_academic_qualification

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile_id', instance.profile)
        qualification_type = validated_data.pop('qualification_type_id', instance.qualification_type)

        profile_academic_qualification = super().update(instance, validated_data)
        profile_academic_qualification.save()
        profile_academic_qualification.profile = profile
        profile_academic_qualification.profile_academic_qualification = qualification_type
        return profile_academic_qualification


class OutbreakTypeSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)

    class Meta:
        model = OutbreakType
        fields = ['value', 'label']

    def get_value(self, obj):
        return obj.id


class OutbreakReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbreak
        fields = ['report', 'id']


class OutbreakSerializer(serializers.ModelSerializer):
    competencies_objects = serializers.SerializerMethodField('get_competencies_objects',
                                                             read_only=True)
    competencies = serializers.PrimaryKeyRelatedField(queryset=Competence.objects.all(),
                                                      many=True)
    affected_regions_objects = serializers.SerializerMethodField('get_affected_regions_objects', read_only=True)
    affected_regions = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(),
                                                          many=True)
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)
    profiles = ProfileSerializer(many=True, read_only=True)

    outbreak_type = OutbreakTypeSerializer(read_only=True)

    outbreak_type_id = serializers.PrimaryKeyRelatedField(queryset=OutbreakType.objects.all())

    class Meta:
        model = Outbreak
        fields = ['id', 'name', 'description', 'competencies', 'competencies_objects', 'severity',
                  'start_date',
                  'end_date', 'affected_regions', 'affected_regions_objects', 'value', 'label', 'profiles',
                  'outbreak_type_id', 'outbreak_type', 'general_information', 'detailed_information',
                  'eligibility_criteria', 'requirements', 'other_information', 'report']

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name

    def get_competencies_objects(self, obj):
        return CompetenceSerializer(obj.competencies, many=True).data

    def get_affected_regions_objects(self, obj):
        return RegionSerializer(obj.affected_regions, many=True).data

    def create(self, validated_data):
        competencies_list = validated_data.pop('competencies', None)
        outbreak_type = validated_data.pop('outbreak_type_id', None)
        affected_regions = validated_data.pop('affected_regions', None)
        outbreak = Outbreak.objects.create(outbreak_type=outbreak_type, **validated_data)
        outbreak.save()
        if affected_regions is not None:
            for affected_region in affected_regions:
                outbreak.affected_regions.add(affected_region)

        if competencies_list is not None:
            for competence in competencies_list:
                outbreak.competencies.add(competence)
        return outbreak

    def update(self, instance, validated_data):
        competencies_list = validated_data.pop('competencies', None)
        affected_regions = validated_data.pop('affected_regions', None)
        outbreak_type = validated_data.pop('outbreak_type_id', None)
        outbreak = super().update(instance, validated_data)
        outbreak.outbreak_type = outbreak_type
        outbreak.save()
        if affected_regions is not None:
            outbreak.affected_regions.clear()
            for affected_region in affected_regions:
                outbreak.affected_regions.add(affected_region)

        if competencies_list is not None:
            outbreak.competencies.clear()
            for competence in competencies_list:
                outbreak.competencies.add(competence)
        return outbreak


class OutbreakOptionsSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Outbreak
        fields = ['value', 'label']

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ProfileDeploymentMiniSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer('get_profile_object',
                                read_only=True)

    class Meta:
        model = ProfileDeployment
        fields = ['id', 'outbreak', 'start_date', 'end_date', 'profile',
                  'status', 'region', 'deployment_report']


class ProfileDeploymentSerializer(serializers.ModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Profile.objects.all())
    outbreak = OutbreakSerializer(read_only=True)
    outbreak_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Outbreak.objects.all())
    region_object = serializers.SerializerMethodField('get_region_object',
                                                      read_only=True)

    class Meta:
        model = ProfileDeployment
        fields = ['id', 'outbreak', 'start_date', 'end_date', 'profile_id', 'outbreak_id', 'status', 'region',
                  'region_object', 'accepted_by_user', 'rejected_by_user', 'deployment_report']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            profile = data['profile_id']
            deployment_count = profile.deployments.filter(status='initiated').count()
            if deployment_count > 0:
                raise serializers.ValidationError({'generic': 'This RDE already has an active deployment'})
        return data

    def get_region_object(self, obj):
        return RegionSerializer(obj.region).data

    def create(self, validated_data):
        profile = validated_data.pop('profile_id')
        outbreak = validated_data.pop('outbreak_id')
        region = validated_data.pop('region')
        if region not in outbreak.affected_regions.all():
            raise serializers.ValidationError({'region': 'This region does not exist in the list of affected regions'})
        deployment = ProfileDeployment.objects.create(profile=profile, region=region, outbreak=outbreak,
                                                      **validated_data)

        deployment.save()
        return deployment

    def update(self, instance, validated_data):
        outbreak = validated_data.pop('outbreak_id', None)
        region = validated_data.pop('region', None)
        deployment = super().update(instance, validated_data)
        if region is not None:
            if outbreak is None:
                outbreak = deployment.outbreak
            else:
                deployment.outbreak = outbreak
            if region not in outbreak.affected_regions:
                raise serializers.ValidationError(
                    {'region': 'This region does not exist in the list of affected regions'})

        deployment.save()
        return deployment


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.get_full_name()
        token['username'] = user.username
        token['email_verified'] = user.email_verified
        token['id'] = user.id
        token['level'] = user.level
        token[
            'region'] = f"{user.attached_region.country.name} ,{user.attached_region.name}" if user.attached_region else ""
        token['roles'] = [group.name for group in user.groups.all()]
        token['is_superuser'] = user.is_superuser
        return token
