from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from core.models import User, Country, Region, Competence, Occupation, Profile, \
    ProfileRecommendation, Outbreak, ProfileDeployment


# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         ("Other Fields", {'fields': ('phone_number', 'staff_number', 'level',
#                                      'attached_region')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ("Other Fields", {'fields': ('phone_number', 'staff_number', 'level', 'attached_region')}),
#     )

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Other Fields", {'fields': ('phone_number', 'staff_number', 'level',
                                     'attached_region')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Other Fields", {
         'fields': ('phone_number', 'staff_number', 'level', 'attached_region')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Competence)
admin.site.register(Occupation)
admin.site.register(Profile)
admin.site.register(ProfileRecommendation)
admin.site.register(Outbreak)
admin.site.register(ProfileDeployment)
