from django.core.management.base import BaseCommand, CommandError

from core.services.steam import SteamSyncError, sync_steam_catalog


class Command(BaseCommand):
    help = "Importa ou atualiza jogos da Steam em lote, filtrando apenas apps do tipo 'game'"

    def add_arguments(self, parser):
        parser.add_argument("--offset", type=int, default=0)
        parser.add_argument("--limit", type=int, default=50)

    def handle(self, *args, **options):
        try:
            result = sync_steam_catalog(
                offset=options["offset"],
                limit=options["limit"],
            )
        except SteamSyncError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                "Sync do catalogo concluido. "
                f"Criados: {result['created']}. "
                f"Atualizados: {result['updated']}. "
                f"Ignorados: {result['skipped']}. "
                f"Jogos processados: {result['processed_games']}. "
                f"Proximo offset sugerido: {result['next_offset']}."
            )
        )
