from django.utils import timezone

from core.models import LibraryEntry, SteamAccountLink
from core.services.steam import SteamSyncError, sync_game_from_steam, fetch_json


def fetch_owned_games(steam_id):
    from django.conf import settings

    if not settings.STEAM_API_KEY:
        raise SteamSyncError(
            "STEAM_API_KEY nao configurada. Nao foi possivel importar a biblioteca Steam."
        )

    payload = fetch_json(
        "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        f"?key={settings.STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=0&include_played_free_games=1"
    )
    response = payload.get("response") or {}
    games = response.get("games")
    if games is None:
        raise SteamSyncError(
            "Nao foi possivel ler a biblioteca Steam. Verifique se o perfil e a biblioteca estao publicos."
        )
    return games


def normalize_owned_games(payload):
    return [int(game["appid"]) for game in payload if game.get("appid")]


def sync_owned_games_for_user(user):
    steam_link = user.steam_account_link
    app_ids = normalize_owned_games(fetch_owned_games(steam_link.steam_id))

    created_entries = 0
    existing_entries = 0
    skipped_entries = 0

    for app_id in app_ids:
        try:
            game, _ = sync_game_from_steam(app_id)
        except SteamSyncError:
            skipped_entries += 1
            continue

        _, created = LibraryEntry.objects.get_or_create(
            user=user,
            game=game,
            defaults={"status": "plan_to_play"},
        )

        if created:
            created_entries += 1
        else:
            existing_entries += 1

    steam_link.last_library_sync_at = timezone.now()
    steam_link.save(update_fields=["last_library_sync_at"])

    return {
        "created_entries": created_entries,
        "existing_entries": existing_entries,
        "skipped_entries": skipped_entries,
        "total_owned_games": len(app_ids),
    }
