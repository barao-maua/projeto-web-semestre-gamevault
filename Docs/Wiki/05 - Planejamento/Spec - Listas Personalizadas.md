---
title: Spec - Listas Personalizadas
aliases:
  - Spec Listas Personalizadas
  - Listas Personalizadas
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - listas
  - gamelist
  - backlog
---

# Spec - Listas Personalizadas

Esta nota define o plano para evoluir a interface de `GameList` e `GameListItem` no [[GameVault]].

## Objetivo

Permitir que o usuario:

- crie listas personalizadas;
- edite listas existentes;
- remova listas;
- adicione jogos a listas;
- remova jogos de listas;
- visualize suas listas de forma organizada e clara.

## Escopo

Dentro do escopo:

- tela de listagem das listas do usuario;
- criacao de lista;
- edicao de nome, descricao e visibilidade;
- detalhe de lista;
- adicionar jogo a lista;
- remover jogo da lista;
- remover a lista.

Fora do escopo:

- compartilhamento publico avancado;
- curtidas ou comentarios em listas;
- ordenacao drag-and-drop;
- ranking ou colaboracao entre usuarios;
- pagina publica completa de exploracao de listas.

## Decisao Tecnica

Manter SSR com Django, usando templates, formularios simples e rotas tradicionais.

Motivo:

- o projeto ja segue esse padrao;
- reduz escopo tecnico;
- facilita demonstracao academica e manutencao;
- evita adicionar mais uma camada JS complexa sem necessidade.

## Modelos Envolvidos

- `GameList`
- `GameListItem`
- `Game`
- `User`

## Regras De Negocio

- somente o dono pode criar, editar e remover as proprias listas;
- somente o dono pode adicionar ou remover jogos dessas listas;
- um mesmo jogo nao pode aparecer duas vezes na mesma lista;
- o nome da lista deve ser unico por usuario;
- `is_public` pode ficar ativo no model mesmo sem fluxo publico completo nesta primeira versao.

## Rotas Sugeridas

- `/lists/`
- `/lists/create/`
- `/lists/<id>/`
- `/lists/<id>/edit/`
- `/lists/<id>/delete/`
- `/lists/<id>/add-game/`
- `/lists/item/<id>/delete/`

## Fluxos Do Usuario

### Fluxo 1 - Criar Lista

1. Usuario abre `Minhas Listas`.
2. Clica em `Criar lista`.
3. Informa nome, descricao e visibilidade.
4. Salva.
5. Volta para a listagem ou vai direto para o detalhe da lista.

### Fluxo 2 - Editar Lista

1. Usuario abre uma lista existente.
2. Clica em `Editar`.
3. Ajusta nome, descricao ou visibilidade.
4. Salva as alteracoes.

### Fluxo 3 - Adicionar Jogo A Lista

1. Usuario abre o detalhe da lista.
2. Clica em `Adicionar jogo`.
3. Seleciona um jogo disponivel.
4. Confirma a adicao.
5. O jogo aparece na lista.

### Fluxo 4 - Remover Jogo Da Lista

1. Usuario abre a lista.
2. Clica em `Remover` no item.
3. Confirma a acao.
4. O jogo sai da lista.

### Fluxo 5 - Apagar Lista

1. Usuario abre a lista ou a listagem.
2. Clica em `Apagar lista`.
3. Confirma a acao.
4. A lista e removida do sistema.

## Como Faremos

### Etapa 1 - Listagem De Listas

Criar pagina `Minhas Listas` com:

- nome da lista;
- descricao curta;
- quantidade de jogos;
- indicador de lista publica ou privada;
- acoes de abrir, editar e remover.

### Etapa 2 - Criacao E Edicao

Criar formulario para `GameList` com:

- `name`;
- `description`;
- `is_public`.

Regras:

- nome unico por usuario;
- somente o dono pode editar;
- descricao pode continuar opcional.

### Etapa 3 - Detalhe Da Lista

Criar tela da lista com:

- nome;
- descricao;
- status publico ou privado;
- grid ou tabela de jogos da lista;
- acoes para remover item;
- botao para adicionar jogo.

### Etapa 4 - Adicionar Jogo A Lista

Criar fluxo simples para adicionar jogo:

- por formulario tradicional ou modal leve;
- buscando entre jogos do catalogo;
- impedindo duplicacao do mesmo jogo na mesma lista.

## Estrategia De UX

### Listagem

A tela `Minhas Listas` deve ser simples e legivel.

Cada card ou bloco de lista deve mostrar:

- nome;
- descricao resumida;
- quantidade de jogos;
- status publico ou privado;
- botoes de abrir, editar e remover.

### Detalhe Da Lista

O detalhe da lista deve funcionar como uma versao especializada da biblioteca:

- jogos renderizados em cards ou tabela compacta;
- foco em nome, capa e acoes;
- sem poluir a tela com informacoes desnecessarias.

### Confirmacoes

Recomendado:

- confirmacao visual para apagar lista;
- confirmacao visual ou simples para remover item.

## Arquivos Impactados

- `core/views.py`
- `core/urls.py`
- `core/forms.py`
- `templates/lists/`
- `static/css/pages/lists.css`
- documentacao tecnica e funcional relacionada.

## Formularios Sugeridos

### `GameListForm`

Campos:

- `name`
- `description`
- `is_public`

Validacoes:

- nome unico por usuario;
- nome obrigatorio;
- descricao opcional.

### `GameListItemForm`

Campos:

- `game`

Validacoes:

- nao permitir adicionar o mesmo jogo duas vezes;
- limitar a selecao a jogos validos do catalogo.

## Views Sugeridas

- `list_user_lists_view`
- `create_game_list_view`
- `game_list_detail_view`
- `edit_game_list_view`
- `delete_game_list_view`
- `add_game_to_list_view`
- `remove_game_list_item_view`

## Protecao E Permissao

Todas as views devem:

- exigir login;
- filtrar listas por `request.user`;
- impedir acesso a listas de outro usuario por ID direto;
- usar `get_object_or_404(..., user=request.user)` sempre que aplicavel.

## Riscos

- repetir a logica de biblioteca e criar UX redundante;
- abrir escopo demais tentando fazer listas publicas muito cedo;
- criar formularios pouco claros para adicionar jogo;
- esquecer de tratar duplicidade do mesmo jogo na lista.

## Mitigacoes

- comecar com listas privadas e simples;
- reaproveitar o visual de cards ja existente onde fizer sentido;
- manter `is_public` preparado, mas sem depender dele para o primeiro fluxo;
- validar duplicidade no backend.

## Ordem Recomendada De Implementacao

1. Criar listagem de listas do usuario.
2. Criar formulario de `GameList`.
3. Criar tela de detalhe da lista.
4. Criar fluxo para adicionar jogo a lista.
5. Criar remocao de item da lista.
6. Criar remocao da propria lista.
7. Atualizar documentacao relacionada.

## Checklist De Implementacao

- [ ] Criar listagem de listas do usuario.
- [ ] Criar formulario de `GameList`.
- [ ] Criar tela de detalhe da lista.
- [ ] Criar fluxo para adicionar jogo a lista.
- [ ] Criar remocao de item da lista.
- [ ] Criar remocao da propria lista.
- [ ] Proteger tudo com `request.user`.
- [ ] Atualizar documentacao relacionada.

## Critério De Pronto

- CRUD basico de listas funcionando.
- Adicionar e remover jogos da lista funcionando.
- Fluxo protegido por usuario autenticado.
- Duplicidade de jogo na mesma lista impedida.
- Nome de lista unico por usuario respeitado.

## Plano De Teste Manual

1. Criar lista nova.
2. Criar segunda lista.
3. Tentar criar lista com nome duplicado.
4. Editar nome e descricao da lista.
5. Abrir detalhe da lista.
6. Adicionar jogo valido.
7. Tentar adicionar o mesmo jogo novamente.
8. Remover jogo da lista.
9. Apagar lista.
10. Tentar acessar lista de outro usuario por URL direta.

## Evolucoes Futuras

- exploracao publica de listas;
- compartilhamento por link;
- listas tematicas com capa customizada;
- ordenacao de itens manual;
- integracao entre listas e catalogo em massa.

## Notas Relacionadas

- [[Models]]
- [[Views e URLs]]
- [[Biblioteca do Usuario]]
- [[Backlog Pos-Entrega]]
