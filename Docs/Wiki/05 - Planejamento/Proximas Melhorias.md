---
title: Proximas Melhorias
aliases:
  - Próximas Melhorias
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - melhorias
  - planejamento
---

# Proximas Melhorias

Esta nota registra ideias para evoluir o [[GameVault]] depois da fundacao atual da aplicacao e da wiki.

## Produto

- Criar listas personalizadas na interface, usando `GameList` e `GameListItem`.
- Permitir favoritos ou marcadores rapidos em jogos.
- Criar filtros da biblioteca por status, genero e nota.
- Exibir estatisticas reais do usuario na home ou no perfil.
- Adicionar historico de alteracoes de status dos jogos.

## Experiencia Do Usuario

- Substituir `prompt` por modal de status ao adicionar jogo a biblioteca.
- Substituir `alert` por mensagens visuais no layout.
- Criar formulario de edicao de progresso na biblioteca.
- Melhorar pagina de perfil com resumo da colecao.
- Adicionar estados de carregamento nos endpoints que usam `fetch`.

## Interface E CSS

- Revisar responsividade pagina por pagina.
- Criar padroes para modais, badges e formularios interativos.
- Consolidar estilos repetidos entre catalogo, biblioteca e detalhe.
- Criar uma pagina de guia visual com componentes reutilizaveis.
- Verificar contraste, foco por teclado e acessibilidade basica.

## Tecnico

- Adicionar testes para models e views principais.
- Trocar tratamento generico de excecoes por validacoes mais especificas.
- Padronizar respostas JSON dos endpoints.
- Avaliar paginacao no catalogo quando houver muitos jogos.
- Avaliar variaveis de ambiente para `SECRET_KEY`, `DEBUG` e banco.

## Documentacao

- Manter o [README principal](../../../README.md) alinhado conforme a arquitetura evoluir.
- Criar nota de setup do ambiente local.
- Criar nota de apresentacao do projeto para entrega academica.
- Expandir [[Decisoes Tecnicas]] conforme novas escolhas forem feitas.
- Manter [[Pendencias]] como checklist ativo.

## Obsidian

- Melhorar visualmente [[GameVault.canvas]] depois de abrir no app.
- Criar templates de notas para funcionalidade, decisao e pendencia.
- Adicionar uma base especifica para pendencias futuras.
- Criar uma nota de changelog da wiki.

## Roadmap Sugerido

1. Corrigir documentacao divergente do codigo.
2. Melhorar fluxo de biblioteca.
3. Implementar listas personalizadas.
4. Criar testes basicos.
5. Refinar apresentacao e responsividade.
