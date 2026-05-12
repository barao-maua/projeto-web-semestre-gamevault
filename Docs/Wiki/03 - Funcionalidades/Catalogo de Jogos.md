---
title: Catalogo de Jogos
aliases:
  - Catálogo de Jogos
tipo: funcionalidade
status: ativo
area: funcionalidades
projeto: GameVault
arquivo_relacionado:
  - core/views.py
  - templates/catalog/game_catalog.html
  - templates/catalog/game_detail.html
  - static/css/pages/catalog.css
  - static/css/pages/game-detail.css
tags:
  - gamevault
  - catalogo
  - jogos
---

# Catalogo de Jogos

O catalogo permite visualizar os jogos cadastrados no sistema, buscar por termo e abrir a pagina de detalhe de cada jogo.

## Rotas

| Caminho | Nome | View | Template |
| --- | --- | --- | --- |
| `/catalog/` | `core:game_catalog` | `game_catalog_view` | `catalog/game_catalog.html` |
| `/game/<game_id>/` | `core:game_detail` | `game_detail_view` | `catalog/game_detail.html` |

## Catalogo

`game_catalog_view` busca jogos com `Game.objects.all()` e aceita o parametro `q` na query string.

A busca filtra por:

- `title`;
- `genre`;
- `description`.

O template renderiza:

- titulo da pagina;
- formulario de busca;
- grid de jogos;
- capa ou placeholder;
- genero;
- descricao resumida;
- link para detalhes.

## Detalhe Do Jogo

`game_detail_view` busca um `Game` por ID, carrega avaliacoes e verifica se o jogo ja esta na biblioteca do usuario autenticado.

O template mostra:

- capa;
- titulo;
- genero usado visualmente como plataforma;
- data de lancamento;
- descricao;
- status na biblioteca, quando existe;
- progresso;
- avaliacoes da comunidade;
- modal de avaliacao para usuario autenticado;
- acao para adicionar a biblioteca.

## Interacoes

Na pagina de detalhe, o JavaScript permite:

- adicionar o jogo a biblioteca via `fetch` para `core:add_to_library`;
- selecionar status inicial por `prompt`;
- abrir e fechar o modal de avaliacao;
- enviar avaliacao via `fetch` para `core:add_review`.

## Capas E Variantes

`core/views.py` possui helpers para usar variantes locais de capa:

- `static/img/home/` para a home;
- `static/img/catalog/` para o catalogo.

Se a variante existir, ela substitui a URL original da capa apenas na renderizacao.

## Relacoes Com Outras Areas

- [[Biblioteca do Usuario]] usa jogos vindos do catalogo.
- [[Models]] documenta `Game`, `LibraryEntry` e `Review`.
- [[Views e URLs]] documenta as views do catalogo e detalhe.
- [[Static e CSS]] documenta os estilos de catalogo e detalhe.
