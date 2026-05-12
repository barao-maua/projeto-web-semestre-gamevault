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

## Cadastro

`register_view` usa `UserCreationForm`.

Fluxo:

1. Usuario acessa `/register/`.
2. View exibe o formulario de cadastro.
3. No `POST`, o formulario e validado.
4. Se valido, o usuario e salvo.
5. O sistema faz login automatico.
6. O usuario e redirecionado para a home.

## Login

`login_view` usa `AuthenticationForm` e `authenticate`.

Fluxo:

1. Usuario acessa `/login/`.
2. View exibe campos de usuario e senha.
3. No `POST`, a view valida as credenciais.
4. Se autenticado, a sessao e iniciada.
5. O usuario e redirecionado para a home.

## Logout

`logout_view` encerra a sessao com `logout(request)` e redireciona para a home.

## Perfil

`profile_view` usa `@login_required`.

O template mostra:

- username;
- email, quando informado;
- data de cadastro;
- link para logout.

## Impacto Na Navegacao

`templates/components/navbar.html` muda os links conforme `user.is_authenticated`:

- Visitante: Inicio, Biblioteca, Avaliacoes, Login e Cadastro.
- Usuario logado: Inicio, Minha Biblioteca, Catalogo, Perfil e Sair.

## Relacoes Com Outras Areas

- [[Biblioteca do Usuario]] depende de usuario autenticado.
- [[Catalogo de Jogos]] pode ser navegado por visitantes, mas interacoes exigem login.
- [[Views e URLs]] documenta as rotas correspondentes.
