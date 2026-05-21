# Apresentacao Final - GameVault

## 1. Abertura

- Projeto: `GameVault`
- Tipo: aplicacao web fullstack com `Django` e renderizacao no servidor.
- Objetivo: permitir que cada usuario organize sua biblioteca pessoal de jogos, acompanhe status e registre reviews.

Fala sugerida:

"O GameVault e uma aplicacao web fullstack em Django criada para centralizar a biblioteca pessoal de jogos do usuario. O sistema permite descobrir jogos, salvar na biblioteca, atualizar status e registrar avaliacoes ao longo do tempo."

## 2. Alternativa Escolhida No PDF

- Alternativa A: `Fullstack Django`.
- O projeto atende os eixos pedidos no PDF:
  - ORM e Admin
  - CRUD de recurso real do dominio
  - Autenticacao
  - Apresentacao tecnica do que foi construido

## 3. Parte De Cada Integrante

Sugestao para dividir a fala:

- Integrante 1: visao geral, objetivo e telas principais.
- Integrante 2: camada ORM e Admin.
- Integrante 3: CRUD da biblioteca e reviews.
- Integrante 4: autenticacao, email, avatar e integracao Steam.

Se o grupo tiver outra divisao, troquem apenas os nomes mantendo a mesma ordem logica.

## 4. Problema Que O Projeto Resolve

- Centraliza a colecao pessoal de jogos.
- Evita controle disperso em anotacoes ou planilhas.
- Permite acompanhar backlog, jogos em andamento e concluidos.
- Guarda a opiniao do usuario sobre cada jogo.

## 5. Stack E Arquitetura

- Backend e frontend no mesmo projeto com `Django SSR`.
- Banco relacional com `SQLite` no ambiente atual.
- Templates HTML em `templates/`.
- CSS modular em `static/css/`.
- Admin nativo do Django para operacoes internas.

Fala sugerida:

"Escolhemos manter o projeto como MPA com renderizacao no servidor porque isso simplificou a integracao entre regras de negocio, autenticacao e interface, alem de atender bem ao escopo da entrega final."

## 6. Camada ORM - Principais Models

### `Game`

- representa um jogo do catalogo;
- guarda titulo, descricao, genero, capa, `steam_app_id`, `steam_type` e `last_synced_at`.

### `LibraryEntry`

- relaciona `User` e `Game`;
- guarda `status` e `progress`;
- impede duplicidade de um mesmo jogo na biblioteca do mesmo usuario.

### `Review`

- relaciona `User` e `Game`;
- guarda `rating` e `comment`;
- preserva historico de reviews em vez de sobrescrever.

### `UserEmailVerification`

- controla se o email atual do usuario ja foi verificado.

### `SteamAccountLink`

- vincula a conta local do GameVault a uma conta Steam.

### `UserProfile`

- guarda o avatar local de perfil.

### Models planejados para evolucao futura

- `GameList`
- `GameListItem`

## 7. Admin E Persistencia

- O admin esta configurado para jogos, biblioteca, reviews, verificacao de email, conta Steam e perfil.
- `GameAdmin` possui acao para sincronizar jogos com a Steam.
- As constraints evitam duplicacoes indevidas.

Fala sugerida:

"O admin foi importante para validar a modelagem e facilitar manutencao dos dados, especialmente nos testes de sincronizacao e nas operacoes de catalogo."

## 8. CRUD Para Destacar Na Apresentacao

Recurso principal recomendado: `LibraryEntry`.

### Create

- adicionar um jogo a biblioteca pelo detalhe do jogo.

### Read

- listar os jogos salvos na pagina `Minha Biblioteca`.

### Update

- editar o status de um jogo salvo.

### Delete

- remover um jogo da biblioteca.

Complemento recomendado: `Review`.

- criar nova avaliacao para o jogo;
- exibir a review mais recente na interface;
- preservar historico no banco.

## 9. Autenticacao

- cadastro com email obrigatorio e unico;
- login com `username` ou `email`;
- logout via `POST`;
- verificacao de email;
- reset de senha por email;
- perfil do usuario;
- login com Steam via OpenID.

## 10. O Que Nao Vimos Em Aula E Foi Implementado

- autenticacao com Steam via OpenID;
- integracao com API externa da Steam;
- sincronizacao de catalogo com fallback local;
- sincronizacao da biblioteca possuida na Steam;
- upload e validacao de avatar;
- envio de email com token assinado para verificacao.

## 11. Maiores Dificuldades Encontradas

- integrar dados locais com dados externos da Steam sem quebrar a navegacao;
- manter fallback quando a Steam falha;
- ajustar UX de biblioteca, detalhe e reviews para ficarem coerentes;
- alinhar a documentacao com a evolucao real do codigo.

## 12. Diferenciais Do Projeto

- login local e tambem login com Steam;
- biblioteca pessoal com status;
- reviews com historico;
- catalogo com descoberta via Steam e persistencia local;
- perfil com avatar local ou avatar da Steam.

## 13. Roteiro De Slides

### Slide 1

- nome do projeto;
- problema que resolve;
- objetivo.

### Slide 2

- stack e arquitetura.

### Slide 3

- principais models do ORM.

### Slide 4

- admin e persistencia.

### Slide 5

- CRUD da biblioteca.

### Slide 6

- reviews e historico.

### Slide 7

- autenticacao local, email e Steam.

### Slide 8

- dificuldades e pontos fora do conteudo de aula.

### Slide 9

- conclusao e proximos passos.

## 14. Encerramento

Fala sugerida:

"Como resultado, o GameVault entrega um fluxo completo de autenticacao, catalogo, biblioteca e avaliacao dentro do modelo fullstack Django pedido na alternativa A. Alem disso, conseguimos implementar recursos extras como integracao Steam, avatar e verificacao de email, que ampliaram a complexidade tecnica do projeto."

## 15. Proximos Passos

- finalizar interface de listas personalizadas;
- expor progresso de jogo com mais destaque na UI;
- ampliar testes automatizados;
- refinar ainda mais a documentacao e a apresentacao final do grupo.
