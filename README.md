# GameVault - Gerenciador de Jogos Pessoal

## Objetivo do Projeto

O **GameVault** é uma aplicação web transacional voltada para o gerenciamento de coleções de jogos digitais. O sistema permite que usuários organizem sua biblioteca pessoal de jogos, acompanhem o progresso, registrem avaliações e criem listas personalizadas.

O objetivo principal é **centralizar e facilitar o controle da coleção de jogos de cada usuário**, permitindo registrar status, avaliações e histórico de interação com os títulos cadastrados.

No estado atual da entrega, o foco principal esta em autenticacao, catalogo, biblioteca pessoal, avaliacoes e integracao com a Steam. O projeto ja consegue usar a Steam como fonte de descoberta e sincronizacao de dados, mantendo o banco local como base persistente da aplicacao.

---

## Principais Funcionalidades (Histórias de Usuário)

### 1. Cadastro e Autenticação

**Como usuário**, quero me cadastrar e realizar login no sistema, para acessar e gerenciar minha biblioteca pessoal de jogos.

Funcionalidades:

- Cadastro com email obrigatorio
- Login com usuario ou email
- Verificacao de email sem bloquear acesso
- Recuperacao de senha por email
- Login com Steam via OpenID
- Edicao de perfil com avatar local
- Acesso a biblioteca pessoal

---

### 2. Gerenciamento da Biblioteca

**Como usuário**, quero adicionar jogos à minha biblioteca, editar informações e removê-los, para manter minha coleção organizada.

Funcionalidades:

- Adicionar jogos
- Editar informações
- Remover jogos da biblioteca
- Sincronizar jogos possuidos na Steam para a biblioteca local

---

### 3. Controle de Status

**Como usuário**, quero definir o status de um jogo, para manter minha coleção organizada e coerente com o que já joguei ou pretendo jogar.

Status possíveis no código atual:

- Jogando
- Pausado
- Concluído
- Abandonado
- Planejo Jogar

O model ainda possui campo de progresso, mas a experiencia principal atual da interface prioriza status e avaliacao.

---

### 4. Avaliação e Resenha

**Como usuário**, quero atribuir uma nota e escrever uma avaliação para um jogo, para registrar minha opinião pessoal.

Funcionalidades:

- Avaliação com nota
- Comentário ou review sobre o jogo
- Preservacao do historico de reviews por usuario e jogo

---

### 5. Criação de Listas Personalizadas

**Como usuário**, quero criar listas personalizadas e adicionar jogos a elas, para organizar minha coleção por categorias específicas.

Exemplos de listas:

- Jogos Favoritos
- Jogos para Jogar em 2026
- RPGs Preferidos

Observacao:

- A modelagem de listas personalizadas existe no codigo atual, mas a interface completa desse recurso ficou fora do escopo principal da entrega.

---

### 6. Integracao com Steam

**Como usuário**, quero aproveitar dados da Steam e, quando fizer sentido, autenticar ou sincronizar minha conta, para reduzir cadastro manual e acelerar a montagem da minha biblioteca.

Funcionalidades:

- Busca de jogos com apoio do catalogo da Steam
- Cache local de jogos sincronizados
- Pagina de detalhe por `app_id` da Steam
- Login com Steam
- Vinculo entre usuario local e conta Steam
- Sincronizacao da biblioteca possuida na Steam

---

## Tipo de Aplicação

O **GameVault** é uma **aplicação web transacional com banco de dados relacional**, onde cada interação realizada pelo usuário é registrada e persistida no sistema.

As operações principais do sistema seguem o modelo **CRUD (Create, Read, Update, Delete)** sobre os seguintes recursos:

- Usuarios
- Jogos
- Entradas na biblioteca
- Avaliacoes
- Listas personalizadas
- Vinculos de conta Steam
- Perfis locais do usuario

Na interface atual, o fluxo mais maduro do sistema esta em:

- autenticacao local e Steam;
- catalogo com fallback local;
- biblioteca do usuario;
- avaliacoes com historico;
- perfil do usuario.

---

## Protótipos de Tela

Foram desenvolvidos **três protótipos principais** que representam o fluxo de interação do usuário com o sistema.

Essas telas demonstram as principais funcionalidades da aplicação e a estrutura da interface.

---

### 1. Tela de Login e Cadastro

#### Objetivo

Permitir que o usuário crie uma conta ou acesse o sistema.

#### Elementos da interface

- Campo de usuario ou email
- Campo de senha
- Botao de login
- Link para cadastro
- Link de esqueci minha senha

---

### 2. Tela da Biblioteca (Dashboard)

#### Objetivo

Exibir os jogos cadastrados pelo usuário e permitir o gerenciamento da biblioteca.

#### Funcionalidades

- Visualização da lista de jogos
- Editar status do jogo
- Remover jogo da biblioteca
- Abrir modal para registrar nova avaliação após mudar status

#### Elementos principais

- Cards de jogos
- Botão **Explorar Catálogo**
- Botão **Editar**
- Botão **Remover**

---

### 3. Tela de Detalhes do Jogo

#### Objetivo

Permitir visualizar informações detalhadas e registrar avaliações.

#### Funcionalidades

- Alterar status do jogo
- Avaliar jogo
- Escrever review
- Registrar nova review no historico do mesmo usuario

#### Elementos principais

- Nome do jogo
- Imagem de capa
- Selecao visual de status
- Campo de nota (1 a 5)
- Campo de texto para avaliacao

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

Observacao:

- O estado de verificacao do email e controlado separadamente por uma entidade auxiliar.

---

### Game

Representa um jogo disponível no sistema.

```
id (PK)
title
description
release_date
genre
cover_image
created_at
updated_at
```

---

### LibraryEntry

Representa a relação entre usuário e jogo na biblioteca.

```
id (PK)
user_id (FK)
game_id (FK)
status
progress
added_at
updated_at
```

---

### Review

Representa uma avaliação feita por um usuário sobre um jogo.

```
id (PK)
user_id (FK)
game_id (FK)
rating
comment
created_at
updated_at
```

Observacao:

- Um mesmo usuario pode registrar varias reviews para o mesmo jogo ao longo do tempo.
- A interface principal mostra apenas a review mais recente de cada usuario.

---

### GameList

Representa listas personalizadas criadas por um usuário.

```
id (PK)
user_id (FK)
name
description
is_public
created_at
updated_at
```

---

### GameListItem

Representa os jogos contidos em uma lista.

```
id (PK)
game_list_id (FK)
game_id (FK)
added_at
```

---

### UserEmailVerification

Representa o estado de verificacao do email atual do usuario.

```
id (PK)
user_id (FK / one-to-one)
is_verified
verified_at
last_verification_email_sent_at
```

---

### SteamAccountLink

Representa o vinculo entre um usuario local e uma conta Steam autenticada.

```text
id (PK)
user_id (FK / one-to-one)
steam_id
persona_name
profile_url
avatar_url
created_at
last_login_at
last_library_sync_at
```

---

### UserProfile

Representa dados locais complementares do perfil do usuario.

```text
id (PK)
user_id (FK / one-to-one)
avatar
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
- Um **User** pode possuir uma **SteamAccountLink** (1:1)
- Um **User** pode possuir um **UserProfile** (1:1)

---

## Caracterização como Aplicação Transacional

O sistema permite realizar operações **CRUD** sobre os principais recursos da aplicação:

- Usuários
- Jogos
- Entradas na biblioteca
- Avaliações
- Listas personalizadas
- Vinculos com Steam
- Perfil local do usuario

Essas operações caracterizam o **GameVault como uma aplicação web transacional**, utilizando banco de dados relacional para persistência das informações.

## Como Rodar o Projeto

Atualmente o projeto esta configurado para ser executado no **Windows PowerShell** usando o ambiente virtual local `.venv`.

### 1. Abrir a pasta do projeto

```powershell
cd "C:\Projetos\ProgramacaoWeb\Trabalhos\1Trabalho\projeto-web-semestre-gamevault"
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

Antes de subir o servidor pela primeira vez, aplique as migracoes, carregue os jogos iniciais e crie o superusuario de demonstracao:

```powershell
python .\manage.py migrate
python .\manage.py seed_games
python .\manage.py create_demo_superuser
```

Opcionalmente, se quiser usar os fluxos com Steam e envio real de email, configure as variaveis de ambiente do arquivo `.env` antes de executar o servidor.

Credenciais padrao do admin de demonstracao:

```text
usuario: admin
senha: admin123
```

Ao rodar `python manage.py create_demo_superuser`, o projeto tambem prepara um exemplo visual para demonstracao:

- `Cyberpunk 2077` adicionado a biblioteca do usuario `admin`
- status `playing`
- progresso `45%`
- review de exemplo cadastrada para o mesmo jogo

## Observacoes Tecnicas Relevantes

- O catalogo tenta usar a Steam como fonte principal de descoberta em `game_catalog_view`.
- Se a consulta externa falhar, a aplicacao cai para o banco local sem quebrar a pagina.
- O login local aceita `username` ou `email`.
- O projeto tambem possui login com Steam via OpenID e sincronizacao opcional da biblioteca possuida.
- As reviews sao historicas: uma nova avaliacao nao apaga automaticamente as anteriores.

```powershell
python .\manage.py runserver
```

Se preferir, tambem e possivel rodar sem ativar o ambiente virtual:

```powershell
.\.venv\Scripts\python.exe .\manage.py runserver
```

### 4. Acessar no navegador

Depois de iniciar o servidor, abrir:

```text
http://127.0.0.1:8000/
```

### 5. Verificar se o projeto esta correto

Para validar a configuracao do Django:

```powershell
python .\manage.py check
```

### 6. Acessar o Django Admin

Abra a rota abaixo e entre com o superusuario de demonstracao:

```text
http://127.0.0.1:8000/admin/
```

## LINK FIGMA: https://www.figma.com/design/eSWG1sVcLrNMDDuWZRtGVx/GameValt?node-id=0-1&t=QbiYw86OHCeU2THv-1
