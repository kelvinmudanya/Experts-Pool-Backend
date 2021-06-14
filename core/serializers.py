from rest_framework import serializers

from core.models import Occupation, Country, Region, Competence, Profile, ProfileRecommendation, Outbreak, \
    ProfileDeployment


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competence
        fields = '__all__'


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    occupation = OccupationSerializer(read_only=True)
    occupation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Occupation.objects.all())
    region_of_residence = RegionSerializer(read_only=True)
    region_of_residence_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Region.objects.all())

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'gender',
            'occupation',
            'occupation_id'
            'date_of_birth',
            'next_of_kin_name',
            'next_of_kin_phone',
            'email',
            'phone',
            'user',
            'id_type',
            'id_number',
            'region_of_residence',
            'region_of_residence_id'
            'cv',
            'active',
            'available',
            'note',
            'application_status',
            'competencies',
        ]


class ProfileRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileRecommendation
        fields = '__all__'


class OutbreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbreak
        fields = '__all__'


class ProfileDeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileDeployment
        fields = '__all__'
