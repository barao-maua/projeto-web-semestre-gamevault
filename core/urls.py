from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    diferenciais_view,
    home_view,
    sobre_view,
    login_view,
    steam_login_view,
    steam_callback_view,
    logout_view,
    register_view,
    profile_view,
    steam_sync_library_view,
    verify_email_view,
    resend_verification_email_view,
    library_view,
    add_to_library_view,
    update_library_entry_view,
    remove_from_library_view,
    game_catalog_view,
    game_detail_view,
    add_review_view,
)
from .forms import GameVaultSetPasswordForm

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("sobre/", sobre_view, name="sobre"),
    path("diferenciais/", diferenciais_view, name="diferenciais"),
    path("login/", login_view, name="login"),
    path("steam/login/", steam_login_view, name="steam_login"),
    path("steam/callback/", steam_callback_view, name="steam_callback"),
    path("logout/", logout_view, name="logout"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=GameVaultSetPasswordForm,
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("steam/sync-library/", steam_sync_library_view, name="steam_sync_library"),
    path("verify-email/<str:token>/", verify_email_view, name="verify_email"),
    path(
        "resend-verification-email/",
        resend_verification_email_view,
        name="resend_verification_email",
    ),
    path("library/", library_view, name="library"),
    path("add-to-library/", add_to_library_view, name="add_to_library"),
    path(
        "update-library-entry/", update_library_entry_view, name="update_library_entry"
    ),
    path("remove-from-library/", remove_from_library_view, name="remove_from_library"),
    path("catalog/", game_catalog_view, name="game_catalog"),
    path("game/<int:game_id>/", game_detail_view, name="game_detail"),
    path("game/<int:game_id>/review/", add_review_view, name="add_review"),
]
