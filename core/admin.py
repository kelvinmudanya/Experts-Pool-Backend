from django.contrib import admin

# Register your models here.
from core.models import User, Country, Region, Competence, Occupation, Profile, \
    ProfileRecommendation, Outbreak, ProfileDeployment

admin.site.register(User)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Competence)
admin.site.register(Occupation)
admin.site.register(Profile)
admin.site.register(ProfileRecommendation)
admin.site.register(Outbreak)
admin.site.register(ProfileDeployment)