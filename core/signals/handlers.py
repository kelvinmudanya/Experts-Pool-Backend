from django.core.mail import send_mail
from django.db.models import signals
from django.dispatch import receiver
from django.template.loader import get_template

from core.models import Country, ProfileRecommendation, ProfileDeployment
from eac_rde_backend.settings import EMAIL_HOST_USER, WEB_APP_URL


@receiver(signals.post_save, sender=Country)
def country_created(sender, instance, **kwargs):
    print("created", str(sender.name), str(instance.name), str(instance.phone_code))


@receiver(signals.post_save, sender=ProfileRecommendation)
def profile_recommendation_saved(sender, instance, **kwargs):
    message = get_template("profile_recommendation.html").render()
    send_mail(
        subject='A new recommendation on your profile',
        html_message=message,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[instance.profile.user.email],
        fail_silently=True
    )


@receiver(signals.post_save, sender=ProfileDeployment)
def profile_deployment_saved(sender, instance, **kwargs):
    email_text = "There are new deployment requests on your profile. Please login to accept or reject"
    subject_text = 'New deployment requests on your profile'
    if instance.accepted_by_user and instance.status == 'initiated':
        email_text = f"Your deployment for {instance.outbreak.name} has been confirmed."
        subject_text = 'Deployment Accepted'
    if instance.status == 'ended':
        email_text = f"Your deployment for {instance.outbreak.name} has been {instance.status}. \n" \
                     f"Please upload a deployment report against your outbreak. \n" \
                     f" Thank you for your service."
        subject_text = f'Deployment {instance.status}'

    message = get_template("generic_message.html").render({
        'message': email_text,
        'link': WEB_APP_URL
    })
    send_mail(
        subject=subject_text,
        html_message=message,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[instance.profile.user.email],
        fail_silently=True
    )
