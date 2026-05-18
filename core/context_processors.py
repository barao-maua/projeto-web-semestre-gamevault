from django.db.utils import OperationalError, ProgrammingError

from .models import UserEmailVerification


def email_verification_status(request):
    verification = None
    if request.user.is_authenticated:
        try:
            verification = UserEmailVerification.objects.filter(
                user=request.user
            ).first()
        except (OperationalError, ProgrammingError):
            verification = None

    return {"global_email_verification": verification}
