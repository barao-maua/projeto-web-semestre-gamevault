---
title: Dificuldades Tecnicas
aliases:
  - Dificuldades Técnicas
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - dificuldades
  - entrega-final
  - ux
---

# Dificuldades Tecnicas

Esta nota registra as principais dificuldades tecnicas e de refinamento encontradas durante a evolucao do [[GameVault]].

## Maior Complexidade Ate Agora

A parte de maior complexidade ate o momento foi o refinamento iterativo dos fluxos de autenticacao, avaliacao e interface.

Isso ficou evidente pelo numero de ajustes sucessivos feitos em problemas do mesmo sentido, o que indica que a dificuldade nao estava apenas em fazer o sistema funcionar, mas em alinhar comportamento real, usabilidade e apresentacao.

## Por Que Foi Complexo

- Varias mudancas dependiam ao mesmo tempo de backend, templates, JavaScript e CSS.
- Alguns fluxos funcionavam tecnicamente, mas ainda falhavam na experiencia do usuario.
- Em muitos casos, um ajuste resolvia a regra de negocio, mas expunha um problema de contraste, cache, modal, mensagem duplicada ou consistencia visual.
- O uso repetido de prompts de mesmo sentido foi um sinal claro de que a complexidade estava no refinamento e nao apenas na implementacao bruta.

## Areas Mais Sensiveis

### Autenticacao E Email

- Inclusao de email obrigatorio e unico no cadastro.
- Verificacao de email sem bloquear login.
- Reenvio de verificacao.
- Recuperacao de senha por email.
- Login por username ou email.

Por que exigiu varias iteracoes:

- precisava manter compatibilidade com o fluxo antigo;
- precisava funcionar com `User` padrao do Django;
- precisava evitar travar o usuario caso o envio de email falhasse;
- precisava alinhar mensagens, redirecionamentos e status de verificacao.

### Senha E Feedback Visual

- Checklists visuais no cadastro e no reset de senha.
- Remocao dos help texts padrao do Django.
- Reforco da regra de senha no backend.

Por que exigiu varias iteracoes:

- a regra visual precisava bater com a regra real do backend;
- o comportamento esperado pelos testes era mais forte do que a validacao inicial;
- foi necessario ajustar os criterios para maiuscula, minuscula, numero e caractere especial.

### Biblioteca E Avaliacoes

- Modal para adicionar jogo a biblioteca.
- CTA para avaliar apos adicionar.
- Avaliacao antes de adicionar a biblioteca.
- Feedback visual no modal de avaliacao.
- Atualizacao da avaliacao anterior do mesmo usuario.

Por que exigiu varias iteracoes:

- havia mistura entre regra de negocio e experiencia de apresentacao;
- o fluxo precisava parecer natural para o usuario, sem `prompt()` e com menos `alert()` nativo;
- foi necessario revisar varias vezes o comportamento do modal, a opacidade, o retorno visual e a coerencia entre detalhe e biblioteca.

### Contraste E Interface

- Campo de busca do catalogo.
- Texto dos botoes verdes.
- Chip de sessao ativa.
- Modal de logout.
- Problemas de cache de CSS no navegador.

Por que exigiu varias iteracoes:

- alguns problemas nao estavam no HTML, mas no autofill do navegador ou em cache de estilos antigos;
- o que parecia simples exigiu ajustes especificos de contraste, estado de hover, visited, focus e `-webkit-autofill`.

## O Que Foi Feito Para Reduzir O Problema

- Substituicao progressiva de `prompt()` e `alert()` por modais e feedbacks visuais.
- Separacao entre regra real de backend e ajuda visual no frontend.
- Cache busting em CSS especifico quando necessario.
- Uso de notas de spec para concentrar decisoes antes da implementacao.
- Revisao continua da wiki para manter contexto compartilhado.

## Aprendizado Tecnico

- Quando varios prompts/ajustes do mesmo tipo sao necessarios, isso normalmente indica alta complexidade de refinamento.
- Em aplicacoes com Django SSR, a parte dificil muitas vezes nao e a rota ou o model, mas a consistencia entre formulario, template, feedback visual e estado do navegador.
- Documentar o motivo de cada ajuste ajuda a evitar retrabalho e reduz regressao em rodadas futuras.

## Notas Relacionadas

- [[Entrega Final - Alternativa A]]
- [[Decisoes Tecnicas]]
- [[Autenticacao]]
- [[Spec - Email Verificacao e Reset de Senha]]
