# Plano de Reorganizacao do CSS

## Objetivo

Reorganizar o CSS do projeto para seguir boas praticas, separando estilos globais, componentes compartilhados e estilos especificos por pagina, sem mudar a identidade visual atual.

## Estrutura Recomendada

```text
static/css/
  base.css
  components.css
  responsive.css
  pages/
    home.css
    auth.css
    catalog.css
    library.css
    game-detail.css
    profile.css
    sobre.css
    diferenciais.css
```

## Criterio de Organizacao

1. Se o seletor for usado em varias telas, ele vai para `components.css`.
2. Se o seletor for usado em apenas uma tela, ele vai para `pages/...`.
3. Se houver duvida, preferir colocar no CSS da pagina para reduzir acoplamento.
4. A responsividade global fica centralizada em `responsive.css`.

## Etapa 1: Preparar a estrutura

1. Criar os arquivos:
   - `static/css/base.css`
   - `static/css/components.css`
   - `static/css/responsive.css`
   - `static/css/pages/home.css`
   - `static/css/pages/auth.css`
   - `static/css/pages/catalog.css`
   - `static/css/pages/library.css`
   - `static/css/pages/game-detail.css`
   - `static/css/pages/profile.css`
   - `static/css/pages/sobre.css`
   - `static/css/pages/diferenciais.css`
2. Manter `static/css/style.css` temporariamente durante a migracao.
3. So parar de importar `style.css` quando todos os novos arquivos estiverem conectados.

## Etapa 2: Atualizar o template base

Arquivo: `templates/base.html`

Substituir:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

Por:

```html
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/components.css' %}">
<link rel="stylesheet" href="{% static 'css/responsive.css' %}">
{% block extra_css %}{% endblock %}
```

Observacao:

1. Manter o `body_class` atual, porque ele ja ajuda a identificar a pagina.
2. O bloco `extra_css` sera usado pelos templates especificos.

## Etapa 3: Extrair o CSS global para `base.css`

Arquivo de origem: `static/css/style.css`

Mover para `base.css`:

### Variaveis e reset

- `:root`
- `*`
- `html`
- `body`
- `a`
- `button, input, textarea, select`

### Estrutura base

- `.app-shell`
- `.app-shell::before`
- `.app-shell::after`
- `.site-main`
- `.page`
- `.page > .screen + .screen`
- `.screen`
- `.screen::after`

### Tipografia e estrutura de secao

- `h1, h2, h3, h4, h5, h6`
- `h1`
- `h2`
- `h3`
- `p, label, li`
- `input, textarea, select`
- `.screen-header`
- `.section-heading`
- `.section-heading p`
- `.eyebrow`

### Mensagens

- `.flash-messages`
- `.flash-messages .alert`

## Etapa 4: Extrair componentes compartilhados para `components.css`

Arquivo de origem: `static/css/style.css`

Mover para `components.css`:

### Navbar

- `.site-header`
- `.navbar`
- `.navbar, .site-main, .site-footer`
- `.brand`
- `.brand:visited, .brand:hover, .brand:focus`
- `.brand-mark`
- `.brand-text strong, .brand-text span`
- `.brand-text span`
- `.brand-text strong`
- `.nav-links`
- `.nav-link`
- `.nav-link:hover, .nav-link.is-active`
- `.nav-link:visited, .nav-link:focus`
- `.user-chip`
- `.user-chip-text`
- `.user-chip-text strong, .user-chip-text span`
- `.user-chip-text strong`
- `.user-chip-text span`
- `.user-avatar`

### Botoes e acoes genericas

- `.button, .ghost-button`
- `.button`
- `.button:hover`
- `.ghost-button`
- `.ghost-button:hover`
- `.screen-actions, .inline-actions`

### Formularios compartilhados

- `.field`
- `.field label`
- `.field input, .field textarea, .field select`
- `.field input::placeholder, .field textarea::placeholder`
- `.field input:focus, .field textarea:focus, .field select:focus`
- `.form-help-text`
- `.form-error`
- `.form-submit`

### Cards e elementos compartilhados

- `.library-grid`
- `.game-card`
- `.game-cover`
- `.game-cover img`
- `.game-cover--focus-top img`
- `.game-cover::before`
- `.cover-caption`
- `.cover-caption span, .cover-caption strong`
- `.cover-caption span`
- `.cover-caption strong`
- `.game-rating`
- `.game-actions`
- `.game-actions span`
- `.game-actions--spaced`
- `.empty-library, .empty-state`
- `.empty-library .button, .empty-state .button`
- `.placeholder-image`

### Footer

- `.site-footer`
- `.site-footer p`
- `.site-footer-nav`

Observacao:

1. `game-card`, `game-cover` e `cover-caption` aparecem em varias telas e devem ficar compartilhados.
2. `placeholder-image` deve ser criado se nao existir, porque esta sendo usado em templates do catalogo e detalhe.

## Etapa 5: Separar a Home em `pages/home.css`

Template: `templates/pages/home.html`

Adicionar:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/home.css' %}">
{% endblock %}
```

Mover para `home.css`:

- `.hero-grid`
- `.hero-copy`
- `.hero-copy p`
- `.stats-grid`
- `.stat-card`
- `.stat-card strong`
- `.hero-preview`
- `.preview-window`
- `.preview-bar`
- `.preview-cards`
- `.preview-card`
- `.preview-card strong, .preview-card span`
- `.preview-card strong`
- `.preview-card span`
- `.preview-card.is-highlighted`

## Etapa 6: Separar login e cadastro em `pages/auth.css`

Templates:

- `templates/registration/login.html`
- `templates/registration/register.html`

Adicionar nos dois:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/auth.css' %}">
{% endblock %}
```

Mover para `auth.css`:

- `.auth-shell`
- `.auth-shell form`
- `.auth-footer`
- `.auth-footer a`
- `.auth-grid`
- `.auth-panel`
- `.auth-panel + .auth-panel`
- `.panel-title`
- `.form-grid`
- `.mini-note`
- `.mini-note strong`

Observacao:

1. Parte desses seletores pode estar subutilizada hoje, mas vale manter organizada para a area de autenticacao.

## Etapa 7: Separar o catalogo em `pages/catalog.css`

Template: `templates/catalog/game_catalog.html`

Adicionar:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/catalog.css' %}">
{% endblock %}
```

Mover para `catalog.css`:

- `.catalog-header`
- `.search-form`
- `.search-form input`
- `.games-grid`
- `.game-card-image`
- `.game-card-image img`
- `.game-card-content`
- `.game-genre`
- `.game-description`
- seletores relacionados a estado vazio do catalogo, se forem especificos

## Etapa 8: Separar a biblioteca em `pages/library.css`

Template: `templates/library/library.html`

Adicionar:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/library.css' %}">
{% endblock %}
```

Mover para `library.css`:

- `.library-header`

Observacao:

1. Grande parte dos cards da biblioteca deve ficar em `components.css`, porque esses blocos tambem sao usados na home e em `sobre.html`.

## Etapa 9: Separar o detalhe do jogo em `pages/game-detail.css`

Template: `templates/catalog/game_detail.html`

Adicionar:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/game-detail.css' %}">
{% endblock %}
```

Mover para `game-detail.css`:

- `.game-detail-hero, .game-detail-panels`
- `.game-detail-hero`
- `.game-detail-panels`
- `.game-detail-image, .game-detail-info, .game-detail-description, .game-reviews, .review-card, .modal-content`
- `.game-detail-image`
- `.game-detail-image img`
- `.game-detail-info`
- `.game-detail-info h1`
- `.game-detail-meta-grid`
- `.detail-meta-item`
- `.detail-meta-item span, .detail-meta-item strong`
- `.detail-meta-item span`
- `.detail-meta-item strong`
- `.game-detail-summary`
- `.game-detail-actions`
- `.game-detail-action-buttons`
- `.game-detail-description`
- `.game-detail-description-note`
- `.game-detail-description-note p`
- `.library-status`
- `.library-status strong`
- `.library-status p`
- `.library-status-header`
- `.library-status--empty`
- `.status-badge`
- `.status-playing, .status-completed, .status-plan_to_play, .status-paused, .status-dropped`
- `progress`
- `.reviews-list`
- `.review-card--empty`
- `.review-header`
- `.review-rating`
- `.review-date`
- `.review-comment`
- `.modal`
- `.modal-content`
- `.close-modal`
- `.form-group`
- `.rating-select`
- `.rating-select.hearts label`
- `.rating-select.hearts label:hover`
- `.rating-select.hearts label.selected`
- `.rating-select.hearts input[type="radio"]`
- `.review-rating.hearts`
- `.review-rating.hearts .heart-selected`
- `.review-rating.hearts .heart-empty`

## Etapa 10: Separar o perfil em `pages/profile.css`

Template: `templates/registration/profile.html`

Adicionar:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/profile.css' %}">
{% endblock %}
```

Adicionar ou mover para `profile.css`:

- `.profile-container`
- `.user-info`

Observacao:

1. Esses seletores nao parecem estar definidos hoje no CSS principal, entao o arquivo pode ser criado do zero com o minimo necessario.

## Etapa 11: Separar `sobre.html` em `pages/sobre.css`

Template: `templates/pages/sobre.html`

Adicionar:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/sobre.css' %}">
{% endblock %}
```

Mover para `sobre.css`:

- `.meta-grid`
- `.meta-card`
- `.meta-card strong`

Observacao:

1. Essa pagina reutiliza `library-grid`, `game-card`, `game-cover`, `cover-caption`, `game-rating` e `game-actions`.
2. Por isso, esses blocos devem continuar em `components.css`.

## Etapa 12: Separar `diferenciais.html` em `pages/diferenciais.css`

Template: `templates/pages/diferenciais.html`

Adicionar:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/diferenciais.css' %}">
{% endblock %}
```

Mover para `diferenciais.css`:

- `.detail-layout`
- `.detail-main`
- `.cover-panel`
- `.rating-panel`
- `.cover-panel .game-cover`
- `.game-cover--detail`
- `.rating-stars`
- `.rating-stars .star`
- `.rating-stars .star:hover`
- `.rating-stars .star.active, .rating-stars .star:hover ~ .star`
- `.rating-stars .star.active`
- `.rating-feedback`
- `.review-hint`
- `.rating-panel textarea`
- `.full-button`
- `.community-panel-title`
- `.community-list`
- `.community-card`
- `.community-card-header`
- `.community-avatar`
- `.community-card strong`
- `.reviewer-comment`
- `.community-card p`
- `.feature-grid`
- `.feature-card`
- `.feature-card strong`

## Etapa 13: Centralizar a responsividade em `responsive.css`

Arquivo de origem: `static/css/style.css`

Mover para `responsive.css`:

- `@media (max-width: 1080px) { ... }`
- `@media (max-width: 820px) { ... }`
- `@media (max-width: 560px) { ... }`

Regra pratica:

1. Media queries que afetam varias telas ficam aqui.
2. Se alguma media query for muito especifica de uma pagina, ela pode ir para o arquivo da pagina.

## Etapa 14: Resolver duplicacoes e inconsistencias

Durante a migracao, revisar os seletores duplicados ou espalhados:

1. `cover-caption` aparece repetido.
2. `rating-stars` aparece em mais de um trecho.
3. Estilos de review e rating estao espalhados.
4. `placeholder-image` esta sendo usado em HTML, mas nao parece definido no CSS atual.
5. `profile-container` e `user-info` precisam ser definidos, porque aparecem no template de perfil.

Regra:

1. Cada seletor deve ter uma definicao principal.
2. Evitar copiar o mesmo bloco em mais de um arquivo.

## Etapa 15: Templates que precisam receber `extra_css`

Adicionar o bloco `extra_css` nestes templates:

1. `templates/pages/home.html`
2. `templates/registration/login.html`
3. `templates/registration/register.html`
4. `templates/catalog/game_catalog.html`
5. `templates/library/library.html`
6. `templates/catalog/game_detail.html`
7. `templates/registration/profile.html`
8. `templates/pages/sobre.html`
9. `templates/pages/diferenciais.html`

## Etapa 16: Validacao visual

Depois da separacao, revisar manualmente:

### Home

- hero
- cards
- preview
- botoes

### Login e cadastro

- campos
- espacamentos
- mensagens
- mobile

### Catalogo

- busca
- grid
- cards
- estado vazio

### Biblioteca

- capa
- status
- botoes
- responsividade

### Detalhe do jogo

- imagem
- layout em colunas
- modal
- avaliacoes
- progresso

### Perfil

- alinhamento
- visual minimo coerente

### Sobre e diferenciais

- grids
- cards
- estrelas/coracoes
- responsividade

## Etapa 17: Limpeza final

1. Conferir se `style.css` nao esta mais sendo importado.
2. Conferir se todos os seletores migrados ficaram com destino correto.
3. Remover o uso de `style.css` do projeto.
4. Se tudo estiver estavel, decidir se `style.css` sera apagado ou mantido apenas como historico temporario.

## Resultado Esperado

Ao final, o projeto deve ficar com:

1. Um CSS global pequeno e claro.
2. Componentes compartilhados centralizados.
3. Estilos especificos separados por pagina.
4. Melhor manutencao e melhor explicacao para apresentacao.

## Forma de Explicar para o Professor

Uma justificativa simples pode ser:

1. Antes o projeto tinha um unico arquivo CSS muito grande.
2. A refatoracao separa estilos globais, componentes reutilizaveis e estilos por pagina.
3. Isso melhora legibilidade, manutencao e reduz o risco de uma tela quebrar outra.
4. A estrutura do CSS passou a seguir a mesma organizacao modular usada em rotas, views e templates.
