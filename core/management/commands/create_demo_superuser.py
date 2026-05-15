from django.core.management.base import BaseCommand

from core.demo_data import create_demo_superuser, seed_demo_library_for_user


class Command(BaseCommand):
    help = "Cria ou atualiza um superusuario padrao para demonstracao"

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--email", default="demo@example.com")
        parser.add_argument("--password", default="admin123")

    def handle(self, *args, **options):
        result = create_demo_superuser(
            username=options["username"],
            email=options["email"],
            password=options["password"],
        )
        seed_result = seed_demo_library_for_user(result["user"])
        action = "criado" if result["created"] else "atualizado"
        message = (
            f"Superusuario de demonstracao {action}: {result['username']} ({result['email']})."
        )
        if seed_result["seeded"]:
            message += (
                f" Biblioteca pronta com {seed_result['game_title']} em status {seed_result['status']} e progresso {seed_result['progress']}%."
            )
        self.stdout.write(self.style.SUCCESS(message))
