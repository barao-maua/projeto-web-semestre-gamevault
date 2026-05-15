from django.contrib.auth import get_user_model

from .models import Game, LibraryEntry, Review


GAMES_DATA = [
    {
        "title": "Hollow Knight",
        "genre": "Metroidvania",
        "description": "Explore um mundo interconectado em Hollow Knight, um jogo de acao e aventura em 2D desenhado a mao. Desca as profundezas de Hallownest, descubra seus segredos e supere seus desafios.",
        "release_date": "2017-02-24",
        "cover_image": "/static/img/HollowKnight.jpg",
    },
    {
        "title": "Hades",
        "genre": "Roguelike",
        "description": "Desafie o deus dos mortos em Hades, um jogo de acao e estrategia onde voce tenta escapar do submundo grego. Lute, morra e tente novamente, cada vez mais forte.",
        "release_date": "2020-09-17",
        "cover_image": "/static/img/Hades.jpg",
    },
    {
        "title": "Elden Ring",
        "genre": "RPG de Acao",
        "description": "Explore as Terras Intermedias em Elden Ring, um RPG de acao de mundo aberto criado por Hidetaka Miyazaki e George R. R. Martin. Enfrente desafios epicos e descubra um mito profundo.",
        "release_date": "2022-02-25",
        "cover_image": "/static/img/EldenRing.png",
    },
    {
        "title": "Disco Elysium",
        "genre": "RPG",
        "description": "Disco Elysium e um RPG inovador onde voce e um detetive com amnesia tentando resolver um caso em uma cidade decadente. Suas habilidades sao suas vozes internas.",
        "release_date": "2019-10-15",
        "cover_image": "/static/img/discoelysium.jpg",
    },
    {
        "title": "Cyberpunk 2077",
        "genre": "RPG de Acao",
        "description": "Mergulhe no futuro sombrio de Night City em Cyberpunk 2077. Jogue como V, um mercenario cyberpunk em busca de um implante unico que e a chave para a imortalidade.",
        "release_date": "2020-12-10",
        "cover_image": "/static/img/cyberpunk2077.jpg",
    },
    {
        "title": "Celeste",
        "genre": "Plataforma",
        "description": "Ajude Madeline a subir o Monte Celeste em um jogo de plataforma desafiador e emocionante. Enfrente seus medos internos enquanto supera obstaculos cada vez mais dificeis.",
        "release_date": "2018-01-25",
        "cover_image": "/static/img/celeste.png",
    },
]


def seed_games():
    created_count = 0
    updated_count = 0

    for game_data in GAMES_DATA:
        game, created = Game.objects.get_or_create(
            title=game_data["title"],
            defaults={
                "genre": game_data["genre"],
                "description": game_data["description"],
                "release_date": game_data["release_date"],
                "cover_image": game_data["cover_image"],
            },
        )
        if created:
            created_count += 1
        else:
            game.genre = game_data["genre"]
            game.description = game_data["description"]
            game.release_date = game_data["release_date"]
            game.cover_image = game_data["cover_image"]
            game.save()
            updated_count += 1

    return {"created": created_count, "updated": updated_count}


def create_demo_superuser(
    username="admin",
    email="demo@example.com",
    password="admin123",
):
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )

    changed = False
    if created:
        user.set_password(password)
        changed = True
    else:
        if user.email != email:
            user.email = email
            changed = True
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not user.is_superuser:
            user.is_superuser = True
            changed = True

    user.set_password(password)
    changed = True

    if changed:
        user.save()

    return {"created": created, "username": username, "email": email, "user": user}


def seed_demo_library_for_user(user):
    game = Game.objects.filter(title="Cyberpunk 2077").first()
    if game is None:
        return {"seeded": False, "reason": "game_not_found"}

    library_entry, _ = LibraryEntry.objects.update_or_create(
        user=user,
        game=game,
        defaults={"status": "playing", "progress": 45},
    )
    Review.objects.update_or_create(
        user=user,
        game=game,
        defaults={
            "rating": 4,
            "comment": "Review de demonstracao criada automaticamente para validar a biblioteca do usuario admin.",
        },
    )

    return {
        "seeded": True,
        "game_title": library_entry.game.title,
        "status": library_entry.status,
        "progress": library_entry.progress,
    }
