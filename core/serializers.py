import base64
import hashlib
import pyotp

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import Occupation, Country, Region, Competence, Profile, ProfileRecommendation, Outbreak, \
    ProfileDeployment, User, OccupationCategory, OutbreakType, AcademicQualificationType, ProfileAcademicQualification
from eac_rde_backend.settings import EMAIL_HOST_USER, APP_URL


class CountrySerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Country
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name


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
                  'password', 'phone_number', 'groups', 'groups_objects',
                  'staff_number', 'attached_region_id', 'attached_region', 'email']

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
        user.otp=otp
        user.save()
        print("link", f"{APP_URL}api/{str(user.username)}/{str(user.otp)}")
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
        profile_id = validated_data.profile_id
        profile = Profile.objects.get(pk=profile_id)
        profile.cv = cv
        profile.save()
        return Profile


class ProfileSerializer(serializers.ModelSerializer):
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

    def get_cv_upload_status(self, obj):
        return True if obj.cv else False

    def get_active_deployments(self, obj):
        active_deployments = ProfileDeployment.objects.filter(profile=obj.id, status='initiated').count()
        return active_deployments

    class Meta:
        model = Profile
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'gender', 'occupation',
            'occupation_id', 'date_of_birth', 'next_of_kin',
            'email', 'phone', 'user', 'id_type', 'id_number', 'region_of_residence',
            'region_of_residence_id', 'cv', 'cv_upload_status', 'active', 'available', 'note',
            'application_status', 'competencies', 'competencies_objects', 'recommendations',
            'active_deployments', 'references', 'professional_experience'
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
        return CompetenceSerializer(obj.competencies, many=True).data

    def validate(self, data):
        user = self.context['request'].user
        if not (user.is_staff or user.is_superuser):
            profiles = Profile.objects.filter(user=user)
            if len(profiles) > 0:
                raise serializers.ValidationError('This user already has a profile')

        return super().validate(data)

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
        profile = super().update(instance, validated_data)
        profile.save()
        if competencies is not None:
            profile.competencies.clear()
            for competence in competencies:
                profile.competencies.add(competence)
        return profile


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

    outbreak_type_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=OutbreakType.objects.all())

    class Meta:
        model = Outbreak
        fields = ['id', 'name', 'description', 'competencies', 'competencies_objects', 'severity',
                  'start_date',
                  'end_date', 'affected_regions', 'affected_regions_objects', 'value', 'label', 'profiles',
                  'outbreak_type_id', 'outbreak_type', 'general_information', 'detailed_information',
                  'eligibility_criteria', 'requirements', 'other_information']

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
        affected_regions = validated_data.pop('affected_regions', None)
        outbreak = Outbreak.objects.create(**validated_data)
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
        outbreak = super().update(instance, validated_data)
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
        fields = ['id', 'outbreak', 'start_date', 'end_date', 'profile', 'status', 'region',
                  ]


class ProfileDeploymentSerializer(serializers.ModelSerializer):
    profile_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Profile.objects.all())
    outbreak = OutbreakSerializer(read_only=True)
    outbreak_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Outbreak.objects.all())
    region_object = serializers.SerializerMethodField('get_region_object',
                                                      read_only=True)

    class Meta:
        model = ProfileDeployment
        fields = ['id', 'outbreak', 'start_date', 'end_date', 'profile_id', 'outbreak_id', 'status', 'region',
                  'region_object',]

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
        token['id'] = user.id
        token['level'] = user.level
        token[
            'region'] = f"{user.attached_region.country.name} ,{user.attached_region.name}" if user.attached_region else ""
        token['roles'] = [group.name for group in user.groups.all()]
        token['is_superuser'] = user.is_superuser
        return token
