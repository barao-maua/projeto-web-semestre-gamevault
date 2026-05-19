from django.contrib import admin
from django.contrib import messages

from .models import (
    Game,
    GameList,
    GameListItem,
    LibraryEntry,
    Review,
    SteamAccountLink,
    UserEmailVerification,
)
from .services.steam import SteamSyncError, sync_existing_game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "steam_app_id",
        "steam_type",
        "genre",
        "release_date",
        "last_synced_at",
        "created_at",
    )
    search_fields = (
        "title",
        "genre",
        "description",
        "steam_app_id__exact",
        "steam_type",
    )
    list_filter = ("steam_type", "genre", "release_date", "last_synced_at")
    actions = ("sync_selected_with_steam",)

    @admin.action(description="Sincronizar com Steam")
    def sync_selected_with_steam(self, request, queryset):
        synced_count = 0

        for game in queryset:
            try:
                sync_existing_game(game)
                synced_count += 1
            except SteamSyncError as exc:
                self.message_user(
                    request,
                    f"Nao foi possivel sincronizar '{game.title}': {exc}",
                    level=messages.WARNING,
                )

        if synced_count:
            self.message_user(
                request,
                f"{synced_count} jogo(s) sincronizado(s) com sucesso.",
                level=messages.SUCCESS,
            )


@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "status", "progress", "added_at")
    search_fields = ("user__username", "game__title")
    list_filter = ("status", "user", "added_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "rating", "created_at")
    search_fields = ("user__username", "game__title", "comment")
    list_filter = ("rating", "user", "created_at")


@admin.register(GameList)
class GameListAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "is_public", "created_at")
    search_fields = ("user__username", "name", "description")
    list_filter = ("is_public", "user", "created_at")


@admin.register(GameListItem)
class GameListItemAdmin(admin.ModelAdmin):
    list_display = ("game_list", "game", "added_at")
    search_fields = ("game_list__name", "game__title")
    list_filter = ("game_list", "added_at")


@admin.register(UserEmailVerification)
class UserEmailVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "is_verified",
        "verified_at",
        "last_verification_email_sent_at",
    )
    search_fields = ("user__username", "user__email")
    list_filter = ("is_verified", "verified_at", "last_verification_email_sent_at")


@admin.register(SteamAccountLink)
class SteamAccountLinkAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "steam_id",
        "persona_name",
        "last_login_at",
        "last_library_sync_at",
        "created_at",
    )
    search_fields = ("user__username", "steam_id", "persona_name")
    list_filter = ("last_login_at", "last_library_sync_at", "created_at")
