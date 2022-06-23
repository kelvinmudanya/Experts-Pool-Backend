from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from core.models import User, Country, Region, Competence, Occupation, Profile, \
    ProfileRecommendation, Outbreak, ProfileDeployment, OccupationCategory, AcademicQualificationType, \
    ProfileAcademicQualification, OutbreakType, AbstractDocument, Specialization, DetailedExperience


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Other Fields", {'fields': ('phone_number', 'staff_number', 'level',
                                     'attached_region', 'otp', 'otp_used', 'email_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Other Fields", {'fields': ('phone_number', 'staff_number', 'level',
                                     'attached_region', 'otp', 'otp_used', 'email_verified')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Country)
admin.site.register(OccupationCategory)
admin.site.register(Region)
admin.site.register(Competence)
admin.site.register(Specialization)
admin.site.register(Occupation)
admin.site.register(AcademicQualificationType)
admin.site.register(Profile)
admin.site.register(DetailedExperience)
admin.site.register(ProfileAcademicQualification)
admin.site.register(ProfileRecommendation)
admin.site.register(Outbreak)
admin.site.register(OutbreakType)
admin.site.register(AbstractDocument)
admin.site.register(ProfileDeployment)
