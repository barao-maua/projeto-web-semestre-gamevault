import re
from pathlib import Path

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Review, UserProfile


AVATAR_MAX_FILE_SIZE = 1024 * 1024
AVATAR_MAX_DIMENSION = 184
ALLOWED_AVATAR_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_AVATAR_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}


def validate_gamevault_password_strength(password):
    if len(password) < 8:
        raise forms.ValidationError("A senha precisa ter pelo menos 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        raise forms.ValidationError("A senha deve conter pelo menos uma letra maiuscula.")
    if not re.search(r"[a-z]", password):
        raise forms.ValidationError("A senha deve conter pelo menos uma letra minuscula.")
    if not re.search(r"\d", password):
        raise forms.ValidationError("A senha deve conter pelo menos um numero.")
    if not re.search(r"[^A-Za-z0-9]", password):
        raise forms.ValidationError(
            "A senha deve conter pelo menos um caractere especial."
        )


class GameVaultAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Usuario, email ou senha invalidos.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario ou email"
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Digite seu usuario ou email", "autocomplete": "username"}
        )
        self.fields["password"].label = "Senha"
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Digite sua senha", "autocomplete": "current-password"}
        )

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            auth_username = username_or_email
            if "@" in username_or_email:
                matched_user = User.objects.filter(
                    email__iexact=username_or_email.strip()
                ).first()
                if matched_user is not None:
                    auth_username = matched_user.username

            self.user_cache = authenticate(
                self.request,
                username=auth_username,
                password=password,
            )

            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"username": self.username_field.verbose_name},
                )

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class GameVaultUserCreationForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        "password_mismatch": "Os dois campos de senha nao correspondem.",
    }
    email = forms.EmailField(label="Email", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nome de usuario"
        self.fields["username"].help_text = "Obrigatorio. Use letras, numeros e @/./+/-/_ apenas."
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Exemplo: bruno", "autocomplete": "username"}
        )

        self.fields["email"].label = "Email"
        self.fields["email"].help_text = "Obrigatorio. Use um email valido e unico."
        self.fields["email"].widget.attrs.update(
            {"placeholder": "voce@email.com", "autocomplete": "email"}
        )

        self.fields["password1"].label = "Senha"
        self.fields["password1"].help_text = ""
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Digite sua senha", "autocomplete": "new-password"}
        )

        self.fields["password2"].label = "Confirmar senha"
        self.fields["password2"].help_text = ""
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Repita a senha", "autocomplete": "new-password"}
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este email ja esta em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        validate_gamevault_password_strength(password)
        return password


class GameVaultProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nome de usuario"
        self.fields["username"].help_text = "Use letras, numeros e @/./+/-/_ apenas."
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Exemplo: bruno", "autocomplete": "username"}
        )
        self.fields["email"].label = "Email"
        self.fields["email"].required = True
        self.fields["email"].help_text = "Use um email valido e unico."
        self.fields["email"].widget.attrs.update(
            {"placeholder": "voce@email.com", "autocomplete": "email"}
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        queryset = User.objects.filter(email__iexact=email)
        if self.user is not None:
            queryset = queryset.exclude(pk=self.user.pk)
        if queryset.exists():
            raise forms.ValidationError("Este email ja esta em uso.")
        return email


class GameVaultSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].label = "Nova senha"
        self.fields["new_password1"].help_text = ""
        self.fields["new_password1"].widget.attrs.update(
            {"placeholder": "Digite sua nova senha", "autocomplete": "new-password"}
        )
        self.fields["new_password2"].label = "Confirmação da nova senha"
        self.fields["new_password2"].help_text = ""
        self.fields["new_password2"].widget.attrs.update(
            {"placeholder": "Repita a nova senha", "autocomplete": "new-password"}
        )

    def clean_new_password1(self):
        password = self.cleaned_data["new_password1"]
        validate_gamevault_password_strength(password)
        return password


class GameVaultReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 1 or rating > 5:
            raise forms.ValidationError("A nota deve estar entre 1 e 5.")
        return rating


class GameVaultAvatarForm(forms.ModelForm):
    remove_avatar = forms.BooleanField(required=False, label="Remover foto atual")

    class Meta:
        model = UserProfile
        fields = ("avatar",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].label = "Foto de perfil"
        self.fields["avatar"].error_messages["invalid_image"] = "Envie uma imagem valida."

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if not avatar:
            return avatar

        file_extension = Path(avatar.name).suffix.lower()
        if file_extension not in ALLOWED_AVATAR_EXTENSIONS:
            raise forms.ValidationError(
                "Envie uma imagem valida nos formatos JPG, PNG, GIF ou WEBP."
            )

        content_type = getattr(avatar, "content_type", "") or ""
        if content_type and content_type.lower() not in ALLOWED_AVATAR_CONTENT_TYPES:
            raise forms.ValidationError(
                "Envie uma imagem valida nos formatos JPG, PNG, GIF ou WEBP."
            )

        if avatar.size > AVATAR_MAX_FILE_SIZE:
            raise forms.ValidationError("A imagem deve ter no maximo 1 MB.")

        width = getattr(avatar, "image", None)
        if width is None:
            raise forms.ValidationError("Envie uma imagem valida.")

        if avatar.image.width > AVATAR_MAX_DIMENSION or avatar.image.height > AVATAR_MAX_DIMENSION:
            raise forms.ValidationError("A imagem deve ter no maximo 184x184 pixels.")

        return avatar

    def clean(self):
        cleaned_data = super().clean()
        avatar = cleaned_data.get("avatar")
        remove_avatar = cleaned_data.get("remove_avatar")

        if remove_avatar and not avatar:
            self._errors.pop("avatar", None)
            cleaned_data["avatar"] = None
            return cleaned_data

        if not avatar and not remove_avatar and not getattr(self.instance, "avatar", None):
            return cleaned_data

        return cleaned_data
