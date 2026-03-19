# GameVault - Gerenciador de Jogos Pessoal

## Objetivo do Projeto

O **GameVault** é uma aplicação web transacional voltada para o gerenciamento de coleções de jogos digitais. O sistema permite que usuários organizem sua biblioteca pessoal de jogos, acompanhem o progresso, registrem avaliações e criem listas personalizadas.

O objetivo principal é **centralizar e facilitar o controle da coleção de jogos de cada usuário**, permitindo registrar status (como *Jogando* ou *Zerado*), avaliações e histórico de interação com os títulos cadastrados.

---

## Principais Funcionalidades (Histórias de Usuário)

### 1. Cadastro e Autenticação

**Como usuário**, quero me cadastrar e realizar login no sistema, para acessar e gerenciar minha biblioteca pessoal de jogos.

Funcionalidades:

- Cadastro de usuário
- Autenticação no sistema
- Acesso à biblioteca pessoal

---

### 2. Gerenciamento da Biblioteca

**Como usuário**, quero adicionar jogos à minha biblioteca, editar informações e removê-los, para manter minha coleção organizada.

Funcionalidades:

- Adicionar jogos
- Editar informações
- Remover jogos da biblioteca

---

### 3. Controle de Status e Progresso

**Como usuário**, quero definir o status de um jogo e registrar meu progresso, para acompanhar minha evolução.

Status possíveis:

- Backlog
- Jogando
- Concluído
- Dropado

Também é possível registrar o progresso do jogo.

---

### 4. Avaliação e Resenha

**Como usuário**, quero atribuir uma nota e escrever uma avaliação para um jogo, para registrar minha opinião pessoal.

Funcionalidades:

- Avaliação com nota
- Comentário ou review sobre o jogo

---

### 5. Criação de Listas Personalizadas

**Como usuário**, quero criar listas personalizadas e adicionar jogos a elas, para organizar minha coleção por categorias específicas.

Exemplos de listas:

- Jogos Favoritos
- Jogos para Jogar em 2026
- RPGs Preferidos

---

## Tipo de Aplicação

O **GameVault** é uma **aplicação web transacional com banco de dados relacional**, onde cada interação realizada pelo usuário é registrada e persistida no sistema.

As operações principais do sistema seguem o modelo **CRUD (Create, Read, Update, Delete)** sobre os seguintes recursos:

- Usuários
- Jogos
- Entradas na biblioteca
- Avaliações
- Listas personalizadas

---

## Protótipos de Tela

Foram desenvolvidos **três protótipos principais** que representam o fluxo de interação do usuário com o sistema.

Essas telas demonstram as principais funcionalidades da aplicação e a estrutura da interface.

---

### 1. Tela de Login e Cadastro

#### Objetivo

Permitir que o usuário crie uma conta ou acesse o sistema.

#### Elementos da interface

- Campo de e-mail
- Campo de senha
- Botão de login
- Link para cadastro

---

### 2. Tela da Biblioteca (Dashboard)

#### Objetivo

Exibir os jogos cadastrados pelo usuário e permitir o gerenciamento da biblioteca.

#### Funcionalidades

- Visualização da lista de jogos
- Filtro por status
- Adicionar novo jogo
- Editar ou remover jogo

#### Elementos principais

- Barra de busca
- Cards de jogos
- Botão **Adicionar Jogo**
- Filtro por status

---

### 3. Tela de Detalhes do Jogo

#### Objetivo

Permitir visualizar informações detalhadas e registrar avaliações.

#### Funcionalidades

- Alterar status do jogo
- Registrar progresso
- Avaliar jogo
- Escrever review

#### Elementos principais

- Nome do jogo
- Imagem de capa
- Dropdown de status
- Campo de nota (0 a 5)
- Campo de texto para avaliação

---

## Modelo de Dados

### Visão Geral

O modelo de dados do GameVault foi estruturado utilizando **banco de dados relacional**, onde cada entidade representa uma tabela.

Os relacionamentos são implementados através de **chaves estrangeiras (FK)**.

O sistema possui como entidade central o **User**, que se relaciona com as demais entidades do sistema.

---

## Entidades do Sistema

### User

Representa um usuário cadastrado na plataforma.

```
id (PK)
first_name
last_name
email
password
```

---

### Game

Representa um jogo disponível no sistema.

```
id (PK)
title
release_year
developer
cover_url
```

---

### LibraryEntry

Representa a relação entre usuário e jogo na biblioteca.

```
id (PK)
user_id (FK)
game_id (FK)
status
progress_hours
started_at
finished_at
```

---

### Review

Representa uma avaliação feita por um usuário sobre um jogo.

```
id (PK)
user_id (FK)
game_id (FK)
rating
text
created_at
```

---

### GameList

Representa listas personalizadas criadas por um usuário.

```
id (PK)
user_id (FK)
name
description
```

---

### GameListItem

Representa os jogos contidos em uma lista.

```
id (PK)
list_id (FK)
game_id (FK)
position
```

---

## Relacionamentos

- Um **User** pode possuir vários **LibraryEntry** (1:N)
- Um **Game** pode estar presente em vários **LibraryEntry** (1:N)
- Um **User** pode escrever várias **Review** (1:N)
- Um **Game** pode receber várias **Review** (1:N)
- Um **User** pode criar várias **GameList** (1:N)
- Uma **GameList** pode conter vários **GameListItem** (1:N)
- Um **Game** pode estar presente em vários **GameListItem** (1:N)

---

## Caracterização como Aplicação Transacional

O sistema permite realizar operações **CRUD** sobre os principais recursos da aplicação:

- Usuários
- Jogos
- Entradas na biblioteca
- Avaliações
- Listas personalizadas

Essas operações caracterizam o **GameVault como uma aplicação web transacional**, utilizando banco de dados relacional para persistência das informações.

## Como Rodar o Projeto

Atualmente o projeto esta configurado para ser executado no **Windows PowerShell** usando o ambiente virtual local `.venv`.

### 1. Abrir a pasta do projeto

```powershell
cd "C:\Users\bruno\OneDrive\Area de Trabalho\Codigos\projeto-web-semestre-gamevault"
```

### 2. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativacao, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 3. Rodar o servidor Django

```powershell
python manage.py runserver
```

Se preferir, tambem e possivel rodar sem ativar o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

### 4. Acessar no navegador

Depois de iniciar o servidor, abrir:

```text
http://127.0.0.1:8000/
```

### 5. Verificar se o projeto esta correto

Para validar a configuracao do Django:

```powershell
python manage.py check
```

## LINK FIGMA: https://www.figma.com/design/eSWG1sVcLrNMDDuWZRtGVx/GameValt?node-id=0-1&t=QbiYw86OHCeU2THv-1
