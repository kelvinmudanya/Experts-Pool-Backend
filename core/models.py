from django.db import models


class TimeStampedModel(models.Model):
    """Abstract model for created_at & updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for TimeStampedModel."""

        abstract = True


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, validators=[
        phone_validator], blank=True, null=True)
    staff_number = models.CharField(max_length=30, unique=True,
                                    blank=True, null=True)

    id_number = models.CharField(max_length=30, blank=True, null=True)


class UserOTP(TimeStampedModel):
    """A user's OTP token."""

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="otp")
    otp = models.CharField(max_length=10, blank=True, null=True)
    # To prevent replay attacks
    used = models.BooleanField(default=False)

    class Meta:
        """Meta definition for UserOTP."""

        verbose_name = 'User OTP'
        verbose_name_plural = 'User OTPs'

    def __str__(self):
        """Unicode representation of UserOTP."""
        return f"{self.user}'s OTP"


APPLICATION_STATUS = (
    ('pending_approval', 'Pending Approval')
    ('approved', 'Approved')
    ('rejected', 'Rejected')
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


class Competence(TimeStampedModel):
    name = models.CharField(max_length=255)


class Occupation(TimeStampedModel):
    name = models.CharField(max_length=255)


ID_TYPES = (
    ('alien_id', 'Alien ID'),
    ('birth_cert', 'Birth Certificate'),
    ('military_id', 'Military ID'),
    ('national_id', 'National ID'),
    ('passport', 'Passport'),
)


class Profile:
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER_TYPES, max_length=1)
    religion = models.CharField(choices=RELIGIONS, max_length=30)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL,
                                   blank=True, null=True)

    date_of_birth = models.DateField()
    next_of_kin_name = models.CharField(max_length=30)
    next_of_kin_phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, validators=[phone_validator],
                             blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                blank=True, null=True)
    id_type = models.CharField(max_length=100, choices=ID_TYPES)
    id_number = models.CharField(max_length=255)

    active = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    APPLICATION_STATUS = models.CharField(max_length=255, choices=APPLICATION_STATUS)
    competencies = models.ManyToManyField(Competence, blank=True, on_delete=models.SET_NULL)


# class ProfileRecommendation(TimeStampedModel):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     comment = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)

class Outbreak(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    competencies = models.ManyToManyField(Competence, blank=True, on_delete=models.CASCADE)
