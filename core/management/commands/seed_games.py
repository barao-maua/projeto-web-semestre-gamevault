from django.core.management.base import BaseCommand

from core.demo_data import seed_games


class Command(BaseCommand):
    help = "Cria ou atualiza os jogos iniciais de demonstracao"

    def handle(self, *args, **options):
        result = seed_games()
        self.stdout.write(
            self.style.SUCCESS(
                f"Jogos processados com sucesso. Criados: {result['created']}. Atualizados: {result['updated']}."
            )
        )
