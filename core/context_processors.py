from django.db.utils import OperationalError, ProgrammingError

from .models import SteamAccountLink, UserEmailVerification


def email_verification_status(request):
    verification = None
    steam_link = None
    if request.user.is_authenticated:
        try:
            verification = UserEmailVerification.objects.filter(
                user=request.user
            ).first()
            steam_link = SteamAccountLink.objects.filter(user=request.user).first()
        except (OperationalError, ProgrammingError):
            verification = None
            steam_link = None

    return {
        "global_email_verification": verification,
        "global_steam_link": steam_link,
    }
