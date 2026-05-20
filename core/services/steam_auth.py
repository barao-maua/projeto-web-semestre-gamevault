from urllib.parse import urlencode, urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from core.models import SteamAccountLink, UserEmailVerification
from core.services.steam import SteamSyncError, fetch_json


STEAM_OPENID_URL = "https://steamcommunity.com/openid/login"
STEAM_CLAIMED_ID_PREFIX = "https://steamcommunity.com/openid/id/"


def build_steam_realm(request):
    return request.build_absolute_uri("/")


def build_steam_login_url(request):
    params = {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "checkid_setup",
        "openid.return_to": request.build_absolute_uri(
            settings.STEAM_OPENID_RETURN_PATH
        ),
        "openid.realm": build_steam_realm(request),
        "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
        "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
    }
    return f"{STEAM_OPENID_URL}?{urlencode(params)}"


def extract_steam_id(claimed_id):
    if not claimed_id or not claimed_id.startswith(STEAM_CLAIMED_ID_PREFIX):
        raise SteamSyncError("Steam ID invalido retornado pelo provedor OpenID.")
    return claimed_id.removeprefix(STEAM_CLAIMED_ID_PREFIX)


def validate_steam_openid_callback(query_params):
    required_keys = {
        "openid.assoc_handle",
        "openid.signed",
        "openid.sig",
        "openid.ns",
        "openid.claimed_id",
        "openid.identity",
        "openid.return_to",
        "openid.response_nonce",
    }
    if not required_keys.issubset(set(query_params.keys())):
        raise SteamSyncError("Callback OpenID da Steam incompleto.")

    verification_payload = {key: value for key, value in query_params.items() if key.startswith("openid.")}
    verification_payload["openid.mode"] = "check_authentication"

    body = urlencode(verification_payload).encode("utf-8")
    request_url = f"{STEAM_OPENID_URL}?{urlencode({'openid.mode': 'check_authentication'})}"
    parsed = urlparse(request_url)
    post_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError

    request = Request(
        post_url,
        data=body,
        headers={
            "User-Agent": "GameVault/1.0 (+Django Steam Auth)",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    try:
        with urlopen(request, timeout=12) as response:
            payload = response.read().decode("utf-8", "ignore")
    except HTTPError as exc:
        raise SteamSyncError(
            f"Falha HTTP ao validar login Steam: {exc.code}."
        ) from exc
    except URLError as exc:
        raise SteamSyncError("Nao foi possivel validar o login Steam.") from exc

    if "is_valid:true" not in payload:
        raise SteamSyncError("A Steam nao validou o callback OpenID.")

    return extract_steam_id(query_params["openid.claimed_id"])


def fetch_steam_profile(steam_id):
    if not settings.STEAM_API_KEY:
        raise SteamSyncError(
            "STEAM_API_KEY nao configurada. Nao foi possivel buscar o perfil publico da Steam."
        )

    payload = fetch_json(
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        f"?key={settings.STEAM_API_KEY}&steamids={steam_id}"
    )

    players = ((payload.get("response") or {}).get("players") or [])
    if not players:
        raise SteamSyncError("Nao foi possivel obter o perfil publico da conta Steam.")
    return players[0]


def build_steam_username(steam_id, persona_name=""):
    base = "".join(character for character in persona_name.lower() if character.isalnum())[:20]
    if not base:
        base = f"steam{steam_id[-8:]}"
    candidate = f"{base}_{steam_id[-6:]}"
    while User.objects.filter(username=candidate).exists():
        candidate = f"{candidate[:20]}x"
    return candidate[:30]


def ensure_steam_user_email_verified(user):
    verification, _ = UserEmailVerification.objects.get_or_create(user=user)
    update_fields = []

    if not verification.is_verified:
        verification.is_verified = True
        update_fields.append("is_verified")

    if verification.verified_at is None:
        verification.verified_at = timezone.now()
        update_fields.append("verified_at")

    if update_fields:
        verification.save(update_fields=update_fields)

    return verification


def get_or_create_user_from_steam_identity(steam_id):
    steam_link = SteamAccountLink.objects.filter(steam_id=steam_id).select_related("user").first()
    if steam_link is not None:
        ensure_steam_user_email_verified(steam_link.user)
        return steam_link.user, steam_link, False

    try:
        profile = fetch_steam_profile(steam_id)
    except SteamSyncError:
        profile = {}

    username = build_steam_username(steam_id, profile.get("personaname", ""))
    user = User.objects.create_user(username=username, password=None)
    steam_link = SteamAccountLink.objects.create(
        user=user,
        steam_id=steam_id,
        persona_name=profile.get("personaname", "") or "",
        profile_url=profile.get("profileurl", "") or "",
        avatar_url=profile.get("avatarfull", "") or "",
        last_login_at=timezone.now(),
    )
    ensure_steam_user_email_verified(user)
    return user, steam_link, True


def refresh_steam_link_profile(steam_link):
    profile = fetch_steam_profile(steam_link.steam_id)
    steam_link.persona_name = profile.get("personaname", "") or steam_link.persona_name
    steam_link.profile_url = profile.get("profileurl", "") or steam_link.profile_url
    steam_link.avatar_url = profile.get("avatarfull", "") or steam_link.avatar_url
    steam_link.last_login_at = timezone.now()
    steam_link.save(
        update_fields=[
            "persona_name",
            "profile_url",
            "avatar_url",
            "last_login_at",
        ]
    )
    return steam_link
