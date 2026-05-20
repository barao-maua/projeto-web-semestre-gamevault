from django.db.utils import OperationalError, ProgrammingError

from .models import SteamAccountLink, UserEmailVerification, UserProfile


def email_verification_status(request):
    verification = None
    steam_link = None
    user_profile = None
    if request.user.is_authenticated:
        try:
            verification = UserEmailVerification.objects.filter(
                user=request.user
            ).first()
            steam_link = SteamAccountLink.objects.filter(user=request.user).first()
            user_profile = UserProfile.objects.filter(user=request.user).first()
        except (OperationalError, ProgrammingError):
            verification = None
            steam_link = None
            user_profile = None

    return {
        "global_email_verification": verification,
        "global_steam_link": steam_link,
        "global_user_profile": user_profile,
    }
