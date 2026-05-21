---
title: Backlog Pos-Entrega
aliases:
  - Melhorias Pos-Entrega
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - backlog
  - pos-entrega
---

# Backlog Pos-Entrega

Esta nota registra melhorias que nao devem bloquear a entrega final, mas que foram identificadas durante a revisao do fluxo do [[GameVault]].

## Objetivo

Separar melhorias futuras da [[Entrega Final - Alternativa A]], mantendo o foco atual em autenticacao, ORM/Admin, CRUD da biblioteca e apresentacao.

## Alta Prioridade

### Progresso Do Jogo

Problema:

- A barra de progresso aparece no detalhe do jogo.
- O valor vem de `LibraryEntry.progress`.
- Ainda falta uma interface clara para o usuario editar esse progresso.

TODO:

- [ ] Criar interface para editar progresso.
- [ ] Permitir valores de 0 a 100.
- [ ] Avaliar uso de `input type="range"` ou campo numerico.
- [ ] Atualizar barra no detalhe do jogo.
- [ ] Validar que progresso nao passa de 0 a 100.

### Home Deslogada Com Cards Demonstrativos

Problema:

- A home deslogada mostra cards que parecem biblioteca ou catalogo real.
- A secao foi criada como demonstracao estatica, mas pode confundir o usuario.

TODO:

- [ ] Renomear secao para “Jogos em destaque”.
- [ ] Remover botao falso “Adicionar”.
- [ ] Usar “Ver detalhes” ou “Explorar catalogo”.
- [ ] Deixar claro que a biblioteca real depende de login.

### Pagina `/sobre/` Como Biblioteca Fake

Problema:

- A pagina publica `/sobre/` parece uma biblioteca real.
- Ela mostra cards com acoes falsas de editar/remover.

TODO:

- [ ] Transformar `/sobre/` em pagina institucional real.
- [ ] Trocar nome publico para “Sobre”.
- [ ] Remover cards falsos de editar/remover.
- [ ] Manter biblioteca real apenas em `/library/`.

### Rota `/diferenciais/` Removida Do Fluxo Atual

Problema:

- A rota institucional antiga nao faz mais parte do fluxo atual.
- O historico visual ainda aparece em arquivos legados de documentacao e CSS.

TODO:

- [ ] Decidir se a rota sera recriada no futuro ou arquivada definitivamente.
- [ ] Se voltar, reintroduzir apenas conteudo institucional real.
- [ ] Manter avaliacoes reais apenas no detalhe do jogo.

## Media Prioridade

### Separar Catalogo E Biblioteca

Problema:

- Alguns textos misturam catalogo, biblioteca e demonstracao.

TODO:

- [ ] Padronizar nomenclatura.
- [ ] `/catalog/`: Catalogo.
- [ ] `/library/`: Minha Biblioteca.
- [ ] `/`: Home/landing.
- [ ] `/sobre/`: Sobre.
- [ ] Confirmar oficialmente a ausencia de `/diferenciais/` no fluxo atual.

### Usuario Deslogado

Problema:

- Visitante ve botoes que parecem acionaveis, mas dependem de login ou sao falsos.

TODO:

- [ ] Mostrar CTAs claros para login/cadastro.
- [ ] Evitar botoes falsos.
- [ ] Remover links `href="#"`.
- [ ] Mostrar mensagem “Faca login para adicionar a biblioteca”.

### Dados Reais Vs Demonstrativos

Problema:

- Algumas paginas ainda usam dados hardcoded.

TODO:

- [ ] Listar dados hardcoded.
- [ ] Decidir se cada bloco deve virar conteudo institucional ou vir do banco.
- [ ] Documentar quais paginas sao dinamicas e quais sao institucionais.

## Baixa Prioridade

### Listas Personalizadas

TODO:

- [ ] Criar telas para `GameList`.
- [ ] Criar telas para `GameListItem`.
- [ ] Permitir criar listas personalizadas.
- [ ] Permitir adicionar jogos a listas.

### Estatisticas Reais Na Home

TODO:

- [ ] Substituir numeros estaticos por dados reais.
- [ ] Mostrar quantidade real de jogos no catalogo.
- [ ] Mostrar quantidade real de avaliacoes.
- [ ] Mostrar estatisticas apenas quando fizer sentido.

## Ordem Recomendada

1. Finalizar CRUD da biblioteca para a entrega final.
2. Consolidar `/sobre/` como pagina institucional real e decidir o destino definitivo da antiga `/diferenciais/`.
3. Melhorar progresso editavel.
4. Revisar experiencia de visitante.
5. Evoluir listas personalizadas.

## Notas Relacionadas

- [[Entrega Final - Alternativa A]]
- [[Biblioteca do Usuario]]
- [[Catalogo de Jogos]]
- [[Autenticacao]]
- [[Pendencias]]
- [[Decisoes Tecnicas]]
