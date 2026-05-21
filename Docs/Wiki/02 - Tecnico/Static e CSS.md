---
title: Static e CSS
tipo: interface
status: ativo
area: tecnico
projeto: GameVault
arquivo_relacionado:
  - static/css/base.css
  - static/css/components/
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
  components/
    badges.css
    banners.css
    buttons.css
    footer.css
    forms.css
    game-card.css
    modals.css
    navbar.css
    user-chip.css
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
- `components/*.css`: componentes compartilhados quebrados por bloco visual, como navbar, user chip, botoes, formularios, modais, cards, badges, banners e footer.
- `responsive.css`: ajustes globais de responsividade, carregado por ultimo.
- `pages/*.css`: estilos especificos de cada pagina, incluindo feedback visual de formularios e modais.

## Ordem De Carregamento

`templates/base.html` carrega os estilos nesta ordem:

1. Bootstrap via CDN.
2. Font Awesome via CDN.
3. `static/css/base.css`.
4. `static/css/components/*.css` em ordem explicita no template base.
5. Bloco `extra_css` com CSS especifico da pagina.
6. `static/css/responsive.css`.

Essa ordem permite que estilos globais sejam definidos primeiro, estilos de pagina ajustem detalhes especificos e regras responsivas tenham prioridade no final.

## CSS Por Pagina

| Template | CSS |
| --- | --- |
| `templates/pages/home.html` | `static/css/pages/home.css` |
| `templates/pages/sobre.html` | `static/css/pages/sobre.css` |
| `templates/catalog/game_catalog.html` | `static/css/pages/catalog.css` |
| `templates/catalog/game_detail.html` | `static/css/pages/game-detail.css` |
| `templates/library/library.html` | `static/css/pages/library.css` |
| `templates/registration/login.html` | `static/css/pages/auth.css` |
| `templates/registration/register.html` | `static/css/pages/auth.css` |
| `templates/registration/profile.html` | `static/css/pages/profile.css` |

Arquivo legado sem rota ativa no momento:

- `static/css/pages/diferenciais.css`: mantido como historico visual de uma tela institucional removida do fluxo atual.

## Ajustes Relevantes Recentes

- `components/user-chip.css` destaca o chip de sessao ativa.
- `components/modals.css` centraliza modal de logout e modais compartilhados.
- `components/banners.css` centraliza o banner global para email pendente de verificacao.
- `components/buttons.css` concentra os botoes principais e secundario.
- `auth.css` passou a incluir:
  - checklist visual de senha;
  - status de confirmacao de senha em tempo real.
- `catalog.css` recebeu:
  - contraste reforcado no campo de busca;
  - tratamento para autofill do navegador.
- `game-detail.css` recebeu:
  - modal de avaliacao opaco;
  - feedback visual inline ao salvar avaliacao;
  - etapa de confirmacao apos adicionar jogo a biblioteca.
- `profile.css` passou a incluir:
  - card de status de verificacao de email;
  - estilos do formulario editavel de perfil.

## Observacao De Manutencao

Alguns estilos passaram a usar query string de versao no carregamento do template base ou da pagina para contornar cache agressivo do navegador durante os ajustes iterativos da interface.

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
