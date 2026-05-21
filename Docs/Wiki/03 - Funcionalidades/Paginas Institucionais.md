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
  - core/views.py
tags:
  - gamevault
  - paginas
  - produto
---

# Paginas Institucionais

As paginas institucionais apresentam o conceito do [[GameVault]], destacam o escopo do MVP e ajudam na navegacao inicial do projeto.

## Rotas

| Caminho | Nome | View | Template |
| --- | --- | --- | --- |
| `/` | `core:home` | `home_view` | `pages/home.html` |
| `/sobre/` | `core:sobre` | `sobre_view` | `pages/sobre.html` |

## Home

`pages/home.html` e a primeira pagina da aplicacao.

Ela apresenta:

- proposta do produto;
- chamadas para login e cadastro;
- cards visuais de estatisticas;
- preview conceitual da biblioteca, reviews e status.

`home_view` atualmente renderiza uma landing page estatica, sem carregar jogos dinamicos do banco.

## Sobre

`pages/sobre.html` atualmente funciona como uma pagina demonstrativa da biblioteca/catalogo.

Ela apresenta:

- descricao de uma tela de colecao;
- visao do MVP atual;
- cards explicando catalogo, biblioteca, reviews, login local e Steam.

## Papel No Projeto

Essas paginas cumprem dois papeis:

- apresentar o produto para visitantes;
- contextualizar visualmente funcionalidades que depois aparecem de forma dinamica no catalogo, detalhe e biblioteca.

## Observacoes

- A rota `/diferenciais/` nao existe mais no estado atual do projeto.
- A home atual e uma landing page estatica; os dados reais aparecem nas telas de catalogo, detalhe e biblioteca.

## Relacoes Com Outras Areas

- [[Catalogo de Jogos]]
- [[Biblioteca do Usuario]]
- [[Autenticacao]]
- [[Templates]]
- [[Static e CSS]]
