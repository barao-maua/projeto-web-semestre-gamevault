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
- `progress`: campo tecnico de progresso, mantido no model, mas sem exibicao na interface atual.

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

A view tambem busca as avaliacoes do proprio usuario para os jogos presentes na biblioteca e anexa cada review ao respectivo card. Isso evita consultas repetidas por item no template.

O template `templates/library/library.html` exibe:

- titulo da biblioteca;
- botao para explorar catalogo;
- cards de jogos salvos;
- capa;
- genero;
- titulo;
- avaliacao pessoal com coracoes dinamicos;
- status;
- botao para editar status em modal;
- link para abrir detalhes;
- botao para remover.

Tambem foram adicionados refinamentos de UX:

- layout de acoes mais limpo, sem separadores textuais;
- feedback visual mais consistente com o restante do projeto;
- integracao visual entre biblioteca, detalhe do jogo e avaliacao pessoal.

## Status Disponiveis

- `playing`: Jogando.
- `completed`: Concluido.
- `paused`: Pausado.
- `dropped`: Abandonado.
- `plan_to_play`: Planejo Jogar.

## Avaliacao No Card

Os coracoes exibidos no card da biblioteca representam a avaliacao do usuario logado para aquele jogo.

- Coracao preenchido usa a cor de destaque verde (`var(--accent)`).
- Coracao vazio usa uma cor neutra.
- Se o usuario ainda nao avaliou o jogo, todos os coracoes aparecem vazios.
- A avaliacao exibida e pessoal, nao uma media global da comunidade.

## Adicionar Jogo

`add_to_library_view` recebe JSON com:

- `game_id`;
- `status` opcional.

A view usa `get_or_create`. Se a entrada ja existir, atualiza o status em vez de duplicar.

Depois da adicao no detalhe do jogo, a interface pode sugerir uma avaliacao quando o status escolhido indicar que o usuario ja tem experiencia com o jogo (`playing`, `completed`, `paused` ou `dropped`). Para `plan_to_play`, a avaliacao nao e incentivada imediatamente.

## Remover Jogo

`remove_from_library_view` recebe JSON com `entry_id`, valida se a entrada pertence ao usuario atual e remove o registro.

Na interface atual, a acao de sair da conta ganhou modal de confirmacao visual, mas a remocao do item da biblioteca ainda usa confirmacao simples do navegador e pode ser refinada em iteracoes futuras.

## Atualizar Status

`update_library_entry_view` aceita `entry_id`, `status` e, tecnicamente, `progress` via JSON. Na interface atual da biblioteca, apenas o status e editado.

Fluxo atual:

- o usuario clica em `Editar` no card da biblioteca;
- um modal abre com o status atual;
- o status e selecionado por cards visuais;
- o formulario envia `entry_id` e `status` para `update_library_entry_view`;
- a view valida se a entrada pertence ao usuario logado;
- a view valida se o status e permitido;
- ao salvar com sucesso, a pagina recarrega para exibir os dados atualizados.

Exemplo de payload:

```json
{
  "entry_id": 12,
  "status": "playing"
}
```

## Regras Importantes

- Acesso exige usuario autenticado.
- Um usuario so pode ter uma entrada por jogo.
- Todas as operacoes buscam entradas filtrando pelo `request.user`, evitando alterar dados de outro usuario.
- `status` precisa ser um dos valores definidos em `LibraryEntry.STATUS_CHOICES`.
- Caso o backend receba `progress`, ele precisa ser inteiro entre 0 e 100.

## Relacoes Com Outras Areas

- [[Catalogo de Jogos]] e a entrada natural para adicionar jogos.
- [[Autenticacao]] controla o acesso.
- [[Views e URLs]] documenta os endpoints JSON.
- [[Models]] documenta as constraints de `LibraryEntry`.

## O Que Mudou Recentemente

- A biblioteca passou a mostrar coracoes dinamicos com base na avaliacao do proprio usuario.
- O progresso deixou de ser enfatizado na interface da entrega.
- A edicao principal foi simplificada para status, mantendo o campo de progresso apenas no model.
- O visual dos botoes foi refinado para melhorar leitura e apresentacao.
