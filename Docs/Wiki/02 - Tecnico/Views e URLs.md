---
title: Views e URLs
tipo: codigo
status: ativo
area: tecnico
projeto: GameVault
arquivo_relacionado:
  - core/views.py
  - core/urls.py
  - config/urls.py
tags:
  - gamevault
  - django
  - views
  - urls
---

# Views e URLs

As rotas do [[GameVault]] sao definidas em `core/urls.py` e apontam para funcoes em `core/views.py`. O arquivo `config/urls.py` inclui essas rotas na raiz do projeto.

## Entrada De Rotas

`config/urls.py` registra:

- `/admin/`: admin do Django.
- `/`: todas as rotas do app `core`.

## Rotas Do App Core

| Caminho | Nome | View | Finalidade |
| --- | --- | --- | --- |
| `/` | `core:home` | `home_view` | Pagina inicial com jogos em destaque. |
| `/sobre/` | `core:sobre` | `sobre_view` | Pagina institucional. |
| `/diferenciais/` | `core:diferenciais` | `diferenciais_view` | Pagina institucional de diferenciais. |
| `/login/` | `core:login` | `login_view` | Login de usuario. |
| `/logout/` | `core:logout` | `logout_view` | Encerramento de sessao. |
| `/password-reset/` | `core:password_reset` | `PasswordResetView` | Solicita redefinicao de senha por email. |
| `/password-reset/done/` | `core:password_reset_done` | `PasswordResetDoneView` | Confirma solicitacao de reset. |
| `/reset/<uidb64>/<token>/` | `core:password_reset_confirm` | `PasswordResetConfirmView` | Define nova senha. |
| `/reset/done/` | `core:password_reset_complete` | `PasswordResetCompleteView` | Confirma senha redefinida. |
| `/register/` | `core:register` | `register_view` | Cadastro de usuario. |
| `/profile/` | `core:profile` | `profile_view` | Perfil do usuario logado. |
| `/verify-email/<token>/` | `core:verify_email` | `verify_email_view` | Confirma email do usuario. |
| `/resend-verification-email/` | `core:resend_verification_email` | `resend_verification_email_view` | Reenvia verificacao de email. |
| `/library/` | `core:library` | `library_view` | Biblioteca pessoal. |
| `/add-to-library/` | `core:add_to_library` | `add_to_library_view` | Adiciona jogo via JSON. |
| `/update-library-entry/` | `core:update_library_entry` | `update_library_entry_view` | Atualiza status/progresso via JSON. |
| `/remove-from-library/` | `core:remove_from_library` | `remove_from_library_view` | Remove item da biblioteca via JSON. |
| `/catalog/` | `core:game_catalog` | `game_catalog_view` | Lista e busca jogos. |
| `/game/<game_id>/` | `core:game_detail` | `game_detail_view` | Exibe detalhes de um jogo. |
| `/game/<game_id>/review/` | `core:add_review` | `add_review_view` | Cria ou atualiza avaliacao via JSON. |

## Grupos De Views

### Paginas publicas

- `home_view`: busca ate seis jogos e adiciona metadados de capa para a home.
- `sobre_view`: renderiza `templates/pages/sobre.html`.
- `diferenciais_view`: renderiza `templates/pages/diferenciais.html`.
- `game_catalog_view`: lista jogos e aplica busca por titulo, genero ou descricao.
- `game_detail_view`: mostra detalhes do jogo e avaliacoes.

### Autenticacao

- `login_view`: usa `GameVaultAuthenticationForm`, aceita username ou email e redireciona para a biblioteca quando nao ha `next`.
- `logout_view`: encerra a sessao e redireciona para home.
- `register_view`: usa `GameVaultUserCreationForm`, cria usuario com email, envia verificacao e autentica.
- `profile_view`: exige login com `@login_required` e permite editar username/email.
- `verify_email_view`: valida token e marca email como verificado.
- `resend_verification_email_view`: exige login e reenvia link de verificacao.
- Views nativas de reset de senha: solicitam, confirmam e concluem redefinicao por email.

O layout base tambem pode exibir um banner global quando o usuario autenticado ainda nao verificou o email.

### Biblioteca e avaliacoes

- `library_view`: exige login e lista entradas do usuario com `select_related("game")`.
- `add_to_library_view`: exige login, aceita JSON e `POST` tradicional, e usa `get_or_create` para evitar duplicidade.
- `update_library_entry_view`: exige login e `POST`; altera status e progresso.
- `remove_from_library_view`: exige login e `POST`; remove entrada da biblioteca.
- `add_review_view`: exige login; cria ou atualiza avaliacao do usuario para um jogo.

## Helpers De Imagem

`core/views.py` tambem possui funcoes auxiliares para capas:

- `resolve_variant_cover_image`: procura uma versao local da imagem em `static/img/<variant>/`.
- `resolve_variant_cover_position`: define posicionamento visual por titulo e variante.
- `attach_variant_cover_metadata`: anexa atributos temporarios aos objetos `Game` usados nos templates.

## Fluxo Catalogo Para Biblioteca

```mermaid
sequenceDiagram
    participant U as Usuario
    participant C as Catalogo
    participant D as Detalhe
    participant B as Biblioteca
    participant DB as Banco
    U->>C: acessa /catalog/
    C->>DB: busca Game
    U->>D: abre /game/<id>/
    D->>DB: busca Game, Review e LibraryEntry
    U->>B: adiciona jogo
    B->>DB: cria ou atualiza LibraryEntry
```

## Notas Relacionadas

- [[Arquitetura]]
- [[Models]]
- [[Templates]]
- [[Autenticacao]]
- [[Catalogo de Jogos]]
- [[Biblioteca do Usuario]]
