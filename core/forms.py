from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class GameVaultAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nome de usuario"
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Digite seu nome de usuario", "autocomplete": "username"}
        )
        self.fields["password"].label = "Senha"
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Digite sua senha", "autocomplete": "current-password"}
        )


class GameVaultUserCreationForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        "password_mismatch": "Os dois campos de senha nao correspondem.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nome de usuario"
        self.fields["username"].help_text = "Obrigatorio. Use letras, numeros e @/./+/-/_ apenas."
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Exemplo: bruno", "autocomplete": "username"}
        )

        self.fields["password1"].label = "Senha"
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Digite sua senha", "autocomplete": "new-password"}
        )

        self.fields["password2"].label = "Confirmar senha"
        self.fields["password2"].help_text = "Digite a mesma senha novamente."
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Repita a senha", "autocomplete": "new-password"}
        )
