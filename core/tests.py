import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Game, GameList, GameListItem, LibraryEntry, Review


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
