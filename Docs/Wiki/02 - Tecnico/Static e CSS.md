---
title: Static e CSS
tipo: interface
status: ativo
area: tecnico
projeto: GameVault
arquivo_relacionado:
  - static/css/base.css
  - static/css/components.css
  - static/css/responsive.css
  - static/css/pages/
tags:
  - gamevault
  - css
  - static
  - interface
---

# Static e CSS

Os arquivos estaticos do [[GameVault]] ficam em `static/`. A configuracao em `config/settings.py` usa `STATICFILES_DIRS = [BASE_DIR / "static"]`, permitindo que os templates carreguem CSS e imagens com `{% static %}`.

## Estrutura CSS Atual

```text
static/css/
  base.css
  components.css
  responsive.css
  pages/
    auth.css
    catalog.css
    diferenciais.css
    game-detail.css
    home.css
    library.css
    profile.css
    sobre.css
```

## Responsabilidades

- `base.css`: variaveis, reset, estrutura global, tipografia, telas base e mensagens.
- `components.css`: navbar, botoes, formularios, cards, capas, estados vazios, status e footer.
- `responsive.css`: ajustes globais de responsividade, carregado por ultimo.
- `pages/*.css`: estilos especificos de cada pagina.

## Ordem De Carregamento

`templates/base.html` carrega os estilos nesta ordem:

1. Bootstrap via CDN.
2. Font Awesome via CDN.
3. `static/css/base.css`.
4. `static/css/components.css`.
5. Bloco `extra_css` com CSS especifico da pagina.
6. `static/css/responsive.css`.

Essa ordem permite que estilos globais sejam definidos primeiro, estilos de pagina ajustem detalhes especificos e regras responsivas tenham prioridade no final.

## CSS Por Pagina

| Template | CSS |
| --- | --- |
| `templates/pages/home.html` | `static/css/pages/home.css` |
| `templates/pages/sobre.html` | `static/css/pages/sobre.css` |
| `templates/pages/diferenciais.html` | `static/css/pages/diferenciais.css` |
| `templates/catalog/game_catalog.html` | `static/css/pages/catalog.css` |
| `templates/catalog/game_detail.html` | `static/css/pages/game-detail.css` |
| `templates/library/library.html` | `static/css/pages/library.css` |
| `templates/registration/login.html` | `static/css/pages/auth.css` |
| `templates/registration/register.html` | `static/css/pages/auth.css` |
| `templates/registration/profile.html` | `static/css/pages/profile.css` |

## Documentacao Visual Existente

- [[DOCUMENTACAO_CSS]]: explica a organizacao CSS atual.
- [[PLANO_REORGANIZACAO_CSS]]: registra o plano de modularizacao dos estilos.

## Imagens De Capa

`core/views.py` procura variantes locais de capa em:

- `static/img/home/`
- `static/img/catalog/`

Se existir um arquivo com mesmo nome-base da imagem original, a view usa a variante local para melhorar o enquadramento visual de cada tela.

## Notas Relacionadas

- [[Templates]]
- [[Views e URLs]]
- [[Arquitetura]]
- [[Catalogo de Jogos]]
