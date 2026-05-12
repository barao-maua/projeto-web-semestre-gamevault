---
title: GameVault
aliases:
  - Projeto GameVault
tipo: projeto
status: ativo
area: geral
projeto: GameVault
tags:
  - gamevault
  - django
  - projeto
---

# GameVault

O **GameVault** e uma aplicacao web transacional para gerenciamento de colecoes pessoais de jogos digitais. O sistema permite que usuarios organizem sua biblioteca, acompanhem progresso, registrem avaliacoes e mantenham listas personalizadas.

## Objetivo

Centralizar o controle da colecao de jogos de cada usuario, permitindo registrar informacoes como status, progresso, notas, reviews e listas organizadas por interesse.

## Tipo de Aplicacao

- Aplicacao web com server rendering usando Django.
- Arquitetura MPA, com multiplas paginas renderizadas no servidor.
- Banco de dados relacional para persistencia.
- Operacoes CRUD sobre usuarios, jogos, biblioteca, avaliacoes e listas.

## Areas Principais

- [[Autenticacao]]: cadastro, login, logout e perfil.
- [[Catalogo de Jogos]]: visualizacao dos jogos disponiveis no sistema.
- [[Biblioteca do Usuario]]: relacao entre usuario e jogos salvos.
- [[Funcionalidades]]: visao geral das capacidades planejadas e implementadas.
- [[Static e CSS]]: organizacao visual e arquivos estaticos.

## Documentos Base

- [README principal](../../../README.md): fonte principal de contexto do produto.
- [[Entrega2]]: requisitos da entrega academica inicial.
- [[DOCUMENTACAO_CSS]]: estado atual da organizacao CSS.
- [[PLANO_REORGANIZACAO_CSS]]: historico do plano de reorganizacao visual.
- [[Plano de Wikificacao do GameVault]]: roteiro para transformar o repositorio em wiki.

## Modelo Conceitual

As entidades descritas na documentacao atual incluem:

- `User`: usuario cadastrado na plataforma.
- `Game`: jogo disponivel no sistema.
- `LibraryEntry`: vinculo entre usuario e jogo na biblioteca pessoal.
- `Review`: avaliacao feita por um usuario sobre um jogo.
- `GameList`: lista personalizada criada pelo usuario.
- `GameListItem`: item dentro de uma lista personalizada.

## Fluxo Geral

1. O usuario acessa a aplicacao.
2. O usuario se cadastra ou realiza login.
3. O usuario navega pelo catalogo de jogos.
4. O usuario visualiza detalhes de um jogo.
5. O usuario adiciona jogos a biblioteca pessoal.
6. O usuario registra status, progresso e avaliacoes.

## Arquivos e Pastas Relevantes

- `core/`: app principal da aplicacao Django.
- `config/`: configuracoes do projeto Django.
- `templates/`: templates HTML renderizados pelo Django.
- `static/`: arquivos estaticos, incluindo CSS e imagens.
- `Docs/`: documentacao, imagens e wiki do projeto.

## Links de Navegacao

- [[00 - Mapa do Projeto]]
- [[Arquitetura]]
- [[Funcionalidades]]
- [[Models]]
- [[Views e URLs]]
- [[Templates]]
