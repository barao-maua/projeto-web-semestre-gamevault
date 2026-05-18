---
title: Autenticacao
aliases:
  - Autenticação
tipo: funcionalidade
status: ativo
area: funcionalidades
projeto: GameVault
arquivo_relacionado:
  - core/views.py
  - core/urls.py
  - templates/registration/login.html
  - templates/registration/register.html
  - templates/registration/profile.html
tags:
  - gamevault
  - autenticacao
  - django
---

# Autenticacao

A autenticacao do [[GameVault]] usa os recursos padrao do Django para cadastro, login, logout e protecao de paginas que exigem usuario autenticado.

## Rotas

| Caminho | Nome | View | Template |
| --- | --- | --- | --- |
| `/login/` | `core:login` | `login_view` | `registration/login.html` |
| `/logout/` | `core:logout` | `logout_view` | nenhum template; redireciona |
| `/register/` | `core:register` | `register_view` | `registration/register.html` |
| `/profile/` | `core:profile` | `profile_view` | `registration/profile.html` |
| `/verify-email/<token>/` | `core:verify_email` | `verify_email_view` | nenhum template; redireciona |
| `/resend-verification-email/` | `core:resend_verification_email` | `resend_verification_email_view` | nenhum template; redireciona |
| `/password-reset/` | `core:password_reset` | `PasswordResetView` | `registration/password_reset_form.html` |
| `/password-reset/done/` | `core:password_reset_done` | `PasswordResetDoneView` | `registration/password_reset_done.html` |
| `/reset/<uidb64>/<token>/` | `core:password_reset_confirm` | `PasswordResetConfirmView` | `registration/password_reset_confirm.html` |
| `/reset/done/` | `core:password_reset_complete` | `PasswordResetCompleteView` | `registration/password_reset_complete.html` |

## Cadastro

`register_view` usa `GameVaultUserCreationForm`, baseado em `UserCreationForm`, com email obrigatorio e unico.

> [!note]
> A evolucao planejada para email unico, verificacao por email e redefinicao de senha esta documentada em [[Spec - Email Verificacao e Reset de Senha]].

Fluxo:

1. Usuario acessa `/register/`.
2. View exibe o formulario de cadastro.
3. No `POST`, o formulario e validado.
4. Se valido, o usuario e salvo com email.
5. O sistema cria registro de verificacao de email pendente.
6. O sistema tenta enviar link de verificacao por email.
7. O sistema faz login automatico.
8. O usuario e redirecionado para a home.

## Login

`login_view` usa `GameVaultAuthenticationForm` e `authenticate`.

Fluxo:

1. Usuario acessa `/login/`.
2. View exibe campo de usuario ou email e senha.
3. No `POST`, a view tenta autenticar por username ou email.
4. Se autenticado, a sessao e iniciada.
5. Se houver `next`, o destino original e respeitado.
6. Caso contrario, o usuario e redirecionado para a biblioteca.

## Logout

`logout_view` encerra a sessao com `logout(request)` e redireciona para a home.

## Perfil

`profile_view` usa `@login_required` e permite editar username/email.

O template mostra:

- username;
- email;
- status de verificacao do email;
- data de cadastro;
- botao para reenviar verificacao quando pendente;
- link para logout.

Se o email for alterado, a verificacao anterior e invalidada e um novo link e enviado.

Enquanto o email estiver pendente, um banner global pode aparecer no layout com atalhos para reenviar verificacao ou abrir o perfil.

## Recuperacao De Senha

O fluxo de esqueci minha senha usa as views nativas do Django e envia link de redefinicao por email.

Fluxo:

1. Usuario acessa `/password-reset/` pelo link do login.
2. Usuario informa o email cadastrado.
3. O sistema envia um link de redefinicao.
4. Usuario acessa o link e define uma nova senha.
5. Usuario volta ao login e entra com a nova senha.

## Impacto Na Navegacao

`templates/components/navbar.html` muda os links conforme `user.is_authenticated`:

- Visitante: Inicio, Biblioteca, Avaliacoes, Login e Cadastro.
- Usuario logado: Inicio, Minha Biblioteca, Catalogo, Perfil e Sair.

## Relacoes Com Outras Areas

- [[Biblioteca do Usuario]] depende de usuario autenticado.
- [[Catalogo de Jogos]] pode ser navegado por visitantes, mas interacoes exigem login.
- [[Views e URLs]] documenta as rotas correspondentes.
