from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core import signing
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
import json

from .models import Game, LibraryEntry, Review, UserEmailVerification
from .forms import (
    GameVaultAuthenticationForm,
    GameVaultProfileForm,
    GameVaultReviewForm,
    GameVaultUserCreationForm,
)
from .services.steam_auth import (
    build_steam_login_url,
    get_or_create_user_from_steam_identity,
    refresh_steam_link_profile,
    validate_steam_openid_callback,
)
from .services.steam import SteamSyncError
from .services.steam_library import sync_owned_games_for_user


IMAGE_VARIANT_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".avif")
VARIANT_COVER_POSITIONS = {
    "home": {
        "default": "center 34%",
        "by_title": {
            "Celeste": "center 20%",
            "Cyberpunk 2077": "center 24%",
            "Disco Elysium": "center 18%",
            "Elden Ring": "center 30%",
            "Hades": "center 22%",
            "Hollow Knight": "center 26%",
        },
    },
    "catalog": {
        "default": "center 30%",
        "by_title": {
            "Celeste": "center 16%",
            "Cyberpunk 2077": "center 24%",
            "Disco Elysium": "center 18%",
            "Elden Ring": "center 24%",
            "Hades": "center 26%",
            "Hollow Knight": "center 20%",
        },
    },
}
EMAIL_VERIFICATION_SALT = "gamevault-email-verification"


def resolve_variant_cover_image(cover_image, variant):
    if not cover_image:
        return ""

    cover_path = Path(urlparse(cover_image).path)
    stem = cover_path.stem
    if not stem:
        return cover_image

    variant_dir = Path(settings.BASE_DIR) / "static" / "img" / variant
    for extension in IMAGE_VARIANT_EXTENSIONS:
        variant_file = variant_dir / f"{stem}{extension}"
        if variant_file.exists():
            return f"{settings.STATIC_URL}img/{variant}/{variant_file.name}"

    return cover_image


def resolve_variant_cover_position(title, variant):
    variant_settings = VARIANT_COVER_POSITIONS.get(variant, {})
    return variant_settings.get("by_title", {}).get(
        title, variant_settings.get("default", "center center")
    )


def attach_variant_cover_metadata(games, variant, image_attribute, position_attribute):
    for game in games:
        setattr(game, image_attribute, resolve_variant_cover_image(game.cover_image, variant))
        setattr(game, position_attribute, resolve_variant_cover_position(game.title, variant))

    return games


def request_expects_json(request):
    return request.headers.get("Content-Type", "").startswith("application/json")


def get_latest_reviews_for_user_and_games(user, game_ids):
    latest_reviews = {}
    reviews = Review.objects.filter(user=user, game_id__in=game_ids).order_by(
        "game_id", "-created_at"
    )
    for review in reviews:
        latest_reviews.setdefault(review.game_id, review)
    return latest_reviews


def get_latest_reviews_for_game(game):
    latest_reviews = {}
    reviews = Review.objects.filter(game=game).select_related("user").order_by(
        "user_id", "-created_at"
    )
    for review in reviews:
        latest_reviews.setdefault(review.user_id, review)
    return sorted(
        latest_reviews.values(), key=lambda review: review.created_at, reverse=True
    )


def get_or_create_email_verification(user):
    verification, _ = UserEmailVerification.objects.get_or_create(user=user)
    return verification


def invalidate_email_verification(user):
    verification = get_or_create_email_verification(user)
    verification.is_verified = False
    verification.verified_at = None
    verification.save(update_fields=["is_verified", "verified_at"])
    return verification


def build_email_verification_url(request, user):
    token = signing.dumps(
        {"user_id": user.pk, "email": user.email}, salt=EMAIL_VERIFICATION_SALT
    )
    path = reverse("core:verify_email", kwargs={"token": token})
    return request.build_absolute_uri(path)


def send_verification_email(request, user):
    if not user.email:
        return False

    verification_url = build_email_verification_url(request, user)
    subject = render_to_string("registration/verify_email_subject.txt").strip()
    message = render_to_string(
        "registration/verify_email_email.txt",
        {"user": user, "verification_url": verification_url},
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    verification = get_or_create_email_verification(user)
    verification.last_verification_email_sent_at = timezone.now()
    verification.save(update_fields=["last_verification_email_sent_at"])
    return True


def home_view(request):
    """View para exibir a página inicial com catálogo de jogos em destaque"""
    # Buscar alguns jogos para exibir na homepage (limitar a 6 para não sobrecarregar)
    featured_games = attach_variant_cover_metadata(
        list(Game.objects.all()[:6]),
        "home",
        "home_cover_image",
        "home_cover_position",
    )

    context = {
        "featured_games": featured_games,
    }
    return render(request, "pages/home.html", context)


def sobre_view(request):
    return render(request, "pages/sobre.html")


def diferenciais_view(request):
    return render(request, "pages/diferenciais.html")


def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == "POST":
        form = GameVaultAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, "Voce entrou com sucesso.")
                if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)
                return redirect("core:library")
    else:
        form = GameVaultAuthenticationForm()

    return render(request, "registration/login.html", {"form": form, "next": next_url})


def steam_login_view(request):
    return redirect(build_steam_login_url(request))


def steam_callback_view(request):
    try:
        steam_id = validate_steam_openid_callback(request.GET)
        user, steam_link, created = get_or_create_user_from_steam_identity(steam_id)
        try:
            steam_link = refresh_steam_link_profile(steam_link)
        except SteamSyncError:
            pass

        login(request, user)

        try:
            sync_result = sync_owned_games_for_user(user)
            messages.success(
                request,
                "Login com Steam realizado com sucesso. "
                f"Biblioteca sincronizada: {sync_result['created_entries']} jogo(s) novos, "
                f"{sync_result['existing_entries']} ja existentes.",
            )
        except SteamSyncError as exc:
            messages.warning(
                request,
                "Login com Steam realizado, mas nao foi possivel sincronizar a biblioteca agora: "
                f"{exc}",
            )

        if created:
            messages.info(
                request,
                "Sua conta local do GameVault foi criada automaticamente a partir do login Steam.",
            )
        return redirect("core:library")
    except SteamSyncError as exc:
        messages.error(request, f"Nao foi possivel entrar com Steam: {exc}")
        return redirect("core:login")


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu com sucesso.")
    return redirect("core:home")


def register_view(request):
    if request.method == "POST":
        form = GameVaultUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            get_or_create_email_verification(user)
            try:
                send_verification_email(request, user)
                messages.success(
                    request,
                    "Conta criada com sucesso. Enviamos um link de verificacao para seu email.",
                )
            except Exception:
                messages.warning(
                    request,
                    "Conta criada com sucesso, mas nao foi possivel enviar o email de verificacao agora.",
                )
            login(request, user)
            return redirect("core:library")
        messages.error(request, "Corrija os campos destacados para criar sua conta.")
    else:
        form = GameVaultUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request):
    verification = get_or_create_email_verification(request.user)
    steam_link = getattr(request.user, "steam_account_link", None)

    if request.method == "POST":
        old_email = request.user.email
        form = GameVaultProfileForm(
            request.POST, instance=request.user, user=request.user
        )
        if form.is_valid():
            user = form.save()
            if user.email.lower() != (old_email or "").lower():
                verification = invalidate_email_verification(user)
                try:
                    send_verification_email(request, user)
                    messages.success(
                        request,
                        "Perfil atualizado. Enviamos um novo link de verificacao para seu email.",
                    )
                except Exception:
                    messages.warning(
                        request,
                        "Perfil atualizado, mas nao foi possivel enviar o email de verificacao agora.",
                    )
            else:
                messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("core:profile")
        messages.error(request, "Corrija os campos destacados para atualizar o perfil.")
    else:
        form = GameVaultProfileForm(instance=request.user, user=request.user)

    return render(
        request,
        "registration/profile.html",
        {
            "form": form,
            "email_verification": verification,
            "steam_link": steam_link,
        },
    )


@login_required
@require_POST
def steam_sync_library_view(request):
    if not hasattr(request.user, "steam_account_link"):
        messages.error(request, "Sua conta nao esta autenticada pela Steam.")
        return redirect("core:profile")

    try:
        result = sync_owned_games_for_user(request.user)
        messages.success(
            request,
            "Biblioteca Steam sincronizada com sucesso. "
            f"Novos jogos: {result['created_entries']}. Ja existentes: {result['existing_entries']}. Ignorados: {result['skipped_entries']}."
        )
    except SteamSyncError as exc:
        messages.error(request, f"Nao foi possivel sincronizar sua biblioteca Steam: {exc}")
    return redirect("core:profile")


def verify_email_view(request, token):
    try:
        data = signing.loads(token, salt=EMAIL_VERIFICATION_SALT, max_age=60 * 60 * 24 * 7)
        user_id = data.get("user_id")
        email = data.get("email")
        user = User.objects.get(pk=user_id)
    except Exception:
        messages.error(
            request,
            "Link de verificacao invalido ou expirado. Solicite um novo email de verificacao.",
        )
        return redirect("core:login")

    if user.email.lower() != (email or "").lower():
        messages.error(
            request,
            "Este link pertence a um email antigo. Solicite uma nova verificacao.",
        )
        return redirect("core:profile" if request.user.is_authenticated else "core:login")

    verification = get_or_create_email_verification(user)
    verification.is_verified = True
    verification.verified_at = timezone.now()
    verification.save(update_fields=["is_verified", "verified_at"])
    messages.success(request, "Email verificado com sucesso.")
    return redirect("core:profile" if request.user.is_authenticated else "core:login")


@login_required
@require_POST
def resend_verification_email_view(request):
    verification = get_or_create_email_verification(request.user)
    if verification.is_verified:
        messages.info(request, "Seu email ja esta verificado.")
        return redirect("core:profile")

    try:
        send_verification_email(request, request.user)
        messages.success(request, "Enviamos um novo link de verificacao para seu email.")
    except Exception:
        messages.error(
            request,
            "Nao foi possivel enviar o email de verificacao agora. Tente novamente mais tarde.",
        )
    return redirect("core:profile")


@login_required
def library_view(request):
    """View para listar os jogos da biblioteca do usuário"""
    library_entries = list(
        LibraryEntry.objects.filter(user=request.user).select_related("game")
    )
    game_ids = [entry.game_id for entry in library_entries]
    reviews_by_game_id = get_latest_reviews_for_user_and_games(request.user, game_ids)

    for entry in library_entries:
        entry.user_review = reviews_by_game_id.get(entry.game_id)

    context = {"library_entries": library_entries}
    return render(request, "library/library.html", context)


@login_required
@require_POST
def add_to_library_view(request):
    """View para adicionar um jogo à biblioteca"""
    try:
        if request_expects_json(request):
            data = json.loads(request.body)
            game_id = data.get("game_id")
            status = data.get("status", "plan_to_play")
        else:
            game_id = request.POST.get("game_id")
            status = request.POST.get("status", "plan_to_play")
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Dados inválidos."}, status=400
        )

    valid_statuses = {choice[0] for choice in LibraryEntry.STATUS_CHOICES}
    if status not in valid_statuses:
        if request_expects_json(request):
            return JsonResponse(
                {"success": False, "message": "Status inválido."}, status=400
            )
        messages.error(request, "Status inválido.")
        if game_id:
            return redirect("core:game_detail", game_id=game_id)
        return redirect("core:game_catalog")

    game = get_object_or_404(Game, id=game_id)

    library_entry, created = LibraryEntry.objects.get_or_create(
        user=request.user, game=game, defaults={"status": status}
    )

    if not created:
        library_entry.status = status
        library_entry.save(update_fields=["status", "updated_at"])

    message = "Jogo adicionado à biblioteca!"
    if request_expects_json(request):
        return JsonResponse(
            {
                "success": True,
                "message": message,
                "created": created,
            }
        )

    messages.success(request, message)
    return redirect("core:game_detail", game_id=game.id)
    
    


@login_required
@require_POST
def update_library_entry_view(request):
    """View para atualizar status/progresso de um jogo na biblioteca"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Dados inválidos."}, status=400
        )

    entry_id = data.get("entry_id")
    status = data.get("status")
    progress = data.get("progress")

    if not entry_id:
        return JsonResponse(
            {"success": False, "message": "Entrada da biblioteca não informada."},
            status=400,
        )

    library_entry = LibraryEntry.objects.filter(id=entry_id, user=request.user).first()
    if library_entry is None:
        return JsonResponse(
            {"success": False, "message": "Entrada da biblioteca não encontrada."},
            status=404,
        )

    updated_fields = []

    if status is not None:
        valid_statuses = {choice[0] for choice in LibraryEntry.STATUS_CHOICES}
        if status not in valid_statuses:
            return JsonResponse(
                {"success": False, "message": "Status inválido."}, status=400
            )
        library_entry.status = status
        updated_fields.append("status")

    if progress is not None:
        try:
            progress = int(progress)
        except (TypeError, ValueError):
            return JsonResponse(
                {"success": False, "message": "Progresso deve ser um número inteiro."},
                status=400,
            )

        if progress < 0 or progress > 100:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Progresso deve estar entre 0 e 100.",
                },
                status=400,
            )

        library_entry.progress = progress
        updated_fields.append("progress")

    if not updated_fields:
        return JsonResponse(
            {"success": False, "message": "Nenhum campo informado para atualização."},
            status=400,
        )

    library_entry.save(update_fields=updated_fields + ["updated_at"])

    return JsonResponse(
        {
            "success": True,
            "message": "Entrada atualizada com sucesso!",
            "entry": {
                "id": library_entry.id,
                "status": library_entry.status,
                "status_label": library_entry.get_status_display(),
                "progress": library_entry.progress,
            },
        }
    )


@login_required
@require_POST
def remove_from_library_view(request):
    """View para remover um jogo da biblioteca"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Dados inválidos."}, status=400
        )

    entry_id = data.get("entry_id")
    library_entry = LibraryEntry.objects.filter(id=entry_id, user=request.user).first()

    if library_entry is None:
        return JsonResponse(
            {"success": False, "message": "Entrada da biblioteca não encontrada."},
            status=404,
        )

    library_entry.delete()

    return JsonResponse({"success": True, "message": "Jogo removido da biblioteca!"})


def game_catalog_view(request):
    """View para exibir o catálogo de jogos"""
    query = request.GET.get("q", "")
    games = Game.objects.all()

    if query:
        games = games.filter(
            Q(title__icontains=query)
            | Q(genre__icontains=query)
            | Q(description__icontains=query)
        )

    games = attach_variant_cover_metadata(
        list(games),
        "catalog",
        "catalog_cover_image",
        "catalog_cover_position",
    )

    context = {"games": games, "query": query}
    return render(request, "catalog/game_catalog.html", context)


@ensure_csrf_cookie
def game_detail_view(request, game_id):
    """View para exibir detalhes de um jogo"""
    game = get_object_or_404(Game, id=game_id)

    # Verificar se o jogo está na biblioteca do usuário (se logado)
    in_library = False
    library_entry = None
    user_review = None
    if request.user.is_authenticated:
        try:
            library_entry = LibraryEntry.objects.get(user=request.user, game=game)
            in_library = True
        except LibraryEntry.DoesNotExist:
            pass

        user_review = (
            Review.objects.filter(user=request.user, game=game)
            .order_by("-created_at")
            .first()
        )

    # Obter avaliações do jogo
    reviews = get_latest_reviews_for_game(game)

    context = {
        "game": game,
        "in_library": in_library,
        "library_entry": library_entry,
        "user_review": user_review,
        "reviews": reviews,
    }
    return render(request, "catalog/game_detail.html", context)


@login_required
@require_POST
def add_review_view(request, game_id):
    """View para adicionar ou atualizar uma avaliação"""
    is_json_request = request_expects_json(request)

    try:
        if is_json_request:
            data = json.loads(request.body)
            form_data = {
                "rating": data.get("rating"),
                "comment": data.get("comment", ""),
            }
        else:
            form_data = request.POST
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "message": "Dados inválidos."}, status=400
        )

    game = get_object_or_404(Game, id=game_id)
    form = GameVaultReviewForm(form_data)

    if not form.is_valid():
        message = form.errors.get("rating", form.non_field_errors())
        error_message = message[0] if message else "Nao foi possivel salvar a avaliacao."
        if is_json_request:
            return JsonResponse(
                {"success": False, "message": error_message}, status=400
            )

        messages.error(request, error_message)
        return redirect("core:game_detail", game_id=game_id)

    review = form.save(commit=False)
    review.user = request.user
    review.game = game
    review.save()

    message = "Avaliacao salva com sucesso!"
    if is_json_request:
        return JsonResponse(
            {
                "success": True,
                "message": message,
                "created": True,
            }
        )

    messages.success(request, message)
    return redirect("core:game_detail", game_id=game.id)
