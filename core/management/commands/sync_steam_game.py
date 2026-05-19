from django.core.management.base import BaseCommand, CommandError

from core.services.steam import SteamSyncError, sync_game_from_steam


class Command(BaseCommand):
    help = "Importa ou sincroniza um jogo da Steam pelo app_id usando a fonte mockada da Fase 1"

    def add_arguments(self, parser):
        parser.add_argument("app_id", type=int)

    def handle(self, *args, **options):
        app_id = options["app_id"]

        try:
            game, created = sync_game_from_steam(app_id)
        except SteamSyncError as exc:
            raise CommandError(str(exc)) from exc

        action = "criado" if created else "atualizado"
        self.stdout.write(
            self.style.SUCCESS(
                f"Jogo {action} com sucesso: {game.title} (steam_app_id={game.steam_app_id})."
            )
        )
