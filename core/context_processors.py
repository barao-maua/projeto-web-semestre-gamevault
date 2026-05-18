from .views import get_or_create_email_verification


def email_verification_status(request):
    verification = None
    if request.user.is_authenticated:
        verification = get_or_create_email_verification(request.user)

    return {"global_email_verification": verification}
