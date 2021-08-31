from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.models import Occupation, Country, Region, Competence, Profile, ProfileRecommendation, Outbreak, \
    ProfileDeployment, User


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
        return obj.name


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


class OccupationSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField('get_value',
                                              read_only=True)
    label = serializers.SerializerMethodField('get_label',
                                              read_only=True)

    class Meta:
        model = Occupation
        fields = '__all__'

    def get_value(self, obj):
        return obj.id

    def get_label(self, obj):
        return obj.name


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

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'password', 'phone_number', 'groups', 'groups_objects', 'staff_number']

    def get_groups_objects(self, obj):
        return GroupSerializer(obj.groups, many=True).data

    def create(self, validated_data):
        groups = validated_data.pop('groups')
        # try:
        #     staff_number = validated_data.pop('staff_number')
        # except:
        #     staff_number = ''
        if not self.context['request'].user.is_staff:
            # cannot add groups since user is not admin
            groups = []
            staff_number = ''

        phone_number = validated_data.pop('phone_number', None)
        if phone_number:
            phone_number = phone_number

        user = User.objects.create_user(phone_number=phone_number,
                                        **validated_data)
        for group in groups:
            user.groups.add(group)

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

        user = super().update(instance, validated_data)
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

    class Meta:
        model = Profile
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'gender', 'occupation',
            'occupation_id', 'date_of_birth', 'next_of_kin_name', 'next_of_kin_phone',
            'email', 'phone', 'user', 'id_type', 'id_number', 'region_of_residence',
            'region_of_residence_id', 'cv', 'active', 'available', 'note',
            'application_status', 'competencies', 'competencies_objects', 'recommendations',
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
        user = validated_data.pop('user', None)

        user_account = self.context['request'].user

        if not (user_account.is_staff or user_account.is_superuser):
            profile = Profile.objects.create(occupation=occupation, region_of_residence=region_of_residence,
                                             **validated_data)
        else:
            if user is not None:
                profile = Profile.objects.create(occupation=occupation, user=user,
                                                 region_of_residence=region_of_residence,
                                                 **validated_data)
            else:
                profile = Profile.objects.create(occupation=occupation,
                                                 region_of_residence=region_of_residence,
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

    class Meta:
        model = Outbreak
        fields = ['id', 'name', 'description', 'competencies', 'competencies_objects', 'severity',
                  'start_date',
                  'end_date', 'affected_regions', 'affected_regions_objects', 'value', 'label']

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


class ProfileDeploymentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Profile.objects.all())
    outbreak = OutbreakSerializer(read_only=True)
    outbreak_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Outbreak.objects.all())

    class Meta:
        model = ProfileDeployment
        fields = ['id', 'profile', 'outbreak', 'start_date', 'end_date', 'profile_id', 'outbreak_id']

    def create(self, validated_data):
        profile = validated_data.pop('profile_id')
        outbreak = validated_data.pop('outbreak_id')
        deployment = ProfileDeployment.objects.create(profile=profile, outbreak=outbreak, **validated_data)
        deployment.save()
        return deployment

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile_id')
        outbreak = validated_data.pop('outbreak_id')
        deployment = super().update(instance, validated_data)
        deployment.profile = profile
        deployment.outbreak = outbreak
        deployment.save()
        return deployment
