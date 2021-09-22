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
    level = models.CharField(max_length=50, choices=LEVEL, default='rde')
    attached_region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.CASCADE)


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


class Occupation(TimeStampedModel):
    name = models.CharField(max_length=255)

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
    ('T', 'Transgender'),
    ('O', 'Other'),
)

APPLICATION_STATUS = (
    ('pending_approval', 'Pending Approval'),
    ('approved_by_partner_state', 'Approved By Partner State'),
    ('approval_complete', 'Approval Complete'),
    ('rejected', 'Rejected')
)


class Profile(TimeStampedModel):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER_TYPES, max_length=1)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL,
                                   blank=True, null=True)

    date_of_birth = models.DateField()
    next_of_kin_name = models.CharField(max_length=30)
    next_of_kin_phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, validators=[phone_validator],
                             null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name='profile')
    id_type = models.CharField(max_length=100, choices=ID_TYPES)
    id_number = models.CharField(max_length=255)
    region_of_residence = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    # cv = models.FileField(upload_to='uploads/%Y/%m/%d/', black=True)
    cv = models.TextField(null=True)
    active = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    application_status = models.CharField(max_length=255, choices=APPLICATION_STATUS, default='pending_approval')
    competencies = models.ManyToManyField(Competence)

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


class ProfileRecommendation(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recommendations')
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')


OUTBREAK_SEVERITY = (
    ('minor', 'Minor'),
    ('medium', 'Medium'),
    ('severe', 'Severe')
)


class Outbreak(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    competencies = models.ManyToManyField(Competence, blank=True, related_name="outbreaks")
    severity = models.CharField(max_length=255, choices=OUTBREAK_SEVERITY)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    affected_regions = models.ManyToManyField(Region)


deployment_status = (
    ('initiated', 'Initiated'),
    ('ended', 'Ended')
)


class ProfileDeployment(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='deployments')
    outbreak = models.ForeignKey(Outbreak, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=deployment_status, default='initiated')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default=1)
