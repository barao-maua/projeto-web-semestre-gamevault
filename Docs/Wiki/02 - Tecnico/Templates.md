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
- Expoe blocos `title`, `body_class`, `extra_css`, `content` e `extra_js`.

## Componentes

### Navbar

`templates/components/navbar.html` adapta links conforme autenticacao:

- Usuario logado: Inicio, Minha Biblioteca, Catalogo, Perfil e Sair.
- Visitante: Inicio, Biblioteca, Avaliacoes, Login e Cadastro.
- Mostra um chip de usuario com nome ou estado de visitante.

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
- Grid de jogos.
- Link para detalhes de cada jogo.
- Estado vazio quando nenhum jogo e encontrado.

### Biblioteca

`templates/library/library.html` apresenta:

- Entradas da biblioteca do usuario.
- Status visual da entrada.
- Link para editar via detalhe do jogo.
- Acao JavaScript para remover da biblioteca usando `fetch`.

### Registro, Login e Perfil

Os templates em `templates/registration/` suportam autenticacao e perfil usando views baseadas nos formularios padrao do Django.

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

## Notas Relacionadas

- [[Arquitetura]]
- [[Views e URLs]]
- [[Static e CSS]]
- [[Paginas Institucionais]]
