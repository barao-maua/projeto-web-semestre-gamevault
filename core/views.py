from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import json

from .models import Game, LibraryEntry, Review, GameList, GameListItem


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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Você está logado como {username}.")
                return redirect("core:home")
            else:
                messages.error(request, "Nome de usuário ou senha inválido.")
        else:
            messages.error(request, "Nome de usuário ou senha inválido.")
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu com sucesso.")
    return redirect("core:home")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Conta criada para {username}!")
            login(request, user)
            return redirect("core:home")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "registration/profile.html")


@login_required
def library_view(request):
    """View para listar os jogos da biblioteca do usuário"""
    library_entries = LibraryEntry.objects.filter(user=request.user).select_related(
        "game"
    )
    context = {"library_entries": library_entries}
    return render(request, "library/library.html", context)


@login_required
def add_to_library_view(request):
    """View para adicionar um jogo à biblioteca"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            game_id = data.get("game_id")
            status = data.get("status", "plan_to_play")

            game = get_object_or_404(Game, id=game_id)

            # Verifica se o jogo já está na biblioteca
            library_entry, created = LibraryEntry.objects.get_or_create(
                user=request.user, game=game, defaults={"status": status}
            )

            if not created:
                # Se já existir, atualiza o status
                library_entry.status = status
                library_entry.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Jogo adicionado à biblioteca!",
                    "created": created,
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Método não permitido"})


@login_required
@require_POST
def update_library_entry_view(request):
    """View para atualizar status/progresso de um jogo na biblioteca"""
    try:
        data = json.loads(request.body)
        entry_id = data.get("entry_id")
        status = data.get("status")
        progress = data.get("progress")

        library_entry = get_object_or_404(LibraryEntry, id=entry_id, user=request.user)

        if status is not None:
            library_entry.status = status
        if progress is not None:
            library_entry.progress = progress

        library_entry.save()

        return JsonResponse(
            {"success": True, "message": "Entrada atualizada com sucesso!"}
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


@login_required
@require_POST
def remove_from_library_view(request):
    """View para remover um jogo da biblioteca"""
    try:
        data = json.loads(request.body)
        entry_id = data.get("entry_id")

        library_entry = get_object_or_404(LibraryEntry, id=entry_id, user=request.user)
        library_entry.delete()

        return JsonResponse(
            {"success": True, "message": "Jogo removido da biblioteca!"}
        )
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


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


def game_detail_view(request, game_id):
    """View para exibir detalhes de um jogo"""
    game = get_object_or_404(Game, id=game_id)

    # Verificar se o jogo está na biblioteca do usuário (se logado)
    in_library = False
    library_entry = None
    if request.user.is_authenticated:
        try:
            library_entry = LibraryEntry.objects.get(user=request.user, game=game)
            in_library = True
        except LibraryEntry.DoesNotExist:
            pass

    # Obter avaliações do jogo
    reviews = Review.objects.filter(game=game).select_related("user")

    context = {
        "game": game,
        "in_library": in_library,
        "library_entry": library_entry,
        "reviews": reviews,
    }
    return render(request, "catalog/game_detail.html", context)


@login_required
def add_review_view(request, game_id):
    """View para adicionar ou atualizar uma avaliação"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rating = data.get("rating")
            comment = data.get("comment", "")

            game = get_object_or_404(Game, id=game_id)

            # Verifica se o usuário já avaliou este jogo
            review, created = Review.objects.get_or_create(
                user=request.user,
                game=game,
                defaults={"rating": rating, "comment": comment},
            )

            if not created:
                # Se já existir, atualiza a avaliação
                review.rating = rating
                review.comment = comment
                review.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Avaliação salva com sucesso!",
                    "created": created,
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Método não permitido"})
