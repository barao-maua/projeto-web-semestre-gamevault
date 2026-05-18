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

- [ ] Remover CSS morto de `auth.css` (`auth-grid`, `auth-panel`, etc.) se realmente nao for mais usado.
- [ ] Remover CSS morto de `game-detail.css` (`inline-action-form`, etc.) se o fluxo modal atual for o definitivo.
- [ ] Revisar imports potencialmente mortos, como `authenticate` em views, quando aplicavel.
- [ ] Revisar settings nao utilizados, como `SITE_BASE_URL`, e decidir se ficam ou saem.
- [ ] Reduzir duplicacao de logica JS do checklist de senha entre cadastro e reset.
- [ ] Reduzir duplicacao de estilos de modal e status cards entre biblioteca e detalhe do jogo.

### Critério de pronto

- O codigo nao mantem estilos ou helpers claramente abandonados.
- Regras repetidas de senha/modal ficam centralizadas ou justificadas.

## Lote 3 - Robustez De Integracao E UX Tecnica

Foco: evitar comportamentos quebrados em casos reais de uso.

### Itens

- [ ] Tratar melhor `fetch` quando a sessao expira e o backend devolve HTML de login.
- [ ] Ajustar os fluxos AJAX para lidar com resposta nao JSON sem quebrar o front.
- [ ] Revisar se logout continua por GET ou se deve evoluir para POST no futuro.
- [ ] Rever a navbar de visitante para nao apontar para paginas mock como se fossem fluxo real.
- [ ] Revisar estrategia de active state na navbar para nao depender apenas de `request.path == ...`.
- [ ] Confirmar estrategia de `MEDIA_URL` e `MEDIA_ROOT` antes da implementacao de foto de perfil.

### Critério de pronto

- Os fluxos `fetch` falham de forma controlada.
- A navegacao publica nao induz o usuario a fluxos demonstrativos inconsistentes.

## Lote 4 - Alinhamento Final De Documentacao

Foco: garantir que README e wiki descrevam o sistema real.

### Itens

- [ ] Revisar `README.md` para remover descricoes de telas/filtros que nao existem mais.
- [ ] Revisar a documentacao de autenticacao sempre que login, email ou reset mudarem.
- [ ] Revisar `Pendencias.md` e `Entrega Final - Alternativa A.md` para evitar status conflitante.
- [ ] Revisar notas tecnicas (`Templates`, `Models`, `Views e URLs`) apos cada lote tecnico acima.

### Critério de pronto

- README, wiki funcional e wiki tecnica nao se contradizem.
- Pendencias e checklist da entrega apontam para o mesmo estado do projeto.

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
