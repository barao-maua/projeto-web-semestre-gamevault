---
title: Paginas Institucionais
aliases:
  - Páginas Institucionais
tipo: funcionalidade
status: ativo
area: funcionalidades
projeto: GameVault
arquivo_relacionado:
  - templates/pages/home.html
  - templates/pages/sobre.html
  - templates/pages/diferenciais.html
  - core/views.py
tags:
  - gamevault
  - paginas
  - produto
---

# Paginas Institucionais

As paginas institucionais apresentam o conceito do [[GameVault]], demonstram telas e ajudam na navegacao inicial do projeto.

## Rotas

| Caminho | Nome | View | Template |
| --- | --- | --- | --- |
| `/` | `core:home` | `home_view` | `pages/home.html` |
| `/sobre/` | `core:sobre` | `sobre_view` | `pages/sobre.html` |
| `/diferenciais/` | `core:diferenciais` | `diferenciais_view` | `pages/diferenciais.html` |

## Home

`pages/home.html` e a primeira pagina da aplicacao.

Ela apresenta:

- proposta do produto;
- chamadas para login e cadastro;
- cards visuais de estatisticas;
- jogos em destaque vindos de `featured_games`;
- link para detalhes de jogos em destaque.

`home_view` busca ate seis jogos do banco e anexa metadados visuais de capa para a variante `home`.

## Sobre

`pages/sobre.html` atualmente funciona como uma pagina demonstrativa da biblioteca/catalogo.

Ela apresenta:

- descricao de uma tela de colecao;
- exemplos de busca, filtro e acao principal;
- cards estaticos de jogos;
- links de navegacao para home e diferenciais.

## Diferenciais

`pages/diferenciais.html` atualmente funciona como uma pagina demonstrativa de detalhes e avaliacoes.

Ela apresenta:

- exemplo de ficha de jogo;
- area de avaliacao pessoal;
- avaliacoes da comunidade;
- interacao visual com coracoes via JavaScript;
- cards explicando status visual, review pessoal e comunidade.

## Papel No Projeto

Essas paginas cumprem dois papeis:

- apresentar o produto para visitantes;
- demonstrar visualmente funcionalidades que tambem aparecem nas telas dinamicas de catalogo, detalhe e biblioteca.

## Observacoes

- Os nomes `sobre` e `diferenciais` sao rotas institucionais, mas o conteudo atual esta mais proximo de demonstracoes de biblioteca e avaliacoes.
- A home ja usa dados reais do model `Game` para jogos em destaque.

## Relacoes Com Outras Areas

- [[Catalogo de Jogos]]
- [[Biblioteca do Usuario]]
- [[Autenticacao]]
- [[Templates]]
- [[Static e CSS]]
