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
STEAM_PT_BR_MONTHS = {
    "jan": "Jan",
    "fev": "Feb",
    "mar": "Mar",
    "abr": "Apr",
    "mai": "May",
    "jun": "Jun",
    "jul": "Jul",
    "ago": "Aug",
    "set": "Sep",
    "out": "Oct",
    "nov": "Nov",
    "dez": "Dec",
}


def clean_steam_text(value):
    if not value:
        return ""

    text = strip_tags(unescape(value))
    text = text.replace("\r", " ")
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"[\t ]+", " ", text)
    return text.strip()


def clean_steam_requirements(value):
    if not value:
        return ""

    text = unescape(value)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = strip_tags(text)
    text = text.replace("\r", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def parse_steam_release_date(raw_date):
    if not raw_date:
        return None

    normalized_date = raw_date.strip()

    pt_br_match = re.fullmatch(r"(\d{1,2})\s+([A-Za-zÀ-ÿ]{3,})\.?\s*(?:,\s*)?(\d{4})", normalized_date)
    if pt_br_match:
        day, raw_month, year = pt_br_match.groups()
        month_key = raw_month.lower()[:3]
        english_month = STEAM_PT_BR_MONTHS.get(month_key)
        if english_month:
            normalized_date = f"{english_month} {int(day)}, {year}"

    for fmt in ("%b %d, %Y", "%d %b, %Y", "%b %d %Y", "%d %b. %Y"):
        try:
            return datetime.strptime(normalized_date, fmt).date()
        except ValueError:
            continue
    return None


def fetch_normalized_steam_game_with_fallback(app_id):
    payload = fetch_steam_game(app_id, language=DEFAULT_STEAM_LANGUAGE)
    normalized_data = normalize_steam_game(payload)

    needs_fallback = not normalized_data.get("description") or not normalized_data.get(
        "release_date"
    ) or not normalized_data.get("genre")

    if not needs_fallback:
        return normalized_data

    fallback_payload = fetch_steam_game(app_id, language=FALLBACK_STEAM_LANGUAGE)
    fallback_data = normalize_steam_game(fallback_payload)

    for field_name in ("description", "release_date", "genre"):
        if not normalized_data.get(field_name) and fallback_data.get(field_name):
            normalized_data[field_name] = fallback_data[field_name]

    return normalized_data


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


def fetch_steam_catalog_page(page=1, page_size=24, query="", language=DEFAULT_STEAM_LANGUAGE):
    if page < 1:
        raise SteamSyncError("Pagina invalida para o catalogo Steam.")
    if page_size <= 0:
        raise SteamSyncError("Quantidade por pagina invalida para o catalogo Steam.")

    start = (page - 1) * page_size
    query_string = urlencode(
        {
            "term": query or "",
            "start": start,
            "count": page_size,
            "infinite": 1,
            "supportedlang": language,
            "ndl": 1,
            "category1": STEAM_GAME_CATEGORY_ID,
        }
    )
    payload = fetch_json(f"{STEAM_SEARCH_RESULTS_URL}?{query_string}")
    if "results_html" not in payload:
        raise SteamSyncError("Resposta paginada do catalogo da Steam invalida.")
    return payload


def normalize_steam_catalog_page(payload):
    return {
        "items": normalize_steam_applist(payload),
        "total_count": int(payload.get("total_count") or 0),
    }


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
    developers = ", ".join(payload.get("developers") or [])
    publishers = ", ".join(payload.get("publishers") or [])
    pc_requirements = payload.get("pc_requirements") or {}
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
        "developers": developers,
        "publishers": publishers,
        "system_requirements_min": clean_steam_requirements(
            pc_requirements.get("minimum")
        ),
        "system_requirements_rec": clean_steam_requirements(
            pc_requirements.get("recommended")
        ),
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
        "developers",
        "publishers",
        "system_requirements_min",
        "system_requirements_rec",
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
    normalized_data = fetch_normalized_steam_game_with_fallback(app_id)

    if normalized_data.get("steam_type") != "game":
        raise SteamSyncError(
            f"O app_id {normalized_data['steam_app_id']} nao representa um jogo do tipo 'game'."
        )

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

    normalized_data = fetch_normalized_steam_game_with_fallback(game.steam_app_id)
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


def get_or_sync_game_by_steam_app_id(app_id):
    game = Game.objects.filter(steam_app_id=app_id).first()
    if game is not None:
        return sync_existing_game(game)

    game, _ = sync_game_from_steam(app_id)
    return game


def ensure_game_cached_from_catalog_item(app_id, title=""):
    game = Game.objects.filter(steam_app_id=app_id).first()
    if game is not None:
        return game

    try:
        game, _ = sync_game_from_steam(app_id)
        return game
    except SteamSyncError:
        if title:
            return Game.objects.create(title=title, steam_app_id=app_id, steam_type="game")
        raise
