---
title: Plano de Wikificação do GameVault
tipo: planejamento
status: planejado
area: documentacao
projeto: GameVault
tags:
  - gamevault
  - obsidian
  - wiki
  - documentacao
---

# Plano de Wikificação do GameVault

## Objetivo

Transformar o repositório/vault do [[GameVault]] em uma wiki navegável no Obsidian, conectando documentação, código, funcionalidades, decisões técnicas e fluxos visuais.

> [!todo] Como usar este plano
> Execute uma seção por vez. Ao finalizar cada plano, valide nomes, links e nível de detalhe antes de avançar para o próximo.

## Plano 1: Fundação da Wiki

Objetivo: criar o núcleo navegável do projeto.

Entregáveis:

- [x] `Docs/Wiki/00 - Inicio/00 - Mapa do Projeto.md`
- [x] `Docs/Wiki/01 - Projeto/GameVault.md`
- [x] Links para documentos existentes:
- [x] [README principal](../../../README.md)
- [x] [[DOCUMENTACAO_CSS]]
- [x] [[PLANO_REORGANIZACAO_CSS]]
- [x] [[Entrega2]]
- [x] Propriedades Obsidian padronizadas nas notas novas.

Resultado esperado: abrir uma nota central e conseguir navegar pelo projeto inteiro.

## Plano 2: Documentação Técnica do Django

Objetivo: transformar a estrutura do código em notas conectadas.

Entregáveis:

- [x] `Docs/Wiki/02 - Tecnico/Arquitetura.md`
- [x] `Docs/Wiki/02 - Tecnico/Models.md`
- [x] `Docs/Wiki/02 - Tecnico/Views e URLs.md`
- [x] `Docs/Wiki/02 - Tecnico/Templates.md`
- [x] `Docs/Wiki/02 - Tecnico/Static e CSS.md`

Arquivos relacionados:

- `core/models.py`
- `core/views.py`
- `core/urls.py`
- `config/settings.py`
- `templates/base.html`
- `static/`

Resultado esperado: documentação técnica clara sobre como o projeto funciona.

## Plano 3: Wiki das Funcionalidades

Objetivo: documentar o produto e suas áreas principais.

Entregáveis:

- [x] `Docs/Wiki/03 - Funcionalidades/Funcionalidades.md`
- [x] `Docs/Wiki/03 - Funcionalidades/Autenticacao.md`
- [x] `Docs/Wiki/03 - Funcionalidades/Catalogo de Jogos.md`
- [x] `Docs/Wiki/03 - Funcionalidades/Biblioteca do Usuario.md`
- [x] `Docs/Wiki/03 - Funcionalidades/Paginas Institucionais.md`

Resultado esperado: entender o que o GameVault faz e onde cada funcionalidade vive no código.

## Plano 4: Canvas Visual

Objetivo: criar um mapa visual do projeto no Obsidian.

Entregável:

- [x] `Docs/Wiki/04 - Visual/GameVault.canvas`

Nós sugeridos:

- Usuário
- Login/Register
- Home
- Catálogo
- Detalhes do jogo
- Biblioteca
- Models
- Views
- Templates
- Static/CSS

Resultado esperado: visão visual rápida do fluxo e da arquitetura do sistema.

## Plano 5: Base do Obsidian

Objetivo: criar uma tabela navegável das notas.

Entregável:

- [x] `Docs/Wiki/Projeto GameVault.base`

Campos sugeridos:

- `tipo`
- `status`
- `area`
- `arquivo_relacionado`
- `prioridade`

Tipos possíveis:

- `arquitetura`
- `funcionalidade`
- `codigo`
- `interface`
- `decisao`
- `pendencia`

Resultado esperado: filtrar notas por área, status ou tipo dentro do Obsidian.

## Plano 6: Decisões e Pendências

Objetivo: transformar o vault em ferramenta de acompanhamento do projeto.

Entregáveis:

- [x] `Docs/Wiki/05 - Planejamento/Decisoes Tecnicas.md`
- [x] `Docs/Wiki/05 - Planejamento/Pendencias.md`
- [x] `Docs/Wiki/05 - Planejamento/Proximas Melhorias.md`

Resultado esperado: centralizar decisões, melhorias futuras e pendências do projeto.

## Plano 7: Limpeza e Consolidação do Vault

Objetivo: reduzir ambiguidades no Obsidian e alinhar documentacao, scripts e configuracoes com o estado atual do codigo.

Entregáveis:

- [x] `Docs/Wiki/05 - Planejamento/Limpeza do Vault.md`
- [x] Remover nota vazia `GameVault.md` da raiz.
- [x] Renomear README interno da wiki para `Docs/Wiki/Wiki Home.md`.
- [x] Configurar ignorados do Obsidian.
- [x] Atualizar `.gitignore`.
- [x] Atualizar README principal conforme os models atuais.
- [x] Revisar `seed_library_images.py`.
- [x] Registrar models no admin.
- [x] Criar testes basicos de models.

Resultado esperado: vault mais limpo, links menos ambiguos e documentacao mais alinhada ao codigo.

## Ordem Recomendada

1. Plano 1: Fundação da wiki.
2. Plano 2: Documentação técnica.
3. Plano 3: Funcionalidades.
4. Plano 4: Canvas visual.
5. Plano 5: Base do Obsidian.
6. Plano 6: Decisões e pendências.
7. Plano 7: Limpeza e consolidação do vault.

## Primeiro Ciclo Recomendado

Começar com uma versão pequena para validar estilo, nomes e nível de detalhe:

- [x] `Docs/Wiki/00 - Inicio/00 - Mapa do Projeto.md`
- [x] `Docs/Wiki/01 - Projeto/GameVault.md`
- [x] `Docs/Wiki/02 - Tecnico/Arquitetura.md`
- [x] `Docs/Wiki/03 - Funcionalidades/Funcionalidades.md`

Depois da validação, expandir para os planos seguintes.
