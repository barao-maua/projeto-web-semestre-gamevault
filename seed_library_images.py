import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Game  # Importa o model de jogos do app principal

# Mapeamento dos titulos dos jogos para os caminhos das imagens principais.
# As variantes visuais de home/catalogo continuam em static/img/home e static/img/catalog.
image_mapping = {
    "Hollow Knight": "/static/img/HollowKnight.jpg",
    "Hades": "/static/img/Hades.jpg",
    "Elden Ring": "/static/img/EldenRing.png",
    "Disco Elysium": "/static/img/discoelysium.jpg",
    "Cyberpunk 2077": "/static/img/cyberpunk2077.jpg",
    "Celeste": "/static/img/celeste.png",
}

for title, image_path in image_mapping.items():
    # Busca o jogo pelo titulo sem diferenciar maiusculas e minusculas
    games = Game.objects.filter(title__icontains=title)
    if games.exists():
        game = games.first()
        game.cover_image = image_path
        game.save()
        print(f"Updated '{game.title}' with cover_image: {game.cover_image}")
    else:
        print(f"Game not found for title containing: {title}")
