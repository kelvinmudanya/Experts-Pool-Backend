from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    r'^\+?[0-9- ]{8,15}$', "Enter a valid phone number.")


class TimeStampedModel(models.Model):
    """Abstract model for created_at & updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for TimeStampedModel."""

        abstract = True


LEVEL = (
    ('country', 'Country'),
    ('eac', 'EAC'),
    ('rde', 'RDE')
)


class Country(models.Model):
    """Model definition for Country."""

    name = models.CharField(max_length=50)
    phone_code = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Country."""

        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        """Unicode representation of Country."""
        return self.name


class Region(TimeStampedModel):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"Region {self.name}, in {self.country}"


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, validators=[
        phone_validator], blank=True, null=True)
    staff_number = models.CharField(max_length=30, unique=True,
                                    blank=True, null=True)
    level = models.CharField(max_length=50, choices=LEVEL, blank=True, null=True, default='rde')
    attached_region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    other_region = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(default=1234, max_length=255)
    otp_used = models.BooleanField(default=False)
    email = models.EmailField(unique=True, max_length=255)


COMPETENCE_TYPES = (
    ('language', 'LANGUAGE'),
    ('work', 'WORK')
)


class Competence(TimeStampedModel):
    name = models.CharField(max_length=255)
    type = models.CharField(choices=COMPETENCE_TYPES, max_length=100, default='work')

    class Meta:
        """Meta definition for Competence."""

        verbose_name = 'Competence'
        verbose_name_plural = 'Competencies'

    def __str__(self):
        return f"{self.name}"


class OccupationCategory(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        """Meta definition for Occupation Category."""

        verbose_name = 'Occupation Category'
        verbose_name_plural = 'Occupation Categories'


class Occupation(TimeStampedModel):
    name = models.CharField(max_length=255)
    occupation_category = models.ForeignKey(OccupationCategory, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        """Meta definition for Occupation."""

        verbose_name = 'Occupation'
        verbose_name_plural = 'Occupations'


ID_TYPES = (
    ('alien_id', 'Alien ID'),
    ('birth_cert', 'Birth Certificate'),
    ('military_id', 'Military ID'),
    ('national_id', 'National ID'),
    ('passport', 'Passport'),
)

GENDER_TYPES = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Other'),
)

APPLICATION_STATUS = (
    ('pending_approval', 'Pending Approval'),
    ('approval_complete', 'Approval Complete'),
    ('rejected', 'Rejected')
)


class AcademicQualificationType(TimeStampedModel):
    degree_level = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.degree_level.capitalize()}"


class Profile(TimeStampedModel):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER_TYPES, max_length=1)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL,
                                   blank=True, null=True)

    date_of_birth = models.DateField()
    next_of_kin = models.JSONField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, validators=[phone_validator],
                             null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name='profile')
    id_type = models.CharField(max_length=100, choices=ID_TYPES)
    id_number = models.CharField(max_length=255)
    region_of_residence = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    cv = models.FileField(blank=True, null=True, upload_to='cvs/%Y/%m/%d/')
    active = models.BooleanField(default=True)
    available = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    religion = models.CharField(max_length=150, null=True, blank=True)
    application_status = models.CharField(max_length=255, choices=APPLICATION_STATUS, default='pending_approval')
    competencies = models.ManyToManyField(Competence)
    references = models.JSONField(blank=True, null=True)
    professional_experience = models.JSONField(blank=True, null=True)
    previous_deployment_experience = models.JSONField(blank=True, null=True)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        constraints = [
            models.UniqueConstraint(
                fields=['id_type', 'id_number'], name='unique_id')
        ]

    def __str__(self):
        return f"RDE {self.first_name}, {self.last_name} - resides in " \
               f"{self.region_of_residence}. Application is {self.application_status}"


class ProfileAcademicQualification(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_academic_qualifications')
    qualification_type = models.ForeignKey(AcademicQualificationType, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    field_of_study = models.CharField(max_length=500)
    institution = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name}'s {self.qualification_type.degree_level} in {self.field_of_study} at {self.institution}"


class ProfileRecommendation(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recommendations')
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')


OUTBREAK_SEVERITY = (
    ('minor', 'Minor'),
    ('medium', 'Medium'),
    ('severe', 'Severe')
)


class OutbreakType(TimeStampedModel):
    label = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.label}"


class Outbreak(TimeStampedModel):
    """
    Defines an event of public health concern.
    Below is the proposed structure of the JSON Fields in this model

    "general_information":{
        "type":"onsite/offsite",
        "reserved_for_pwds":"true/false"
    }
    "detailed_information":{
        "mission_and_objectives":"",
        "task_description":""
    }
    "eligibility_creteria":{
        "age":"",
        "nationality":""
    }
    "requirements":{
        "required_experience":"",
        "areas_of_expertise":"",
        "languages":"",
        "required_education_level":"",
        "competencies_and_values":"",
        "driving_license":""
    }
    "other_information":{
        "living_conditions_and_remarks":"",
        "inclusivity_statement":""
    }
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    competencies = models.ManyToManyField(Competence, blank=True, related_name="outbreaks")
    severity = models.CharField(max_length=255, choices=OUTBREAK_SEVERITY)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    affected_regions = models.ManyToManyField(Region)
    outbreak_type = models.ForeignKey(OutbreakType, null=True, blank=True, on_delete=models.SET_NULL)
    general_information = models.JSONField(null=True, blank=True)
    detailed_information = models.JSONField(null=True, blank=True)
    eligibility_criteria = models.TextField(null=True, blank=True)
    requirements = models.JSONField(null=True, blank=True)
    other_information = models.JSONField(null=True, blank=True)
    report = models.FileField(blank=True, null=True, upload_to='outbreak_reports/%Y/%m/%d/')

    def __str__(self):
        return f"{self.name}"


deployment_status = (
    ('initiated', 'Initiated'),
    ('ended', 'Ended')
)


class ProfileDeployment(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='deployments')
    outbreak = models.ForeignKey(Outbreak, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=deployment_status, default='initiated')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
    accepted_by_user = models.BooleanField(null=True, default=False)
    rejected_by_user = models.BooleanField(null=True, default=False)
    deployment_report = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"Deployment for {self.profile} is deployed on outbreak {self.outbreak}"


class AbstractDocument(TimeStampedModel):
    """
    Stores documents tha the EAC may need to upload that are not related to
    any public health event
    """
    name = models.CharField(max_length=255)  # name of the document
    document = models.FileField(upload_to='abstract_reports/%Y/%m/%d/')
