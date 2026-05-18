# Gerado manualmente para adicionar verificacao de email.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserEmailVerification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_verified",
                    models.BooleanField(default=False, verbose_name="Email verificado"),
                ),
                (
                    "verified_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Verificado em"
                    ),
                ),
                (
                    "last_verification_email_sent_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Ultimo envio de verificacao",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_verification",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuario",
                    ),
                ),
            ],
            options={
                "verbose_name": "Verificacao de Email",
                "verbose_name_plural": "Verificacoes de Email",
            },
        ),
    ]
