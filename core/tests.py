from django.test import TestCase
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
