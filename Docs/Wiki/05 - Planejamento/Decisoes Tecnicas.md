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
- O email e salvo no campo nativo `User.email`.
- O estado de verificacao do email fica separado em `UserEmailVerification`, evitando trocar o model de usuario.
- Caso o projeto precise de campos extras alem do email, isso deve ser planejado antes de alterar o model de usuario.

Notas relacionadas:

- [[Autenticacao]]
- [[Models]]

### Verificacao De Email Sem Bloquear Login

Status: adotada.

Motivo:

- Mantem o cadastro simples para a entrega.
- Evita bloquear usuario caso o SMTP falhe ou o email demore.
- Ainda permite confirmar propriedade do email pelo perfil.

Impacto:

- Email e obrigatorio e unico no cadastro.
- Usuario pode usar o sistema mesmo com email pendente.
- Perfil mostra status de verificacao.
- Trocar email invalida a verificacao anterior.
- Recuperacao de senha usa email via views nativas do Django.

Notas relacionadas:

- [[Autenticacao]]
- [[Spec - Email Verificacao e Reset de Senha]]

### Login Por Username Ou Email

Status: adotada.

Motivo:

- Reduz atrito de acesso para o usuario.
- Aproveita o email unico ja exigido no cadastro.
- Mantem compatibilidade com o login tradicional por username.

Impacto:

- O formulario de login aceita usuario ou email no mesmo campo.
- A autenticacao continua usando o backend padrao do Django, resolvendo email para username antes do login.
- O destino padrao apos login passou a ser a biblioteca, salvo quando existe `next`.

Notas relacionadas:

- [[Autenticacao]]
- [[Views e URLs]]

### Politica De Senha Reforcada

Status: adotada.

Motivo:

- Aumenta previsibilidade e seguranca minima para cadastro e redefinicao de senha.
- Evita depender apenas dos help texts padrao do Django na interface.

Impacto:

- Cadastro e redefinicao de senha exigem no minimo 8 caracteres.
- A senha precisa conter letra maiuscula, letra minuscula, numero e caractere especial.
- A interface mostra checklist visual em tempo real, mas o backend continua sendo a fonte de verdade.

Notas relacionadas:

- [[Autenticacao]]
- [[Spec - Email Verificacao e Reset de Senha]]

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

## Decisoes Fechadas Recentemente

### Listas Personalizadas Fora Do Escopo Da Entrega Atual

Status: adotada.

Motivo:

- O recurso principal da entrega continua sendo `LibraryEntry`.
- `GameList` e `GameListItem` ja demonstram modelagem e admin, sem exigir telas completas agora.
- Abrir interface de listas nesta fase aumentaria escopo e risco sem fortalecer a demonstracao principal.

Impacto:

- `GameList` e `GameListItem` permanecem como modelagem pronta para evolucao futura.
- O foco de interface fica em autenticacao, catalogo, biblioteca e avaliacoes.

Notas relacionadas:

- [[Entrega Final - Alternativa A]]
- [[Backlog Pos-Entrega]]

### README Como Fonte Externa Alinhada Ao Codigo Atual

Status: adotada.

Motivo:

- O README continua sendo um ponto de entrada rapido fora do vault.
- Divergencias entre README e codigo enfraquecem a apresentacao e a manutencao.

Impacto:

- O README deve refletir autenticacao por email, verificacao, reset de senha, status da biblioteca e models atuais.
- Sempre que um fluxo principal mudar, o README precisa ser revisado junto com a wiki.

Notas relacionadas:

- [[GameVault]]
- [[Autenticacao]]

### Endpoints JSON Mantidos Com Fetch Na Interface Atual

Status: adotada.

Motivo:

- Os fluxos principais ja foram refinados em cima de modais e feedback visual com JavaScript.
- Reescrever tudo para formularios tradicionais agora seria retrabalho.
- O padrao atual atende bem a experiencia da biblioteca e das avaliacoes.

Impacto:

- Adicao, edicao e remocao na biblioteca continuam usando `fetch`.
- Avaliacao de jogos continua usando `fetch`.
- Melhorias futuras devem priorizar mensagens, validacoes e UX, nao trocar o paradigma sem necessidade.

Notas relacionadas:

- [[Views e URLs]]
- [[Biblioteca do Usuario]]
- [[Catalogo de Jogos]]

### Catalogo Futuro Baseado Em Dados Da Steam

Status: adotada como direcao de evolucao.

Motivo:

- O projeto tem problemas visuais com imagens de alguns jogos.
- Cadastrar manualmente todos os jogos no banco nao escala bem.
- A integracao com a Steam e vista como parte central da proposta futura do GameVault.

Impacto:

- No curto prazo, o catalogo atual continua usando `Game` e dados locais ja existentes.
- No planejamento futuro, a fonte de jogos e capas deve evoluir para integracao com dados da Steam.
- Essa integracao precisara considerar importacao, sincronizacao, fallback local e tratamento visual das imagens.

Notas relacionadas:

- [[Catalogo de Jogos]]
- [[Backlog Pos-Entrega]]

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
