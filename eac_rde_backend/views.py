from django.http import HttpResponse

from core.models import User


def confirm_email_html(request, username=None, otp=None):
    user = User.objects.filter(username=username, otp=otp).first()
    if not user:
        return HttpResponse("Could Not Find the specified username and otp")
    user.is_active=True
    user.otp_used=True
    user.save()
    return HttpResponse("Email Verified Successfully")
