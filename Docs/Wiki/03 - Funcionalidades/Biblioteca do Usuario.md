---
title: Biblioteca do Usuario
aliases:
  - Biblioteca do Usuário
tipo: funcionalidade
status: ativo
area: funcionalidades
projeto: GameVault
arquivo_relacionado:
  - core/models.py
  - core/views.py
  - templates/library/library.html
  - static/css/pages/library.css
tags:
  - gamevault
  - biblioteca
  - usuario
---

# Biblioteca do Usuario

A biblioteca do usuario representa a colecao pessoal de jogos salvos por uma conta autenticada.

## Model Principal

A entidade central e `LibraryEntry`, documentada em [[Models]].

Ela conecta:

- `User`: usuario dono da biblioteca;
- `Game`: jogo salvo;
- `status`: estado atual do jogo;
- `progress`: progresso em porcentagem.

## Rotas

| Caminho | Nome | View | Finalidade |
| --- | --- | --- | --- |
| `/library/` | `core:library` | `library_view` | Lista a biblioteca do usuario. |
| `/add-to-library/` | `core:add_to_library` | `add_to_library_view` | Adiciona ou atualiza jogo na biblioteca. |
| `/update-library-entry/` | `core:update_library_entry` | `update_library_entry_view` | Atualiza status/progresso. |
| `/remove-from-library/` | `core:remove_from_library` | `remove_from_library_view` | Remove jogo da biblioteca. |

## Listagem Da Biblioteca

`library_view` exige login com `@login_required` e busca as entradas do usuario atual:

```python
LibraryEntry.objects.filter(user=request.user).select_related("game")
```

O template `templates/library/library.html` exibe:

- titulo da biblioteca;
- botao para explorar catalogo;
- cards de jogos salvos;
- capa;
- genero;
- titulo;
- status;
- link para editar pelo detalhe;
- botao para remover.

## Status Disponiveis

- `playing`: Jogando.
- `completed`: Concluido.
- `paused`: Pausado.
- `dropped`: Abandonado.
- `plan_to_play`: Planejo Jogar.

## Adicionar Jogo

`add_to_library_view` recebe JSON com:

- `game_id`;
- `status` opcional.

A view usa `get_or_create`. Se a entrada ja existir, atualiza o status em vez de duplicar.

## Remover Jogo

`remove_from_library_view` recebe JSON com `entry_id`, valida se a entrada pertence ao usuario atual e remove o registro.

## Atualizar Status E Progresso

`update_library_entry_view` aceita `entry_id`, `status` e `progress` via JSON.

Estado atual:

- a view existe;
- a tela da biblioteca ainda nao possui uma interface completa de edicao inline;
- o template indica que a atualizacao esta em desenvolvimento.

## Regras Importantes

- Acesso exige usuario autenticado.
- Um usuario so pode ter uma entrada por jogo.
- Todas as operacoes buscam entradas filtrando pelo `request.user`, evitando alterar dados de outro usuario.

## Relacoes Com Outras Areas

- [[Catalogo de Jogos]] e a entrada natural para adicionar jogos.
- [[Autenticacao]] controla o acesso.
- [[Views e URLs]] documenta os endpoints JSON.
- [[Models]] documenta as constraints de `LibraryEntry`.
