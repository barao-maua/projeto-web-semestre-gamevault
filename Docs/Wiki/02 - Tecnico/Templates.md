---
title: Templates
tipo: codigo
status: ativo
area: tecnico
projeto: GameVault
arquivo_relacionado:
  - templates/base.html
  - templates/components/navbar.html
  - templates/components/footer.html
  - templates/pages/home.html
  - templates/catalog/game_catalog.html
  - templates/catalog/game_detail.html
  - templates/library/library.html
  - templates/registration/login.html
  - templates/registration/register.html
  - templates/registration/profile.html
tags:
  - gamevault
  - django
  - templates
  - html
---

# Templates

Os templates do [[GameVault]] ficam em `templates/` e usam a engine nativa do Django. O projeto segue uma estrutura MPA: cada rota renderiza uma pagina HTML no servidor.

## Estrutura

```text
templates/
  base.html
  components/
    navbar.html
    footer.html
  pages/
    home.html
    sobre.html
    diferenciais.html
  catalog/
    game_catalog.html
    game_detail.html
  library/
    library.html
  registration/
    login.html
    register.html
    profile.html
    password_reset_form.html
    password_reset_done.html
    password_reset_confirm.html
    password_reset_complete.html
    password_reset_email.html
    password_reset_subject.txt
    verify_email_email.txt
    verify_email_subject.txt
```

## Template Base

`templates/base.html` define a estrutura comum:

- Carrega `{% load static %}`.
- Define `lang="pt-BR"`.
- Inclui Bootstrap via CDN.
- Inclui Font Awesome via CDN.
- Carrega `base.css`, `components.css`, CSS especifico por pagina e `responsive.css`.
- Inclui `components/navbar.html` e `components/footer.html`.
- Renderiza mensagens do Django.
- Pode renderizar um banner global de email pendente de verificacao para usuarios autenticados.
- Expoe blocos `title`, `body_class`, `extra_css`, `content` e `extra_js`.

## Componentes

### Navbar

`templates/components/navbar.html` adapta links conforme autenticacao:

- Usuario logado: Inicio, Minha Biblioteca, Catalogo, Perfil e Sair.
- Visitante: Inicio, Biblioteca, Avaliacoes, Login e Cadastro.
- Mostra um chip de usuario com nome ou estado de visitante.
- O chip do usuario autenticado funciona como atalho para o perfil.
- O logout agora passa por um modal de confirmacao visual.

### Footer

`templates/components/footer.html` centraliza o rodape compartilhado.

## Paginas

### Home

`templates/pages/home.html` apresenta:

- Hero de apresentacao.
- Chamadas para login e cadastro.
- Cards estatisticos visuais.
- Jogos em destaque vindos de `featured_games`.

### Catalogo

`templates/catalog/game_catalog.html` apresenta:

- Campo de busca via query string `q`.
- Campo de busca com contraste reforcado e tratamento de autofill.
- Grid de jogos.
- Link para detalhes de cada jogo.
- Estado vazio quando nenhum jogo e encontrado.

### Detalhe Do Jogo

`templates/catalog/game_detail.html` apresenta:

- status atual do jogo na biblioteca, quando houver;
- modal visual para adicionar o jogo a biblioteca;
- etapa de confirmacao apos adicionar;
- sugestao opcional para avaliar o jogo;
- modal de avaliacao com feedback visual inline;
- lista de avaliacoes existentes.

### Biblioteca

`templates/library/library.html` apresenta:

- Entradas da biblioteca do usuario.
- Status visual da entrada.
- Coracoes dinamicos baseados na avaliacao pessoal do usuario.
- Modal para editar status da entrada.
- Acao JavaScript para remover da biblioteca usando `fetch`.

### Registro, Login e Perfil

Os templates em `templates/registration/` suportam autenticacao, perfil, verificacao de email e recuperacao de senha.

- `login.html`: login por usuario ou email e link de esqueci minha senha.
- `register.html`: cadastro com email obrigatorio e checklist visual de senha.
- `profile.html`: edicao de username/email, status de verificacao e reenvio.
- `password_reset_*.html`: fluxo completo de redefinicao de senha.
- `verify_email_*.txt`: assunto e corpo do email de verificacao.

## Relacao Com CSS

Cada pagina usa o bloco `extra_css` para carregar um CSS especifico:

- `home.html` -> `static/css/pages/home.css`
- `game_catalog.html` -> `static/css/pages/catalog.css`
- `game_detail.html` -> `static/css/pages/game-detail.css`
- `library.html` -> `static/css/pages/library.css`
- `login.html` e `register.html` -> `static/css/pages/auth.css`
- `profile.html` -> `static/css/pages/profile.css`
- `sobre.html` -> `static/css/pages/sobre.css`
- `diferenciais.html` -> `static/css/pages/diferenciais.css`

## Observacao De Evolucao

Parte importante dos templates foi refinada em rodadas iterativas apos testes reais. Isso explica a presenca de modais visuais, feedbacks inline, banners de verificacao e pequenos ajustes de contraste e navegacao que nao estavam presentes na estrutura inicial.

## Notas Relacionadas

- [[Arquitetura]]
- [[Views e URLs]]
- [[Static e CSS]]
- [[Paginas Institucionais]]
