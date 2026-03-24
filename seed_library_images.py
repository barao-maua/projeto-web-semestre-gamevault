import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Game  # Adjust the import according to your app name

# Mapping of game titles to image paths
image_mapping = {
    "Hollow Knight": "/static/img/Hollow_Knight.jpg",
    "Cyberpunk 2077": "/static/img/cyberpunk2077.jpg",
    "Assassin's Creed Valhalla": "/static/img/AssassinsCreedValhalla.jpg"
}

for title, image_path in image_mapping.items():
    # Find game by title (case-insensitive contains)
    games = Game.objects.filter(title__icontains=title)
    if games.exists():
        game = games.first()
        game.cover_image = image_path
        game.save()
        print(f"Updated '{game.title}' with cover_image: {game.cover_image}")
    else:
        print(f"Game not found for title containing: {title}")