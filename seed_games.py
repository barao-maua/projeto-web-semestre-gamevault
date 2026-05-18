import os
import sys
import django
from pathlib import Path

# Configura o Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.demo_data import seed_games

if __name__ == '__main__':
    result = seed_games()
    print(f"Total de jogos criados: {result['created']}")
    print(f"Total de jogos atualizados: {result['updated']}")
