---
title: Plano de Saneamento do Codigo
aliases:
  - Saneamento do Codigo
  - Plano de Revisao Tecnica
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - refactor
  - revisao
  - qualidade
---

# Plano de Saneamento do Codigo

Esta nota organiza os ajustes tecnicos identificados na revisao do projeto antes de abrir novos specs de maior escopo, como listas personalizadas, foto de perfil e integracao com Steam.

## Objetivo

Melhorar consistencia, reduzir codigo morto, corrigir fragilidades de fluxo e alinhar documentacao e comportamento real do sistema.

## Motivacao

Os fluxos principais do GameVault ja funcionam, mas a revisao mostrou alguns pontos de divida tecnica:

- inconsistencias entre backend e frontend;
- validacoes incompletas no dominio;
- componentes duplicados ou mortos;
- documentacao ainda divergente em partes importantes;
- fluxos `fetch` que ainda podem falhar de modo confuso.

## Estrategia Geral

Executar o saneamento em quatro lotes:

1. bugs e consistencia funcional;
2. limpeza de codigo morto e duplicacoes;
3. robustez de integracao e UX tecnica;
4. alinhamento final da documentacao.

## Lote 1 - Bugs E Consistencia Funcional

Foco: corrigir os pontos que podem gerar dado inconsistente ou comportamento enganoso.

### Itens

- [x] Tornar o context processor de verificacao de email somente leitura.
- [x] Parar de criar `UserEmailVerification` automaticamente durante renderizacao de template.
- [x] Criar/garantir `UserEmailVerification` nos pontos corretos de escrita:
  - cadastro;
  - atualizacao de perfil;
  - verificacao de email;
  - reenvio de verificacao.
- [x] Validar `Review.rating` no backend com form ou `full_clean()`.
- [x] Validar `Review.comment` pelo mesmo fluxo usado na avaliacao.
- [x] Ajustar `add_review_view` para retornar codigos HTTP coerentes em erro.
- [x] Corrigir o rotulo `Plataforma` no detalhe do jogo, que hoje exibe genero.
- [x] Revisar `add_to_library_view` e manter o suporte hibrido JSON + POST tradicional por compatibilidade com os fluxos atuais.

### Critério de pronto

- Nenhuma renderizacao normal de pagina faz escrita oculta no banco.
- Avaliacoes invalidas nao entram no banco.
- O detalhe do jogo nao mostra label semantica errada.
- O fluxo de adicao a biblioteca fica formalmente mantido como endpoint hibrido, com comportamento documentado.

## Lote 2 - Limpeza De Codigo Morto E Duplicacoes

Foco: remover sobras de fluxos antigos e reduzir risco de drift.

### Itens

- [x] Remover CSS morto de `auth.css` (`auth-grid`, `auth-panel`, etc.) se realmente nao for mais usado.
- [x] Remover CSS morto de `game-detail.css` (`inline-action-form`, etc.) se o fluxo modal atual for o definitivo.
- [x] Revisar imports potencialmente mortos, como `authenticate` em views, quando aplicavel.
- [x] Revisar settings nao utilizados, como `SITE_BASE_URL`, e decidir se ficam ou saem.
- [x] Reduzir duplicacao de logica JS do checklist de senha entre cadastro e reset.
- [x] Reduzir duplicacao de estilos de modal e status cards entre biblioteca e detalhe do jogo.

Implementacao realizada neste lote:

- CSS legado de autenticacao removido de `auth.css` e referencias responsivas associadas limpas.
- Estilos mortos de fluxo antigo removidos de `game-detail.css`.
- Checklist de senha extraido para parcial compartilhado e script unico em `static/js/password-feedback.js`.
- Estilos de modal e `status-card` centralizados em `static/css/components/modals.css` para reuso entre biblioteca e detalhe do jogo.
- `SITE_BASE_URL` removido de `config/settings.py` por nao ter uso no codigo atual.
- Import `authenticate` mantido em `core/views.py` apos revisao, pois segue em uso no login.

### Critério de pronto

- O codigo nao mantem estilos ou helpers claramente abandonados.
- Regras repetidas de senha/modal ficam centralizadas ou justificadas.

Status do lote: concluido.

## Lote 3 - Robustez De Integracao E UX Tecnica

Foco: evitar comportamentos quebrados em casos reais de uso.

### Itens

- [x] Tratar melhor `fetch` quando a sessao expira e o backend devolve HTML de login.
- [x] Ajustar os fluxos AJAX para lidar com resposta nao JSON sem quebrar o front.
- [x] Revisar se logout continua por GET ou se deve evoluir para POST no futuro.
- [x] Rever a navbar de visitante para nao apontar para paginas mock como se fossem fluxo real.
- [x] Revisar estrategia de active state na navbar para nao depender apenas de `request.path == ...`.
- [x] Confirmar estrategia de `MEDIA_URL` e `MEDIA_ROOT` antes da implementacao de foto de perfil.

Implementacao realizada neste lote:

- Helper global `static/js/http.js` criado para centralizar `fetch`, CSRF, sessao expirada e resposta nao JSON.
- Fluxos AJAX de biblioteca e detalhe do jogo migrados para o helper comum, com falha controlada em sessao expirada e HTML inesperado.
- Logout migrado de GET para POST em `logout_view`, modal da navbar e perfil.
- Navbar publica revisada para apontar para fluxos reais (`Catalogo` e `Sobre`) em vez de rotulos mock.
- Active state da navbar revisado para usar `request.resolver_match.url_name`, incluindo destaque correto para detalhe do jogo dentro de `Catalogo`.
- Estrategia atual de media confirmada: `MEDIA_URL = "/media/"`, `MEDIA_ROOT = BASE_DIR / "media"` e servico local habilitado em `config/urls.py` apenas em `DEBUG`.

### Critério de pronto

- Os fluxos `fetch` falham de forma controlada.
- A navegacao publica nao induz o usuario a fluxos demonstrativos inconsistentes.

Status do lote: concluido.

## Lote 4 - Alinhamento Final De Documentacao

Foco: garantir que README e wiki descrevam o sistema real.

### Itens

- [x] Revisar `README.md` para remover descricoes de telas/filtros que nao existem mais.
- [x] Revisar a documentacao de autenticacao sempre que login, email ou reset mudarem.
- [x] Revisar `Pendencias.md` e `Entrega Final - Alternativa A.md` para evitar status conflitante.
- [x] Revisar notas tecnicas (`Templates`, `Models`, `Views e URLs`) apos cada lote tecnico acima.

Implementacao realizada neste lote:

- `README.md` revisado para remover referencias a filtro/barra de busca da biblioteca e alinhar o fluxo atual de reviews, biblioteca e execucao local.
- Nota [[Autenticacao]] atualizada para refletir login por form proprio, logout via `POST` e navegacao publica real.
- `Pendencias.md` e `Entrega Final - Alternativa A.md` alinhados com o estado atual de historico de reviews, robustez de `fetch` e autenticacao.
- Notas tecnicas `Templates`, `Models` e `Views e URLs` revisadas para refletir logout via `POST`, helper global de AJAX, servico de `media/` em `DEBUG` e historico de reviews com exibicao principal da review mais recente.

### Critério de pronto

- README, wiki funcional e wiki tecnica nao se contradizem.
- Pendencias e checklist da entrega apontam para o mesmo estado do projeto.

Status do lote: concluido.

## Ordem Recomendada De Execucao

1. Lote 1 - bugs e consistencia funcional.
2. Lote 3 - robustez de integracao e UX tecnica.
3. Lote 2 - limpeza de codigo morto e duplicacoes.
4. Lote 4 - alinhamento final de documentacao.

## O Que Nao Entra Neste Plano

Este plano nao cobre implementacao de features novas de escopo maior, como:

- [[Spec - Listas Personalizadas]]
- [[Spec - Foto de Perfil]]
- [[Spec - Integracao Steam]]

Esses specs devem avancar depois que os lotes acima reduzirem o risco tecnico do projeto.

## Resultado Esperado

Ao final do saneamento, o GameVault deve ficar:

- mais consistente entre backend, frontend e documentacao;
- menos dependente de comportamento acidental do navegador;
- com menos codigo morto;
- mais seguro para evoluir com os proximos recursos.

## Notas Relacionadas

- [[Pendencias]]
- [[Dificuldades Tecnicas]]
- [[Entrega Final - Alternativa A]]
- [[Spec - Listas Personalizadas]]
- [[Spec - Foto de Perfil]]
- [[Spec - Integracao Steam]]
