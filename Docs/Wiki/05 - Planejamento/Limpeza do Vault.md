---
title: Limpeza do Vault
tipo: planejamento
status: concluido
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - obsidian
  - limpeza
---

# Limpeza do Vault

Esta nota registra o Plano 7 de consolidacao do vault do [[GameVault]], executado depois da criacao da wiki inicial.

## Objetivo

Reduzir ambiguidade no Obsidian, alinhar documentacao com o codigo atual e remover ruidos que atrapalham a navegacao pelo vault.

## Itens Executados

- [x] Remover a nota vazia `GameVault.md` da raiz.
- [x] Renomear o README interno da wiki para [[Wiki Home]], evitando conflito com o README principal.
- [x] Trocar links ambiguos `[[README]]` por links Markdown para o README principal.
- [x] Configurar `.obsidian/app.json` para ignorar `.git/`, `.venv/`, `venv/`, `__pycache__/`, `.pyc`, `db.sqlite3` e journals SQLite.
- [x] Atualizar `.gitignore` para banco local, media e workspace local do Obsidian.
- [x] Atualizar o modelo de dados no README principal para refletir `core/models.py`.
- [x] Atualizar `seed_library_images.py` com os jogos e caminhos de imagem atuais.
- [x] Registrar os models no Django Admin.
- [x] Criar testes basicos de representacao dos models.

## Arquivos Alterados

- `.obsidian/app.json`
- `.gitignore`
- `README.md`
- `seed_library_images.py`
- `core/admin.py`
- `core/tests.py`
- `Docs/Wiki/Wiki Home.md`
- `Docs/Wiki/00 - Inicio/00 - Mapa do Projeto.md`
- `Docs/Wiki/05 - Planejamento/Plano de Wikificacao do GameVault.md`
- `Docs/Wiki/05 - Planejamento/Pendencias.md`
- `Docs/Wiki/05 - Planejamento/Proximas Melhorias.md`
- `Docs/Wiki/01 - Projeto/GameVault.md`

## Resultado Esperado

- Menos resultados falsos no grafo e na busca do Obsidian.
- Links principais menos ambiguos.
- Documentacao principal mais alinhada ao codigo.
- Admin do Django mais util para demonstracao e manutencao.
- Base tecnica minima para testes futuros.

## Proximos Cuidados

- Abrir o vault no Obsidian e confirmar se os filtros ignorados foram aplicados.
- Abrir [[Projeto GameVault.base]] e validar visualmente as views.
- Abrir [[GameVault.canvas]] e ajustar o layout manualmente, se necessario.
- Conferir se `db.sqlite3` ja estava rastreado pelo Git antes da alteracao do `.gitignore`.
