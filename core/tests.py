import json
from io import StringIO
from unittest.mock import patch

from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Game, GameList, GameListItem, LibraryEntry, Review, SteamAccountLink
from .services.steam import (
    SteamSyncError,
    fetch_steam_applist,
    normalize_steam_applist,
    normalize_steam_game,
    sync_existing_game,
    sync_game_from_steam,
    sync_steam_catalog,
)
from .services.steam_auth import build_steam_username, get_or_create_user_from_steam_identity


class MockHTTPResponse:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class GameVaultModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player", password="testpass123")
        self.game = Game.objects.create(
            title="Hollow Knight",
            genre="Metroidvania",
            cover_image="/static/img/HollowKnight.jpg",
        )

    def test_game_string_representation_uses_title(self):
        self.assertEqual(str(self.game), "Hollow Knight")

    def test_library_entry_string_representation(self):
        entry = LibraryEntry.objects.create(user=self.user, game=self.game)

        self.assertEqual(str(entry), "player - Hollow Knight")

    def test_review_string_representation(self):
        review = Review.objects.create(user=self.user, game=self.game, rating=5)

        self.assertEqual(str(review), "player - Hollow Knight (5/5)")

    def test_game_list_and_item_string_representations(self):
        game_list = GameList.objects.create(user=self.user, name="Favoritos")
        item = GameListItem.objects.create(game_list=game_list, game=self.game)

        self.assertEqual(str(game_list), "player - Favoritos")
        self.assertEqual(str(item), "Favoritos - Hollow Knight")


class GameDetailInteractionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player", password="testpass123")
        self.game = Game.objects.create(
            title="Hollow Knight",
            genre="Metroidvania",
            cover_image="/static/img/HollowKnight.jpg",
        )

    def test_game_detail_sets_csrf_cookie(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("core:game_detail", args=[self.game.id]))

        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", response.cookies)

    def test_authenticated_user_can_add_game_to_library(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("core:add_to_library"),
            data=json.dumps({"game_id": self.game.id, "status": "playing"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            LibraryEntry.objects.filter(
                user=self.user, game=self.game, status="playing"
            ).exists()
        )

    def test_authenticated_user_can_add_game_to_library_by_html_form(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("core:add_to_library"),
            data={"game_id": self.game.id, "status": "plan_to_play"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            LibraryEntry.objects.filter(
                user=self.user, game=self.game, status="plan_to_play"
            ).exists()
        )

    def test_authenticated_user_can_create_review(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("core:add_review", args=[self.game.id]),
            data=json.dumps({"rating": 5, "comment": "Excelente"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Review.objects.filter(
                user=self.user, game=self.game, rating=5, comment="Excelente"
            ).exists()
        )

    def test_authenticated_user_can_create_review_by_html_form(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("core:add_review", args=[self.game.id]),
            data={"rating": "4", "comment": "Muito bom"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Review.objects.filter(
                user=self.user, game=self.game, rating=4, comment="Muito bom"
            ).exists()
        )

    def test_authenticated_user_can_create_review_history(self):
        self.client.force_login(self.user)
        Review.objects.create(user=self.user, game=self.game, rating=3, comment="Bom")

        response = self.client.post(
            reverse("core:add_review", args=[self.game.id]),
            data=json.dumps({"rating": 5, "comment": "Excelente agora"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.filter(user=self.user, game=self.game).count(), 2)
        latest_review = Review.objects.filter(user=self.user, game=self.game).latest("created_at")
        self.assertEqual(latest_review.rating, 5)
        self.assertEqual(latest_review.comment, "Excelente agora")

    def test_library_view_includes_user_review_context(self):
        self.client.force_login(self.user)
        LibraryEntry.objects.create(user=self.user, game=self.game, status="playing")
        Review.objects.create(user=self.user, game=self.game, rating=2, comment="Antes")
        Review.objects.create(user=self.user, game=self.game, rating=4, comment="Muito bom")

        response = self.client.get(reverse("core:library"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-has-review="true"')
        self.assertContains(response, 'aria-label="Sua avaliação: 4 de 5"')

    def test_game_detail_shows_only_latest_review_per_user(self):
        self.client.force_login(self.user)
        Review.objects.create(user=self.user, game=self.game, rating=2, comment="Opinião antiga")
        Review.objects.create(user=self.user, game=self.game, rating=5, comment="Opinião atual")

        response = self.client.get(reverse("core:game_detail", args=[self.game.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Opinião atual")
        self.assertNotContains(response, "Opinião antiga")

    def test_catalog_shows_steam_badge_for_synced_game(self):
        self.game.steam_app_id = 620
        self.game.save(update_fields=["steam_app_id"])

        response = self.client.get(reverse("core:game_catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Steam")

    def test_game_detail_shows_steam_sync_badge_for_synced_game(self):
        self.game.steam_app_id = 620
        self.game.save(update_fields=["steam_app_id"])

        response = self.client.get(reverse("core:game_detail", args=[self.game.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dados sincronizados da Steam")

    def test_logout_requires_post_and_logs_user_out(self):
        self.client.force_login(self.user)

        get_response = self.client.get(reverse("core:logout"))
        self.assertEqual(get_response.status_code, 405)

        post_response = self.client.post(reverse("core:logout"), follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_public_navbar_points_to_real_routes(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/catalog/"')
        self.assertContains(response, ">Sobre<")
        self.assertContains(response, ">Diferenciais<")


class SteamIntegrationPhaseOneTests(TestCase):
    def build_appdetails_response(
        self,
        app_id=620,
        name="Portal 2",
        app_type="game",
        detailed_description="<p>Descricao <strong>real</strong> do jogo.</p>",
        short_description="Descricao curta.",
    ):
        return {
            str(app_id): {
                "success": True,
                "data": {
                    "steam_appid": app_id,
                    "type": app_type,
                    "name": name,
                    "detailed_description": detailed_description,
                    "short_description": short_description,
                    "header_image": f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg",
                    "release_date": {"date": "Apr 19, 2011"},
                    "genres": [{"description": "Puzzle"}, {"description": "Adventure"}],
                },
            }
        }

    def build_steam_payload(self, app_id=620, name="Portal 2"):
        return self.build_appdetails_response(app_id=app_id, name=name)

    def build_applist_payload(self):
        return {
            "success": 1,
            "results_html": """
                <a data-ds-appid=\"620\"><span class=\"title\">Portal 2</span></a>
                <a data-ds-appid=\"211\"><span class=\"title\">Source SDK</span></a>
                <a data-ds-appid=\"730\"><span class=\"title\">Counter-Strike 2</span></a>
            """,
        }

    @patch("core.services.steam.urlopen")
    def test_sync_game_from_mock_source_creates_new_game(self, mocked_urlopen):
        mocked_urlopen.return_value = MockHTTPResponse(self.build_steam_payload())
        game, created = sync_game_from_steam(620)

        self.assertTrue(created)
        self.assertEqual(game.steam_app_id, 620)
        self.assertEqual(game.steam_type, "game")
        self.assertEqual(game.title, "Portal 2")
        self.assertEqual(game.genre, "Puzzle")
        self.assertEqual(game.description, "Descricao real do jogo.")
        self.assertIsNotNone(game.last_synced_at)

    @patch("core.services.steam.urlopen")
    def test_sync_game_from_mock_source_updates_existing_game_without_duplication(self, mocked_urlopen):
        mocked_urlopen.return_value = MockHTTPResponse(self.build_steam_payload())
        existing_game = Game.objects.create(
            title="Portal 2 antigo",
            steam_app_id=620,
            description="Descricao antiga",
            genre="Old Genre",
            cover_image="https://example.com/old.jpg",
        )

        game, created = sync_game_from_steam(620)

        self.assertFalse(created)
        self.assertEqual(game.pk, existing_game.pk)
        self.assertEqual(Game.objects.filter(steam_app_id=620).count(), 1)
        self.assertEqual(game.title, "Portal 2")
        self.assertEqual(game.steam_type, "game")
        self.assertEqual(game.genre, "Puzzle")

    def test_sync_existing_game_requires_steam_app_id(self):
        game = Game.objects.create(title="Jogo local")

        with self.assertRaises(SteamSyncError):
            sync_existing_game(game)

    def test_normalize_steam_game_raises_on_invalid_payload(self):
        with self.assertRaises(SteamSyncError):
            normalize_steam_game({})

    def test_fetch_steam_applist_returns_apps(self):
        with patch("core.services.steam.urlopen") as mocked_urlopen:
            mocked_urlopen.return_value = MockHTTPResponse(self.build_applist_payload())

            apps = fetch_steam_applist(start=0, count=5)

        self.assertIn("results_html", apps)

    def test_normalize_steam_applist_filters_empty_items(self):
        normalized = normalize_steam_applist(self.build_applist_payload())

        self.assertEqual(len(normalized), 3)
        self.assertEqual(normalized[0]["steam_app_id"], 620)

    def test_normalize_steam_game_strips_html_from_description(self):
        normalized = normalize_steam_game(
            {
                "steam_appid": 620,
                "type": "game",
                "name": "Portal 2",
                "detailed_description": "<p>Descricao <strong>real</strong> do jogo.</p>",
                "short_description": "Descricao curta.",
                "header_image": "https://cdn.akamai.steamstatic.com/steam/apps/620/header.jpg",
                "release_date": {"date": "Apr 19, 2011"},
                "genres": [{"description": "Puzzle"}],
            }
        )

        self.assertEqual(normalized["description"], "Descricao real do jogo.")

    @patch("core.services.steam.urlopen")
    def test_sync_game_uses_english_fallback_when_brazilian_description_is_empty(self, mocked_urlopen):
        mocked_urlopen.side_effect = [
            MockHTTPResponse(
                self.build_appdetails_response(
                    detailed_description="",
                    short_description="",
                )
            ),
            MockHTTPResponse(
                self.build_appdetails_response(
                    detailed_description="<p>Fallback english description.</p>",
                    short_description="Fallback short.",
                )
            ),
        ]

        game, _ = sync_game_from_steam(620)

        self.assertEqual(game.description, "Fallback english description.")

    @patch("core.services.steam.urlopen")
    def test_sync_steam_catalog_imports_only_games_and_respects_limit(self, mocked_urlopen):
        mocked_urlopen.side_effect = [
            MockHTTPResponse(self.build_applist_payload()),
            MockHTTPResponse(self.build_appdetails_response(app_id=620, name="Portal 2", app_type="game")),
            MockHTTPResponse(self.build_appdetails_response(app_id=211, name="Source SDK", app_type="tool")),
            MockHTTPResponse(self.build_appdetails_response(app_id=730, name="Counter-Strike 2", app_type="game")),
        ]

        result = sync_steam_catalog(offset=0, limit=2)

        self.assertEqual(result["processed_games"], 2)
        self.assertEqual(result["created"], 2)
        self.assertEqual(result["skipped"], 1)
        self.assertTrue(Game.objects.filter(steam_app_id=620, steam_type="game").exists())
        self.assertTrue(Game.objects.filter(steam_app_id=730, steam_type="game").exists())
        self.assertFalse(Game.objects.filter(steam_app_id=211).exists())

    @patch("core.services.steam.urlopen")
    def test_sync_command_outputs_success_message(self, mocked_urlopen):
        mocked_urlopen.return_value = MockHTTPResponse(self.build_steam_payload(app_id=730, name="Counter-Strike 2"))
        stdout = StringIO()

        call_command("sync_steam_game", "730", stdout=stdout)

        self.assertIn("Jogo criado com sucesso", stdout.getvalue())
        self.assertTrue(Game.objects.filter(steam_app_id=730, title="Counter-Strike 2").exists())

    @patch("core.services.steam.urlopen")
    def test_sync_catalog_command_outputs_summary(self, mocked_urlopen):
        mocked_urlopen.side_effect = [
            MockHTTPResponse(self.build_applist_payload()),
            MockHTTPResponse(self.build_appdetails_response(app_id=620, name="Portal 2", app_type="game")),
        ]
        stdout = StringIO()

        call_command("sync_steam_catalog", "--offset", "0", "--limit", "1", stdout=stdout)

        self.assertIn("Sync do catalogo concluido", stdout.getvalue())

    @patch("core.services.steam.urlopen")
    def test_sync_command_raises_command_error_for_unknown_app(self, mocked_urlopen):
        mocked_urlopen.return_value = MockHTTPResponse({"999999": {"success": False}})
        with self.assertRaisesMessage(CommandError, "nao encontrado na Steam"):
            call_command("sync_steam_game", "999999")


class SteamDirectLoginTests(TestCase):
    def setUp(self):
        self.game = Game.objects.create(
            title="Portal 2",
            steam_app_id=620,
            steam_type="game",
        )

    def test_build_steam_username_uses_persona_name_when_available(self):
        username = build_steam_username("76561198000000000", "Portal Fan")

        self.assertTrue(username.startswith("portalfan_"))

    @patch("core.services.steam_auth.fetch_steam_profile")
    def test_get_or_create_user_from_steam_identity_creates_local_user(self, mocked_profile):
        mocked_profile.return_value = {
            "personaname": "SteamPlayer",
            "profileurl": "https://steamcommunity.com/id/player",
            "avatarfull": "https://steamcdn/avatar.jpg",
        }

        user, steam_link, created = get_or_create_user_from_steam_identity(
            "76561198000000000"
        )

        self.assertTrue(created)
        self.assertEqual(steam_link.user, user)
        self.assertEqual(steam_link.steam_id, "76561198000000000")
        self.assertEqual(steam_link.persona_name, "SteamPlayer")

    @patch("core.views.sync_owned_games_for_user")
    @patch("core.views.refresh_steam_link_profile")
    @patch("core.views.get_or_create_user_from_steam_identity")
    @patch("core.views.validate_steam_openid_callback")
    def test_steam_callback_logs_user_in_and_syncs_library(
        self,
        mocked_validate_callback,
        mocked_get_or_create_user,
        mocked_refresh_profile,
        mocked_sync_library,
    ):
        user = User.objects.create_user(username="steam_local")
        steam_link = SteamAccountLink.objects.create(
            user=user,
            steam_id="76561198000000000",
            persona_name="SteamPlayer",
            last_login_at=timezone.now(),
        )
        mocked_validate_callback.return_value = "76561198000000000"
        mocked_get_or_create_user.return_value = (user, steam_link, False)
        mocked_refresh_profile.return_value = steam_link
        mocked_sync_library.return_value = {
            "created_entries": 1,
            "existing_entries": 0,
            "skipped_entries": 0,
            "total_owned_games": 1,
        }

        response = self.client.get(reverse("core:steam_callback"), {"openid.mode": "id_res"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("_auth_user_id", self.client.session)

    @patch("core.services.steam_library.fetch_owned_games")
    @patch("core.services.steam_library.sync_game_from_steam")
    def test_sync_owned_games_creates_library_entries_as_plan_to_play(
        self,
        mocked_sync_game,
        mocked_fetch_owned_games,
    ):
        from .services.steam_library import sync_owned_games_for_user

        user = User.objects.create_user(username="steam_local")
        SteamAccountLink.objects.create(
            user=user,
            steam_id="76561198000000000",
            persona_name="SteamPlayer",
        )
        mocked_fetch_owned_games.return_value = [{"appid": 620}]
        mocked_sync_game.return_value = (self.game, False)

        result = sync_owned_games_for_user(user)

        self.assertEqual(result["created_entries"], 1)
        entry = LibraryEntry.objects.get(user=user, game=self.game)
        self.assertEqual(entry.status, "plan_to_play")

    @patch("core.services.steam_library.fetch_owned_games")
    @patch("core.services.steam_library.sync_game_from_steam")
    def test_sync_owned_games_does_not_overwrite_existing_library_entry(
        self,
        mocked_sync_game,
        mocked_fetch_owned_games,
    ):
        from .services.steam_library import sync_owned_games_for_user

        user = User.objects.create_user(username="steam_local")
        SteamAccountLink.objects.create(user=user, steam_id="76561198000000000")
        LibraryEntry.objects.create(user=user, game=self.game, status="playing")
        mocked_fetch_owned_games.return_value = [{"appid": 620}]
        mocked_sync_game.return_value = (self.game, False)

        result = sync_owned_games_for_user(user)

        self.assertEqual(result["existing_entries"], 1)
        entry = LibraryEntry.objects.get(user=user, game=self.game)
        self.assertEqual(entry.status, "playing")
