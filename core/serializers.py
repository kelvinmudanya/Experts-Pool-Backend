from rest_framework import serializers

from core.models import Occupation, Country, Region, Competence, Profile, ProfileRecommendation, Outbreak, \
    ProfileDeployment


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
    competencies = CompetenceSerializer(read_only=True, many=True)
    competencies_list = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Competence, many=True)

    class Meta:
        model = Profile
        fields = [
            'first_name', 'middle_name', 'last_name', 'gender', 'occupation',
            'occupation_id', 'date_of_birth', 'next_of_kin_name', 'next_of_kin_phone',
            'email', 'phone', 'user', 'id_type', 'id_number', 'region_of_residence',
            'region_of_residence_id', 'cv', 'active', 'available', 'note',
            'application_status', 'competencies', 'competencies_list'
        ]

    def create(self, validated_data):
        competencies = validated_data.pop('competencies_list', None)
        profile = Profile.objects.create(**validated_data)
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


class ProfileRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileRecommendation
        fields = '__all__'


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
