from django.contrib import admin

from .models import Game, GameList, GameListItem, LibraryEntry, Review


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "release_date", "created_at")
    search_fields = ("title", "genre", "description")
    list_filter = ("genre", "release_date")


@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "status", "progress", "added_at")
    search_fields = ("user__username", "game__title")
    list_filter = ("status", "added_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "rating", "created_at")
    search_fields = ("user__username", "game__title", "comment")
    list_filter = ("rating", "created_at")


@admin.register(GameList)
class GameListAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "is_public", "created_at")
    search_fields = ("user__username", "name", "description")
    list_filter = ("is_public", "created_at")


@admin.register(GameListItem)
class GameListItemAdmin(admin.ModelAdmin):
    list_display = ("game_list", "game", "added_at")
    search_fields = ("game_list__name", "game__title")
    list_filter = ("added_at",)
