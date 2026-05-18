---
title: Pendencias
aliases:
  - Pendências
tipo: pendencia
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - pendencias
  - planejamento
---

# Pendencias

Esta nota centraliza tarefas, inconsistencias e pontos que precisam de revisao no [[GameVault]].

## Documentacao

- [x] Atualizar o [README principal](../../../README.md) para alinhar o modelo de dados com o codigo atual.
- [x] Revisar termos antigos como `release_year` e `progress_hours`, pois o codigo usa `release_date` e `progress`.
- [ ] Validar se [[Entrega2]] deve continuar na raiz ou ser arquivado em uma pasta de entregas.
- [ ] Adicionar instrucoes de uso da wiki no README principal do repositorio, se fizer sentido.

## Funcionalidades

- [x] Criar interface visual para atualizar status na [[Biblioteca do Usuario]].
- [ ] Avaliar se `GameList` e `GameListItem` terao telas proprias.
- [x] Melhorar o fluxo de adicionar jogo a biblioteca sem usar `prompt`.
- [ ] Verificar se visitantes devem conseguir acessar detalhes completos de jogos ou apenas uma previa.
- [x] Revisar mensagens de erro retornadas pelos endpoints JSON.
- [x] Implementar verificacao de email e redefinicao de senha por email.
- [x] Permitir login por usuario ou email.

## Interface

- [ ] Validar responsividade das principais telas em mobile.
- [ ] Revisar acessibilidade dos botoes e formularios.
- [x] Trocar a maior parte das interacoes com `alert` e `prompt` por componentes visuais.
- [ ] Garantir consistencia entre paginas demonstrativas e telas dinamicas reais.
- [ ] Decidir se a proxima iteracao inclui foto de perfil real no lugar do avatar por inicial.

## Tecnico

- [x] Confirmar se arquivos `__pycache__` e banco local devem ficar fora do versionamento.
- [x] Revisar `.gitignore` para ambiente Python/Django.
- [ ] Rodar `python manage.py check` no ambiente local antes da proxima entrega.
- [x] Verificar se as views JSON principais usam `@require_POST` nos endpoints de alteracao.
- [ ] Avaliar tratamento de excecoes genericas em `core/views.py`.

## Obsidian/Wiki

- [ ] Abrir [[GameVault.canvas]] no Obsidian e ajustar layout se necessario.
- [ ] Abrir [[Projeto GameVault.base]] no Obsidian e validar se as views renderizam como esperado.
- [ ] Decidir se os documentos de entrega devem ganhar uma pasta propria dentro de `Docs/Wiki/`.
- [ ] Criar padrao de propriedades para futuras notas.

## Prioridades Sugeridas

1. Validar responsividade e apresentacao.
2. Revisar excecoes e robustez do backend.
3. Definir futuro de `GameList` e `GameListItem`.
4. Revisar paginas demonstrativas publicas.
5. Validar base e canvas no Obsidian.
