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
    class Meta:
        model = Profile
        fields = '__all__'


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
