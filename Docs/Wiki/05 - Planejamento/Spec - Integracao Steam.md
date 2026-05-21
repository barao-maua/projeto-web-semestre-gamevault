---
title: Spec - Integracao Steam
aliases:
  - Spec Integracao Steam
  - Integracao Steam
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - steam
  - catalogo
  - backlog
---

# Spec - Integracao Steam

Esta nota define o plano para evoluir o catalogo do [[GameVault]] usando dados vindos da Steam.

## Objetivo

Transformar a Steam na principal fonte de dados do catalogo do GameVault, reduzindo cadastro manual e melhorando consistencia visual das capas e metadados dos jogos.

## Objetivos Funcionais

O sistema deve conseguir:

- buscar jogos da Steam;
- importar jogos para o banco local;
- atualizar jogos ja importados;
- usar capas e dados vindos da Steam no catalogo;
- manter o catalogo funcional mesmo sem chamada online no momento da navegacao.

## Principio Central

A interface do GameVault nao deve depender de chamada ao vivo para a Steam em cada page load.

A Steam entra como:

- fonte de importacao;
- fonte de atualizacao;
- fonte de midia e metadados.

O banco local continua sendo a fonte imediata da aplicacao.

## Motivacao

- evitar cadastrar manualmente todos os jogos;
- corrigir inconsistencias visuais das capas;
- escalar o catalogo;
- facilitar expansao futura.

## Escopo

Dentro do escopo:

- adicionar identificador externo em `Game`;
- importar dados de jogo da Steam;
- atualizar dados ja existentes;
- persistir dados localmente;
- criar fluxo administrativo ou tecnico para sincronizacao.

Fora do escopo:

- login com conta Steam;
- sincronizar biblioteca real do usuario na Steam;
- compras, wishlist, achievements;
- busca fulltext remota em tempo real no frontend;
- dependencia obrigatoria de internet para abrir catalogo.

## Decisao De Arquitetura

Manter `Game` como entidade central local.

A Steam sera tratada como:

- fonte de importacao;
- fonte de atualizacao;
- fonte de midia e metadados.

## Por Que Essa Arquitetura

- preserva todo o resto do sistema (`LibraryEntry`, `Review`, etc.);
- evita acoplar a experiencia a uma API externa;
- facilita fallback quando a Steam falhar;
- permite cache e persistencia local.

## Modelagem Sugerida

Hoje `Game` ja guarda:

- `title`;
- `description`;
- `release_date`;
- `genre`;
- `cover_image`.

Sugestao de evolucao:

- `steam_app_id`;
- opcionalmente `data_source`;
- opcionalmente `external_cover_image`;
- opcionalmente `last_synced_at`.

## Recomendacao De MVP

- adicionar apenas `steam_app_id`;
- reutilizar `cover_image` para a URL ou import da capa;
- se precisar evoluir depois, separar origem local e externa.

## Regras De Dados

- `steam_app_id` deve ser unico quando preenchido;
- um jogo local pode existir sem `steam_app_id` no inicio;
- se o jogo for sincronizado pela Steam, a aplicacao deve conseguir:
  - criar novo `Game`;
  - ou atualizar um existente.

## Decisao De Origem

Recomendacao:

- `steam_app_id` e a chave de integracao;
- `title` nao deve ser usado como chave principal de sync;
- titulo pode mudar, ter diferencas de capitalizacao ou localidade.

## Campos Que Queremos Puxar Da Steam

Minimo viavel:

- nome;
- descricao;
- imagem/capa;
- data de lancamento;
- genero ou categoria quando disponivel.

Campos futuros possiveis:

- screenshots;
- publisher;
- developer;
- tags;
- trailers.

Preco nao e necessario para o escopo atual.

## Fluxos Principais

### Fluxo 1 - Importar Jogo Por App ID

1. Admin ou integrador informa `steam_app_id`.
2. Sistema consulta a fonte Steam.
3. Sistema transforma dados no formato do model `Game`.
4. Sistema cria ou atualiza jogo local.
5. Jogo passa a aparecer normalmente no catalogo.

### Fluxo 2 - Sincronizar Jogo Existente

1. Jogo ja existe com `steam_app_id`.
2. Admin ou comando executa sync.
3. Sistema atualiza campos importaveis.
4. Mantem integridade dos relacionamentos locais.

### Fluxo 3 - Catalogo Em Uso Normal

1. Usuario abre `/catalog/`.
2. Sistema le do banco local.
3. Nenhuma dependencia online imediata da Steam.
4. Se houver imagens sincronizadas, elas ja aparecem normalmente.

## Origem Tecnica Dos Dados

Esta nota mantem a camada de origem desacoplada.

Possibilidades futuras:

- endpoint viavel da Steam;
- endpoint publico da loja;
- adaptador interno para normalizar a origem.

Recomendacao:

- esconder a fonte exata atras de um servico interno.

Assim, no futuro da para trocar a fonte sem quebrar views ou models.

## Camada Recomendada

Criar um servico interno, por exemplo:

- `core/services/steam.py`

Responsabilidades:

- buscar dados remotos;
- normalizar resposta;
- converter para formato do projeto;
- lancar erro claro se a integracao falhar.

## Funcoes Sugeridas

- `fetch_steam_game(app_id)`;
- `normalize_steam_game(payload)`;
- `sync_game_from_steam(app_id)`;
- `sync_existing_game(game)`.

## Admin E Operacoes

MVP recomendado:

1. comando Django para importar ou sincronizar;
2. acao no admin para sincronizar um jogo;
3. depois, se quiser, UI administrativa dedicada.

## Comando Sugerido

- `python manage.py sync_steam_game <app_id>`
- `python manage.py sync_steam_catalog ...` no futuro

## Admin Sugerido

No `GameAdmin`:

- acao `Sincronizar com Steam`;
- campo visivel `steam_app_id`;
- possivelmente `last_synced_at`.

## Fallbacks

Se a Steam falhar:

- o catalogo continua funcionando com os dados locais;
- o sync deve retornar erro controlado;
- nao deve quebrar paginas publicas.

Se a imagem externa falhar:

- mostrar placeholder ou imagem local ja existente.

Se algum campo vier vazio:

- manter valor local quando fizer sentido;
- ou preencher com default neutro.

## Estrategia De Atualizacao

Decisao recomendada:

- sync manual ou admin no MVP;
- sem auto-sync em todo acesso;
- sem cron obrigatorio nesta fase.

Depois:

- auto-sync agendado;
- refresh seletivo por `last_synced_at`.

## Conflito Entre Dado Local E Dado Steam

Politica recomendada para MVP:

- Steam domina os campos importaveis:
  - titulo;
  - descricao;
  - capa;
  - release_date;
  - genero.
- dados de interacao local nunca sao tocados:
  - `LibraryEntry`;
  - `Review`;
  - listas.

Se no futuro quiser customizacao manual local, isso deve virar regra separada.

## UX Futura Relacionada

Nao e necessario agora, mas deve ficar previsto:

- botao `Importar da Steam` no admin;
- exibicao mais consistente de capas no catalogo;
- selo discreto opcional de `dados sincronizados`;
- filtro futuro para jogos importados da Steam.

## Riscos

- indisponibilidade da fonte externa;
- mudancas de schema;
- imagens quebradas;
- dados inconsistentes entre jogos;
- importacao parcial;
- rate limit ou bloqueio.

## Mitigacoes

- usar servico interno isolado;
- persistir localmente;
- fallback visual;
- logs claros de falha;
- sync manual primeiro;
- nao atrelar renderizacao da UI a consulta externa.

## Impacto Em Arquivos

Provaveis:

- `core/models.py`
- migration nova
- `core/admin.py`
- `core/views.py` talvez pouco ou nada no MVP
- `core/services/steam.py`
- `management/commands/`
- docs de catalogo, models, views e decisoes tecnicas

## Fase 1 Recomendada

- `steam_app_id`;
- servico interno;
- comando Django;
- sync basico;
- admin.

Status atual da Fase 1:

- implementacao local concluida;
- `steam_app_id`, `steam_type`, `last_synced_at`, servico interno, sync individual, sync em lote e suporte no admin ja estao ativos;
- o catalogo da interface ja tenta usar a Steam como fonte de descoberta e faz fallback para o banco local quando necessario.

## Fase 2 Recomendada

- acao no admin;
- melhoria visual de origem dos dados;
- sync em lote;
- politica de atualizacao mais refinada.

Status atual da Fase 2:

- fonte real ativa para detalhes por `app_id`;
- importacao em lote ativa via busca publica da Steam Store;
- selo visual de origem Steam ativo no catalogo e no detalhe do jogo;
- fallback visual de imagem validado com placeholder local na UI principal.

## Checklist Refinado

- [x] Definir campo `steam_app_id` em `Game`.
- [x] Criar migration.
- [x] Definir servico interno de integracao.
- [x] Implementar busca por `app_id`.
- [x] Normalizar payload remoto.
- [x] Criar sync create/update para `Game`.
- [x] Definir politica de atualizacao dos campos.
- [x] Criar comando Django para sync.
- [x] Adicionar suporte no admin.
- [x] Testar importacao de alguns jogos reais.
- [x] Validar fallback de imagem.
- [x] Atualizar documentacao tecnica e funcional.

Observacao:

- A Fase 1 com mock foi substituida por integracao real no fluxo de detalhes por `app_id`.
- O sync em lote usa a busca publica da Steam Store para descobrir jogos e depois enriquece cada item via `appdetails`.
- O filtro operacional atual continua restrito a apps do tipo `game`.
- O projeto tambem passou a incluir login com Steam e sincronizacao da biblioteca possuida pelo usuario, expandindo o escopo original desta nota.

## Criterio De Pronto

- E possivel importar pelo menos alguns jogos reais da Steam.
- O catalogo usa esses dados locais normalmente.
- A capa fica visualmente mais consistente.
- O sistema continua funcionando sem consulta online na navegacao normal.

## Plano De Teste Manual

1. Importar um jogo por `steam_app_id`.
2. Confirmar criacao no banco.
3. Abrir catalogo e ver o jogo.
4. Abrir detalhe e verificar dados.
5. Sincronizar o mesmo jogo novamente.
6. Confirmar update sem duplicacao.
7. Testar jogo com imagem valida.
8. Testar falha de sync.
9. Confirmar que o catalogo nao quebra.

## Decisao Estrategica

Como a integracao com a Steam e tratada como parte primordial do futuro do site, este spec deve ser lido como linha principal de evolucao do catalogo e nao apenas como melhoria secundaria.

## Notas Relacionadas

- [[Catalogo de Jogos]]
- [[Models]]
- [[Views e URLs]]
- [[Backlog Pos-Entrega]]
