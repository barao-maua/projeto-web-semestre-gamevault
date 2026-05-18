---
title: Spec - Email Verificacao e Reset de Senha
aliases:
  - Spec Email Verificacao Reset Senha
  - Email Verificacao e Reset de Senha
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - autenticacao
  - email
  - senha
  - smtp
---

# Spec - Email Verificacao e Reset de Senha

Esta nota registra o escopo completo para evoluir a [[Autenticacao]] do [[GameVault]] com email unico, verificacao por email e fluxo de esqueci minha senha.

## Decisoes Fechadas

- Email sera obrigatorio no cadastro.
- Email sera unico por usuario.
- Login continua sendo feito com username e senha.
- Usuario podera entrar mesmo antes de verificar o email.
- Verificacao de email sera por link enviado por SMTP do Google.
- Redefinicao de senha sera feita por email.
- Recuperacao de senha deve usar as views nativas do Django sempre que possivel.
- Credenciais SMTP nao devem ser versionadas no repositorio.

## Objetivo

Implementar:

- campo de email no cadastro;
- validacao de email unico;
- perfil editavel com username e email;
- status de email verificado ou pendente;
- envio de link de verificacao de email;
- reenvio de verificacao pelo perfil;
- invalidacao da verificacao quando o email for alterado;
- fluxo de esqueci minha senha com redefinicao por email.

## Fora Do Escopo

- Login por email.
- Bloquear login enquanto o email nao estiver verificado.
- Troca de senha dentro do perfil.
- Rate limit avancado para reenvio de email.
- Fila assincrona de emails.
- Template HTML sofisticado para email.

## Estado Atual

- `User` padrao do Django ja possui campo `email`.
- `GameVaultUserCreationForm` coleta email obrigatorio e unico.
- `profile_view` renderiza e processa formulario de perfil.
- `templates/registration/profile.html` permite editar username/email e mostra status de verificacao.
- `config/settings.py` possui configuracao SMTP por variaveis de ambiente.
- Rotas/templates de `password_reset` foram adicionados.
- `templates/registration/login.html` possui link de esqueci minha senha.

## Arquivos Impactados

- `core/models.py`
- `core/forms.py`
- `core/views.py`
- `core/urls.py`
- `config/settings.py`
- `config/urls.py`
- `templates/registration/register.html`
- `templates/registration/profile.html`
- `templates/registration/login.html`
- `templates/registration/password_reset_form.html`
- `templates/registration/password_reset_done.html`
- `templates/registration/password_reset_confirm.html`
- `templates/registration/password_reset_complete.html`
- `templates/registration/password_reset_email.html`
- `templates/registration/password_reset_subject.txt`
- `templates/registration/verify_email_email.txt`
- `templates/registration/verify_email_subject.txt`

## Modelagem

Manter o `User` padrao do Django.

Criar um model auxiliar em `core/models.py`:

```python
class UserEmailVerification(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="email_verification",
    )
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    last_verification_email_sent_at = models.DateTimeField(null=True, blank=True)
```

Regras:

- cada usuario tem no maximo um registro de verificacao;
- novo usuario inicia com `is_verified=False`;
- quando o email for alterado, `is_verified` volta para `False`;
- quando o email for alterado, `verified_at` volta para `None`.

## Formularios

### Cadastro

Atualizar `GameVaultUserCreationForm` em `core/forms.py`.

Campos:

- `username`;
- `email`;
- `password1`;
- `password2`.

Regras:

- `email` obrigatorio;
- validar unicidade do email;
- comparar email com normalizacao por lowercase;
- salvar email em `user.email`.

### Perfil

Criar `GameVaultProfileForm` em `core/forms.py`.

Campos:

- `username`;
- `email`.

Regras:

- `email` obrigatorio;
- `email` unico, exceto para o usuario atual;
- `username` deve respeitar validacoes do `User`;
- a view deve detectar se o email mudou.

## Views

### `register_view`

Fluxo esperado:

1. Receber `POST` do cadastro.
2. Validar `GameVaultUserCreationForm`.
3. Criar `User` com email.
4. Criar ou garantir `UserEmailVerification` pendente.
5. Tentar enviar email de verificacao.
6. Fazer login automatico, mantendo o comportamento atual.
7. Redirecionar para home ou perfil.

Mensagens:

- sucesso com email enviado: `Conta criada com sucesso. Enviamos um link de verificacao para seu email.`
- sucesso com falha no envio: `Conta criada com sucesso, mas nao foi possivel enviar o email de verificacao agora.`
- erro de formulario: manter erros reais por campo.

### `profile_view`

Transformar em GET + POST.

GET:

- carregar `GameVaultProfileForm` com `request.user`;
- carregar estado de verificacao;
- renderizar perfil editavel.

POST:

- validar formulario;
- detectar se email mudou;
- salvar `username` e `email`;
- se email mudou, invalidar verificacao;
- tentar reenviar verificacao automaticamente;
- exibir mensagem de sucesso ou falha de envio.

### `verify_email_view`

Nova view.

Rota:

```text
/verify-email/<uidb64>/<token>/
```

Fluxo:

1. Decodificar `uidb64`.
2. Buscar usuario.
3. Validar token.
4. Criar ou obter `UserEmailVerification`.
5. Marcar `is_verified=True`.
6. Preencher `verified_at=timezone.now()`.
7. Redirecionar com mensagem de sucesso.

Falhas:

- token invalido;
- usuario inexistente;
- uid invalido.

Mensagem de erro sugerida:

```text
Link de verificacao invalido ou expirado. Solicite um novo email de verificacao.
```

### `resend_verification_email_view`

Nova view protegida por login.

Rota:

```text
/resend-verification-email/
```

Metodo:

- `POST`.

Fluxo:

1. Verificar usuario autenticado.
2. Obter/criar registro de verificacao.
3. Se ja verificado, mostrar mensagem informativa.
4. Se pendente, enviar novo email.
5. Atualizar `last_verification_email_sent_at`.

## Password Reset

Usar views nativas do Django:

- `PasswordResetView`;
- `PasswordResetDoneView`;
- `PasswordResetConfirmView`;
- `PasswordResetCompleteView`.

Rotas esperadas:

```text
/password-reset/
/password-reset/done/
/reset/<uidb64>/<token>/
/reset/done/
```

Templates esperados:

- `registration/password_reset_form.html`;
- `registration/password_reset_done.html`;
- `registration/password_reset_confirm.html`;
- `registration/password_reset_complete.html`;
- `registration/password_reset_email.html`;
- `registration/password_reset_subject.txt`.

Regras:

- usuario informa email;
- sistema envia link se houver usuario correspondente;
- tela nao deve expor claramente se o email existe ou nao;
- usuario redefine a senha pelo link;
- apos sucesso, pode voltar ao login.

## SMTP Google

Configurar em `config/settings.py` usando variaveis de ambiente.

Variaveis:

```text
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
EMAIL_TIMEOUT=10
SITE_BASE_URL=
```

Config esperada:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "10"))
SITE_BASE_URL = os.getenv("SITE_BASE_URL", "http://127.0.0.1:8000")
```

Importante:

- usar App Password do Google;
- nao usar senha normal da conta Google;
- nao commitar credenciais;
- documentar variaveis em exemplo seguro, sem valores reais.

## Templates E UX

### Cadastro

Adicionar campo `email` entre username e senha.

Campos:

- nome de usuario;
- email;
- senha;
- confirmar senha.

### Perfil

Transformar tela em formulario.

Mostrar:

- username;
- email;
- status do email;
- data de cadastro;
- botao `Salvar alteracoes`;
- botao `Reenviar verificacao` quando email estiver pendente;
- link/botao `Sair`.

Estados visuais:

- `Email verificado`;
- `Email pendente de verificacao`.

### Login

Adicionar link:

```text
Esqueci minha senha
```

### Emails

Email de verificacao:

- informar usuario;
- explicar objetivo;
- incluir link;
- avisar para ignorar se nao solicitou.

Email de reset de senha:

- usar padrao do Django adaptado ao visual/texto do GameVault.

## Helpers Recomendados

Criar helpers em `core/views.py` ou `core/utils.py`.

Sugestoes:

- `get_or_create_email_verification(user)`;
- `invalidate_email_verification(user)`;
- `send_verification_email(request, user)`;
- `build_verification_url(request, user)`.

## Seguranca

- Validar email unico no backend.
- Nao versionar senha SMTP.
- Manter CSRF nos formularios.
- Proteger reenvio com login.
- Invalidar verificacao ao trocar email.
- Usar tokens nativos do Django para links sensiveis.
- Usar views nativas para reset de senha.
- Nao bloquear o cadastro caso o envio de verificacao falhe.

## Checklist De Implementacao

- [x] Criar `UserEmailVerification` em `core/models.py`.
- [x] Criar migration.
- [x] Adicionar `email` obrigatorio em `GameVaultUserCreationForm`.
- [x] Validar email unico no cadastro.
- [x] Salvar `user.email` no cadastro.
- [x] Criar `GameVaultProfileForm`.
- [x] Transformar `profile_view` em GET + POST.
- [x] Exibir status de verificacao no perfil.
- [x] Invalidar verificacao quando email mudar.
- [x] Criar helper de envio de email de verificacao.
- [x] Criar template de email de verificacao.
- [x] Criar assunto do email de verificacao.
- [x] Criar `verify_email_view`.
- [x] Criar `resend_verification_email_view`.
- [x] Adicionar rotas de verificacao em `core/urls.py`.
- [x] Configurar SMTP Google em `config/settings.py`.
- [x] Adicionar variaveis de ambiente necessarias.
- [x] Adicionar link `Esqueci minha senha` no login.
- [x] Adicionar rotas nativas de password reset.
- [x] Criar templates de password reset.
- [x] Testar cadastro com email novo.
- [x] Testar bloqueio de email duplicado.
- [x] Testar envio de verificacao.
- [x] Testar clique no link de verificacao.
- [x] Testar perfil mostrando email verificado.
- [x] Testar troca de email voltando para pendente.
- [x] Testar reenvio de verificacao.
- [x] Testar esqueci minha senha.
- [x] Testar login com senha redefinida.
- [x] Atualizar [[Autenticacao]].
- [x] Atualizar [[Views e URLs]].
- [x] Atualizar [[Decisoes Tecnicas]].

## Criterios De Pronto

- Usuario nao consegue cadastrar email duplicado.
- Usuario novo e criado com email salvo.
- Usuario novo recebe link de verificacao.
- Usuario consegue entrar mesmo com email pendente.
- Perfil mostra status correto do email.
- Link de verificacao marca email como verificado.
- Trocar email no perfil invalida verificacao anterior.
- Reenvio de verificacao funciona.
- Login mostra link de esqueci minha senha.
- Usuario recebe email de reset de senha.
- Usuario consegue redefinir senha pelo link.
- Usuario consegue logar com a nova senha.

## Plano De Teste Manual

1. Cadastrar usuario novo com email valido.
2. Confirmar que o usuario entra automaticamente.
3. Abrir perfil e verificar status pendente.
4. Abrir email recebido e clicar no link.
5. Conferir status verificado no perfil.
6. Alterar email no perfil.
7. Conferir status pendente novamente.
8. Clicar em reenviar verificacao.
9. Confirmar recebimento do novo email.
10. Tentar cadastrar outro usuario com o mesmo email.
11. Confirmar que o cadastro bloqueia duplicidade.
12. Abrir login.
13. Clicar em esqueci minha senha.
14. Informar email cadastrado.
15. Abrir link recebido.
16. Definir nova senha.
17. Entrar com a nova senha.

## Notas Relacionadas

- [[Autenticacao]]
- [[Views e URLs]]
- [[Decisoes Tecnicas]]
- [[Entrega Final - Alternativa A]]
