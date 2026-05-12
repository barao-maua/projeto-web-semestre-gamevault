---
title: Decisoes Tecnicas
aliases:
  - Decisões Técnicas
tipo: decisao
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - decisoes
  - planejamento
---

# Decisoes Tecnicas

Esta nota registra decisoes importantes tomadas no [[GameVault]], com foco no motivo de cada escolha e nos impactos para manutencao do projeto.

## Decisoes Atuais

### Django com MPA e server rendering

Status: adotada.

Motivo:

- Atende aos requisitos academicos do projeto.
- Mantem a arquitetura simples e explicavel.
- Evita dependencias front-end desnecessarias.

Impacto:

- As telas ficam em `templates/`.
- As rotas e regras de negocio ficam concentradas em `core/views.py`.
- A navegacao usa paginas renderizadas no servidor.

Notas relacionadas:

- [[Arquitetura]]
- [[Views e URLs]]
- [[Templates]]

### Uso do User padrao do Django

Status: adotada.

Motivo:

- Reduz complexidade.
- Permite usar `UserCreationForm`, `AuthenticationForm`, `login`, `logout` e `@login_required`.
- E suficiente para cadastro, login e perfil atuais.

Impacto:

- `LibraryEntry`, `Review` e `GameList` se relacionam com `django.contrib.auth.models.User`.
- Caso o projeto precise de campos extras de perfil, isso deve ser planejado antes de alterar o model de usuario.

Notas relacionadas:

- [[Autenticacao]]
- [[Models]]

### SQLite como banco local

Status: adotada para desenvolvimento.

Motivo:

- Simples para ambiente academico/local.
- Nao exige servico externo.
- Facilita demonstracao do projeto.

Impacto:

- O banco fica em `db.sqlite3`.
- Para producao, seria necessario avaliar outro banco e configuracoes de ambiente.

Notas relacionadas:

- [[Arquitetura]]
- [[Models]]

### CSS modular por responsabilidade

Status: adotada.

Motivo:

- Evita um unico arquivo CSS grande.
- Facilita manutencao visual.
- Diminui risco de uma alteracao afetar paginas sem relacao.

Impacto:

- Estilos globais ficam em `base.css`.
- Componentes compartilhados ficam em `components.css`.
- Ajustes responsivos ficam em `responsive.css`.
- Estilos especificos ficam em `static/css/pages/`.

Notas relacionadas:

- [[Static e CSS]]
- [[DOCUMENTACAO_CSS]]
- [[PLANO_REORGANIZACAO_CSS]]

### Wiki do projeto dentro do proprio vault

Status: adotada.

Motivo:

- O repositorio ja funciona como vault Obsidian.
- Permite documentar codigo, produto e planejamento no mesmo lugar.
- Facilita navegacao com wikilinks, canvas e base.

Impacto:

- A documentacao navegavel fica em `Docs/Wiki/`.
- O codigo permanece nas pastas tecnicas originais.
- O Obsidian pode abrir tanto a wiki quanto os arquivos de codigo.

Notas relacionadas:

- [[00 - Mapa do Projeto]]
- [[Projeto GameVault.base]]
- [[GameVault.canvas]]

## Decisoes A Avaliar

- [ ] Definir se listas personalizadas terao interface nesta entrega.
- [ ] Definir se o README deve ser atualizado para refletir os campos atuais dos models.
- [ ] Definir se endpoints JSON devem virar views com formularios tradicionais ou permanecer com `fetch`.
- [ ] Definir se imagens de capa devem depender de URLs externas ou arquivos locais padronizados.

## Como Registrar Novas Decisoes

Use este formato:

```md
### Titulo da decisao

Status: proposta | adotada | descartada.

Motivo:

- Razao principal.

Impacto:

- Consequencia para codigo, produto ou documentacao.
```
