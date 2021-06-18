from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from core.models import Occupation, Country, Region, Competence, Profile, ProfileRecommendation, Outbreak, \
    ProfileDeployment, User


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Country.objects.all())

    class Meta:
        model = Region
        fields = ['name', 'country', 'country_id']

    def create(self, validated_data):
        country = validated_data.pop('country_id')
        region = Region.objects.create(country=country, **validated_data)
        region.save()
        return region


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password',
                                                                            'placeholder': 'Password'})
    groups = GroupSerializer(read_only=True, many=True)
    groups_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                                   write_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username',
                  'password', 'phone_number', 'groups', 'groups_id', 'staff_number']

    def validate(self, data):
        try:
            groups = data['groups_id']
            auth_user = self.context['request'].user
            if not auth_user.is_staff:
                # cannot add groups since user is not admin
                data.pop('groups_id')
        except KeyError:
            pass

    def create(self, validated_data):
        groups = validated_data.pop('groups_id')

        phone_number = validated_data.pop('phone_number', None)
        if phone_number:
            phone_number = phone_number

        user = User.objects.create_user(phone_number=phone_number,
                                        **validated_data)
        for group in groups:
            user.groups.add(group)

        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups_id', None)
        password = validated_data.pop('password', None)
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
    competencies = CompetenceSerializer(read_only=True, many=True)
    competencies_list = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Competence.objects.all(),
                                                           many=True)

    recommendations = ProfileRecommendationSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'occupation',
            'occupation_id', 'date_of_birth', 'next_of_kin_name', 'next_of_kin_phone',
            'email', 'phone', 'user', 'id_type', 'id_number', 'region_of_residence',
            'region_of_residence_id', 'cv', 'active', 'available', 'note',
            'application_status', 'competencies', 'competencies_list', 'recommendations',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Profile.objects.all(),
                fields=['id_type', 'id_number']
            )
        ]

    def validate(self, data):
        user = self.context['request'].user
        if not (user.is_staff or user.is_superuser):
            profiles = Profile.objects.filter(user=user)
            if len(profiles) > 0:
                raise serializers.ValidationError('This user already has a profile')

        return super().validate(data)

    def create(self, validated_data):
        competencies = validated_data.pop('competencies_list', None)
        occupation = validated_data.pop('occupation_id')
        region_of_residence = validated_data.pop('region_of_residence_id')
        auth_user = None
        user = self.context['request'].user


        profile = Profile.objects.create(occupation=occupation, user=user, region_of_residence=region_of_residence,
                                         **validated_data)
        profile.save()
        if competencies is not None:
            for competence in competencies:
                profile.competencies.add(competence)

        return profile

    def update(self, instance, validated_data):
        competencies = validated_data.pop('competencies_list', None)
        profile = super().update(instance, **validated_data)
        profile.save()
        if competencies is not None:
            for competence in competencies:
                profile.competencies.add(competence)
        return


class OutbreakSerializer(serializers.ModelSerializer):
    competencies = CompetenceSerializer(read_only=True, many=True)
    competencies_list = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Competence.objects.all(),
                                                           many=True, )
    affected_regions = RegionSerializer(read_only=True, many=True)
    affected_regions_list = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Region.objects.all(),
                                                               many=True, )

    class Meta:
        model = Outbreak
        fields = ['name', 'description', 'competencies', 'competencies_list', 'severity', 'start_date', 'end_date',
                  'affected_regions', 'affected_regions_list']

    def create(self, validated_data):
        competencies_list = validated_data.pop('competencies_list', None)
        affected_regions = validated_data.pop('affected_regions_list', None)
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
        competencies_list = validated_data.pop('competencies_list', None)
        affected_regions = validated_data.pop('affected_regions_list', None)
        outbreak = super().update(instance, **validated_data)
        outbreak.save()
        if affected_regions is not None:
            for affected_region in affected_regions:
                outbreak.affected_regions.add(affected_region)

        if competencies_list is not None:
            for competence in competencies_list:
                outbreak.competencies.add(competence)
        return outbreak


class ProfileDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileDeployment
        fields = '__all__'
