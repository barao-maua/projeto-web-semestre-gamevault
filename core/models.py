from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    """Modelo base para jogos no catálogo"""

    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    release_date = models.DateField(
        null=True, blank=True, verbose_name="Data de Lançamento"
    )
    genre = models.CharField(max_length=100, blank=True, verbose_name="Gênero")
    cover_image = models.URLField(blank=True, verbose_name="URL da Capa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"
        ordering = ["title"]

    def __str__(self):
        return self.title


class LibraryEntry(models.Model):
    """Entrada da biblioteca pessoal do usuário"""

    STATUS_CHOICES = [
        ("playing", "Jogando"),
        ("completed", "Concluído"),
        ("paused", "Pausado"),
        ("dropped", "Abandonado"),
        ("plan_to_play", "Planejo Jogar"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Jogo")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="plan_to_play",
        verbose_name="Status",
    )
    progress = models.IntegerField(
        default=0,
        help_text="Progresso em porcentagem (0-100)",
        verbose_name="Progresso",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Adicionado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Entrada da Biblioteca"
        verbose_name_plural = "Entradas da Biblioteca"
        unique_together = [
            "user",
            "game",
        ]  # Um usuário só pode ter uma entrada por jogo
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"


class Review(models.Model):
    """Avaliação de um jogo por um usuário"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Jogo")
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], verbose_name="Nota (1-5)"
    )
    comment = models.TextField(blank=True, verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = [
            "user",
            "game",
        ]  # Um usuário só pode ter uma avaliação por jogo
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.rating}/5)"


class GameList(models.Model):
    """Lista personalizada de jogos (ex: Favoritos, Jogar em 2026)"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    name = models.CharField(max_length=100, verbose_name="Nome da Lista")
    description = models.TextField(blank=True, verbose_name="Descrição")
    is_public = models.BooleanField(default=False, verbose_name="Lista Pública")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Lista de Jogos"
        verbose_name_plural = "Listas de Jogos"
        unique_together = [
            "user",
            "name",
        ]  # Um usuário não pode ter duas listas com o mesmo nome
        ordering = ["name"]

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class GameListItem(models.Model):
    """Item dentro de uma lista personalizada"""

    game_list = models.ForeignKey(
        GameList, on_delete=models.CASCADE, verbose_name="Lista"
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Jogo")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Adicionado em")

    class Meta:
        verbose_name = "Item da Lista"
        verbose_name_plural = "Itens da Lista"
        unique_together = [
            "game_list",
            "game",
        ]  # Um jogo só pode aparecer uma vez em uma lista
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.game_list.name} - {self.game.title}"
