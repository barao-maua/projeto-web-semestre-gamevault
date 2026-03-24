import os
import sys
import django
from pathlib import Path

# Configura o Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Game

def seed_games():
    games_data = [
        {
            'title': 'Hollow Knight',
            'genre': 'Metroidvania',
            'description': 'Explore um mundo interconectado em Hollow Knight, um jogo de ação e aventura em 2D desenhado à mão. Desça às profundezas de Hallownest, descubra seus segredos e supere seus desafios.',
            'release_date': '2017-02-24',
            'cover_image': '/static/img/HollowKnight.jpg'
        },
        {
            'title': 'Hades',
            'genre': 'Roguelike',
            'description': 'Desafie o deus dos mortos em Hades, um jogo de ação e estratégia onde você tenta escapar do submundo grego. Lute, morra e tente novamente, cada vez mais forte.',
            'release_date': '2020-09-17',
            'cover_image': '/static/img/Hades.jpg'
        },
        {
            'title': 'Elden Ring',
            'genre': 'RPG de Ação',
            'description': 'Explore as Terras Intermédias em Elden Ring, um RPG de ação de mundo aberto criado por Hidetaka Miyazaki e George R. R. Martin. Enfrente desafios épicos e descubra um mito profundo.',
            'release_date': '2022-02-25',
            'cover_image': '/static/img/EldenRing.png'
        },
        {
            'title': 'Disco Elysium',
            'genre': 'RPG',
            'description': 'Disco Elysium é um RPG inovador onde você é um detetive com amnésia tentando resolver um caso em uma cidade decadente. Suas habilidades são suas vozes internas.',
            'release_date': '2019-10-15',
            'cover_image': '/static/img/discoelysium.jpg'
        },
        {
            'title': 'Cyberpunk 2077',
            'genre': 'RPG de Ação',
            'description': 'Mergulhe no futuro sombrio de Night City em Cyberpunk 2077. Jogue como V, um mercenário cyberpunk em busca de um implante único que é a chave para a imortalidade.',
            'release_date': '2020-12-10',
            'cover_image': '/static/img/cyberpunk2077.jpg'
        },
        {
            'title': 'Celeste',
            'genre': 'Plataforma',
            'description': 'Ajude Madeline a subir o Monte Celeste em um jogo de plataforma desafiador e emocionante. Enfrente seus medos internos enquanto supera obstáculos cada vez mais difíceis.',
            'release_date': '2018-01-25',
            'cover_image': '/static/img/celeste.png'
        }
    ]

    created_count = 0
    updated_count = 0

    for game_data in games_data:
        game, created = Game.objects.get_or_create(
            title=game_data['title'],
            defaults={
                'genre': game_data['genre'],
                'description': game_data['description'],
                'release_date': game_data['release_date'],
                'cover_image': game_data['cover_image']
            }
        )
        if created:
            created_count += 1
            print(f'Criado: {game.title}')
        else:
            # Atualiza os campos se o jogo já existir
            game.genre = game_data['genre']
            game.description = game_data['description']
            game.release_date = game_data['release_date']
            game.cover_image = game_data['cover_image']
            game.save()
            updated_count += 1
            print(f'Atualizado: {game.title}')

    print(f'\nTotal de jogos criados: {created_count}')
    print(f'Total de jogos atualizados: {updated_count}')

if __name__ == '__main__':
    seed_games()
