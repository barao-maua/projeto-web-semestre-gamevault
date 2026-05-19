import json
import re
from datetime import datetime
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.utils import timezone
from django.utils.html import strip_tags

from core.models import Game


class SteamSyncError(Exception):
    pass


STEAM_SEARCH_RESULTS_URL = "https://store.steampowered.com/search/results/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"
REQUEST_TIMEOUT_SECONDS = 12
DEFAULT_STEAM_LANGUAGE = "brazilian"
FALLBACK_STEAM_LANGUAGE = "english"
STEAM_GAME_CATEGORY_ID = 998


def clean_steam_text(value):
    if not value:
        return ""

    text = strip_tags(unescape(value))
    text = text.replace("\r", " ")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[\t ]+", " ", text)
    return text.strip()


def parse_steam_release_date(raw_date):
    if not raw_date:
        return None

    for fmt in ("%b %d, %Y", "%d %b, %Y", "%b %d %Y"):
        try:
            return datetime.strptime(raw_date, fmt).date()
        except ValueError:
            continue
    return None


def fetch_json(url):
    request = Request(
        url,
        headers={
            "User-Agent": "GameVault/1.0 (+Django Steam Sync)",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise SteamSyncError(f"Falha HTTP ao consultar a Steam: {exc.code}.") from exc
    except URLError as exc:
        raise SteamSyncError("Nao foi possivel conectar a Steam.") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SteamSyncError("Resposta invalida da Steam.") from exc


def fetch_steam_applist(start=0, count=50, language=DEFAULT_STEAM_LANGUAGE):
    query_string = urlencode(
        {
            "query": "",
            "start": start,
            "count": count,
            "infinite": 1,
            "supportedlang": language,
            "ndl": 1,
            "category1": STEAM_GAME_CATEGORY_ID,
        }
    )
    payload = fetch_json(f"{STEAM_SEARCH_RESULTS_URL}?{query_string}")
    if "results_html" not in payload:
        raise SteamSyncError("Resposta do catalogo da Steam invalida.")
    return payload


def normalize_steam_applist(payload):
    results_html = payload.get("results_html", "")
    normalized_apps = []

    matches = re.findall(
        r'data-ds-appid="(\d+)".*?<span class="title">(.*?)</span>',
        results_html,
        flags=re.DOTALL,
    )
    for app_id, title in matches:
        cleaned_title = clean_steam_text(title)
        if not cleaned_title:
            continue
        normalized_apps.append({"steam_app_id": int(app_id), "title": cleaned_title})

    if not normalized_apps and payload.get("success") != 1:
        raise SteamSyncError("Nao foi possivel normalizar os jogos da busca Steam.")

    return normalized_apps


def fetch_steam_game(app_id, language=DEFAULT_STEAM_LANGUAGE):
    try:
        normalized_app_id = int(app_id)
    except (TypeError, ValueError) as exc:
        raise SteamSyncError("Steam App ID invalido.") from exc

    payload = fetch_json(
        f"{STEAM_APP_DETAILS_URL}?appids={normalized_app_id}&l={language}"
    )

    app_payload = payload.get(str(normalized_app_id))
    if not app_payload or not app_payload.get("success"):
        raise SteamSyncError(
            f"Jogo com app_id {normalized_app_id} nao encontrado na Steam."
        )

    data = app_payload.get("data")
    if not data:
        raise SteamSyncError(
            f"Steam retornou sucesso sem dados utilizaveis para app_id {normalized_app_id}."
        )

    return data


def normalize_steam_game(payload):
    if not payload or not payload.get("steam_appid") or not payload.get("name"):
        raise SteamSyncError("Payload da Steam invalido ou incompleto.")

    genres = payload.get("genres") or []
    primary_genre = genres[0]["description"] if genres else ""
    description = clean_steam_text(payload.get("detailed_description"))
    if not description:
        description = clean_steam_text(payload.get("short_description"))

    return {
        "steam_app_id": payload["steam_appid"],
        "steam_type": payload.get("type", "") or "",
        "title": payload["name"],
        "description": description,
        "release_date": parse_steam_release_date(
            (payload.get("release_date") or {}).get("date")
        ),
        "genre": primary_genre,
        "cover_image": payload.get("header_image", "") or "",
    }


def apply_steam_data_to_game(game, normalized_data):
    updated_fields = []

    for field_name in (
        "steam_type",
        "title",
        "description",
        "release_date",
        "genre",
        "cover_image",
    ):
        incoming_value = normalized_data.get(field_name)
        if incoming_value in (None, ""):
            continue
        if getattr(game, field_name) != incoming_value:
            setattr(game, field_name, incoming_value)
            updated_fields.append(field_name)

    if game.steam_app_id != normalized_data["steam_app_id"]:
        game.steam_app_id = normalized_data["steam_app_id"]
        updated_fields.append("steam_app_id")

    game.last_synced_at = timezone.now()
    updated_fields.append("last_synced_at")

    return updated_fields


def sync_game_from_steam(app_id):
    payload = fetch_steam_game(app_id, language=DEFAULT_STEAM_LANGUAGE)
    normalized_data = normalize_steam_game(payload)

    if normalized_data.get("steam_type") != "game":
        raise SteamSyncError(
            f"O app_id {normalized_data['steam_app_id']} nao representa um jogo do tipo 'game'."
        )

    if not normalized_data.get("description"):
        fallback_payload = fetch_steam_game(app_id, language=FALLBACK_STEAM_LANGUAGE)
        fallback_data = normalize_steam_game(fallback_payload)
        if fallback_data.get("description"):
            normalized_data["description"] = fallback_data["description"]
        if not normalized_data.get("genre") and fallback_data.get("genre"):
            normalized_data["genre"] = fallback_data["genre"]

    game = Game.objects.filter(steam_app_id=normalized_data["steam_app_id"]).first()
    created = game is None

    if created:
        game = Game(steam_app_id=normalized_data["steam_app_id"])

    updated_fields = apply_steam_data_to_game(game, normalized_data)

    if created:
        game.save()
    elif updated_fields:
        game.save(update_fields=updated_fields)

    return game, created


def sync_existing_game(game):
    if not game.steam_app_id:
        raise SteamSyncError("O jogo selecionado nao possui steam_app_id para sincronizar.")

    payload = fetch_steam_game(game.steam_app_id)
    normalized_data = normalize_steam_game(payload)
    updated_fields = apply_steam_data_to_game(game, normalized_data)

    if updated_fields:
        game.save(update_fields=updated_fields)

    return game


def sync_steam_catalog(offset=0, limit=100):
    apps = normalize_steam_applist(fetch_steam_applist(start=offset, count=limit))

    if offset < 0:
        raise SteamSyncError("Offset invalido.")
    if limit <= 0:
        raise SteamSyncError("Limit deve ser maior que zero.")

    created_count = 0
    updated_count = 0
    skipped_count = 0
    processed_games = 0
    next_offset = offset

    for app in apps:
        next_offset += 1
        try:
            _, created = sync_game_from_steam(app["steam_app_id"])
        except SteamSyncError:
            skipped_count += 1
            continue

        processed_games += 1
        if created:
            created_count += 1
        else:
            updated_count += 1

        if processed_games >= limit:
            break

    return {
        "created": created_count,
        "updated": updated_count,
        "skipped": skipped_count,
        "processed_games": processed_games,
        "next_offset": next_offset,
    }
