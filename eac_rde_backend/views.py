from django.http import HttpResponse

from core.models import User


def confirm_email_html(request, username=None, otp=None):
    user = User.objects.filter(username=username, otp=otp, otp_used=False).first()
    if user is None:
        return HttpResponse("Could Not Find the specified username and otp")
    user.is_active=True
    user.otp_used=True
    user.save()
    
    return HttpResponse("Email Verified Successfully")
