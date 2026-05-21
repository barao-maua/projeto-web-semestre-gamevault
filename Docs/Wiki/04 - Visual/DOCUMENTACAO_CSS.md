# Documentacao da Organizacao do CSS

## Objetivo

O CSS do GameVault foi reorganizado para separar responsabilidades e facilitar manutencao, leitura e apresentacao do projeto.

Antes, quase todos os estilos estavam concentrados em `static/css/style.css`. Agora, os estilos foram divididos entre base global, componentes reutilizaveis, responsividade e arquivos especificos de pagina.

## Estrutura Atual

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

## Responsabilidade dos Arquivos

`base.css`

Contem variaveis globais, reset simples, estilos do `body`, estrutura principal da pagina, tipografia, telas base e mensagens do Django.

`components/*.css`

Contem componentes compartilhados entre varias telas. O antigo `components.css` foi quebrado em arquivos menores por bloco visual, como navbar, botoes, formularios, cards de jogo, modais, badges, banners e footer.

`responsive.css`

Centraliza as regras de responsividade globais. Ele e carregado por ultimo para conseguir ajustar os estilos das paginas em telas menores.

`pages/*.css`

Contem estilos especificos de cada pagina. Isso reduz o risco de uma alteracao visual em uma tela afetar outra tela sem necessidade.

Observacao:

- `diferenciais.css` ainda existe como arquivo legado de uma rota institucional que nao esta mais ativa no fluxo atual.

## Como os Templates Carregam CSS

O arquivo `templates/base.html` carrega os estilos globais e disponibiliza o bloco `extra_css`:

```django
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/components/buttons.css' %}">
<link rel="stylesheet" href="{% static 'css/components/forms.css' %}">
<link rel="stylesheet" href="{% static 'css/components/navbar.css' %}">
<link rel="stylesheet" href="{% static 'css/components/user-chip.css' %}">
<link rel="stylesheet" href="{% static 'css/components/banners.css' %}">
<link rel="stylesheet" href="{% static 'css/components/modals.css' %}">
<link rel="stylesheet" href="{% static 'css/components/game-card.css' %}">
<link rel="stylesheet" href="{% static 'css/components/badges.css' %}">
<link rel="stylesheet" href="{% static 'css/components/footer.css' %}">
{% block extra_css %}{% endblock %}
<link rel="stylesheet" href="{% static 'css/responsive.css' %}">
```

Cada template de pagina adiciona seu CSS proprio dentro de `extra_css`. Exemplo:

```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/pages/home.css' %}">
{% endblock %}
```

## Criterios Usados na Separacao

1. Estilos globais foram para `base.css`.
2. Estilos usados por mais de uma tela foram para `static/css/components/`.
3. Estilos usados por apenas uma tela foram para `pages/`.
4. Regras mobile compartilhadas foram para `responsive.css`.
5. Duplicacoes simples, como estilos repetidos de `cover-caption`, foram consolidadas.

## Limpeza do CSS Antigo

O arquivo antigo `static/css/style.css` foi removido depois que todos os estilos passaram a ser carregados pelos arquivos modulares.

Na apresentacao, a explicacao recomendada e:

1. O projeto tinha um unico CSS grande.
2. A reorganizacao separou estilos globais, componentes menores e paginas.
3. Isso melhora manutencao e deixa mais claro onde cada estilo deve ser alterado.
4. O `responsive.css` fica por ultimo para preservar os ajustes em telas menores.
