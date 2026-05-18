---
title: Entrega Final - Alternativa A
aliases:
  - Plano da Entrega Final
  - Entrega Final GameVault
tipo: planejamento
status: ativo
area: planejamento
projeto: GameVault
tags:
  - gamevault
  - entrega-final
  - planejamento
  - django
---

# Entrega Final - Alternativa A

Esta nota consolida o plano da entrega final do [[GameVault]] com base nas diretrizes do PDF da disciplina.

## Decisao Principal

Alternativa escolhida: **Alternativa A - Fullstack Django**.

Motivos:

- O projeto ja segue arquitetura Django MPA com renderizacao no servidor.
- A estrutura atual ja possui `models`, `views`, `urls`, `templates` e arquivos estaticos.
- Evita criar um front-end separado em React/Vite ou Next.js nesta fase.
- Mantem o escopo mais simples, demonstravel e alinhado com as decisoes registradas em [[Decisoes Tecnicas]].

## Criterios Da Entrega

| Criterio | Valor | Como o projeto vai atender |
| --- | ---: | --- |
| ORM e Admin | 2,0 | Configurar models no Django Admin e dados iniciais. |
| CRUD | 2,0 | Implementar CRUD principal de `LibraryEntry`, a biblioteca do usuario. |
| Autenticacao | 2,0 | Validar cadastro, login, logout e rotas protegidas. |
| Apresentacao | 4,0 | Demonstrar models, fluxo funcional, dificuldades e responsabilidades. |

## Escopo Oficial

### Dentro do escopo

- Validar e corrigir [[Autenticacao]].
- Configurar Django Admin para os principais models.
- Criar ou padronizar dados iniciais para o [[Catalogo de Jogos]].
- Fechar o CRUD de [[Biblioteca do Usuario]] usando `LibraryEntry`.
- Manter [[Catalogo de Jogos]] como entrada principal para adicionar jogos.
- Manter avaliacoes como funcionalidade secundaria.
- Documentar fluxo final para apresentacao.

### Fora do escopo desta entrega

- Criar front-end separado com React, Vite ou Next.js.
- Criar telas completas para `GameList` e `GameListItem`.
- Trocar o `User` padrao do Django por usuario customizado.
- Transformar todos os endpoints JSON em API REST completa.

## Recurso Principal Do CRUD

Recurso escolhido: `LibraryEntry`.

Nome funcional: **Biblioteca do Usuario**.

Justificativa:

- Representa a relacao entre usuario autenticado e jogo salvo.
- Faz sentido direto com a proposta do GameVault.
- Ja existe no model e tem views parcialmente implementadas.
- Permite demonstrar Create, Read, Update e Delete de forma clara.

CRUD esperado:

| Operacao | Fluxo |
| --- | --- |
| Create | Usuario adiciona um jogo do catalogo a propria biblioteca. |
| Read | Usuario visualiza os jogos salvos em `/library/`. |
| Update | Usuario altera o status do jogo salvo. |
| Delete | Usuario remove jogo da biblioteca. |

## Parte 1 - Base Tecnica

- [x] Confirmar ambiente virtual do projeto.
- [x] Rodar `python manage.py check`.
- [x] Rodar `python manage.py migrate`.
- [x] Confirmar que o servidor inicia com `python manage.py runserver`.
- [x] Confirmar que `/`, `/catalog/`, `/login/`, `/register/` e `/admin/` abrem corretamente.
- [x] Definir estrategia de dados iniciais: usar `seed_games.py`; `db.sqlite3` fica como banco local de demonstracao.

Observacao da revisao:

- `python3 manage.py check` e `python3 manage.py migrate --plan` nao puderam ser validados no shell do assistente porque o pacote `django` nao esta instalado nesse ambiente.
- Comandos de ambiente marcados como concluidos por validacao manual no ambiente local do projeto.

## Parte 2 - Autenticacao

- [x] Testar cadastro em `/register/`.
- [x] Confirmar que o cadastro cria usuario real no banco.
- [x] Corrigir exibicao dos erros reais no formulario de cadastro.
- [x] Ajustar labels e placeholders dos formularios de login/cadastro.
- [x] Testar login em `/login/`.
- [x] Confirmar que a navbar muda quando `user.is_authenticated` e verdadeiro.
- [x] Testar logout em `/logout/` no navegador.
- [x] Testar acesso protegido a `/library/` sem login.
- [x] Corrigir redirecionamento de `/accounts/login/` para a rota `core:login`.
- [x] Confirmar que login com `next=/library/` retorna para a biblioteca.
- [x] Confirmar mensagens de erro e sucesso.

Critério de pronto:

- [x] Um usuario novo consegue se cadastrar, entrar, acessar a biblioteca e sair.

## Parte 3 - ORM, Admin E Dados

- [x] Registrar `Game` no Django Admin.
- [x] Registrar `LibraryEntry` no Django Admin.
- [x] Registrar `Review` no Django Admin.
- [x] Registrar `GameList` no Django Admin.
- [x] Registrar `GameListItem` no Django Admin.
- [x] Configurar `list_display` nos admins principais.
- [x] Configurar `search_fields` para facilitar demonstracao.
- [x] Configurar `list_filter` para status, genero e usuario quando fizer sentido.
- [x] Criar superusuario para demonstracao.
- [x] Definir dados iniciais: usar o script `seed_games.py` no estado atual.
- [x] Documentar comando para carregar jogos iniciais.

Comando para carregar jogos iniciais:

```bash
python manage.py migrate
python seed_games.py
```

Observacao da revisao:

- O banco local possui superusuario `admin` confirmado em `db.sqlite3`.

Critério de pronto:

- [x] O admin mostra os models principais e permite consultar os dados do projeto.

## Parte 4 - CRUD Da Biblioteca

- [x] Validar adicao de jogo a biblioteca pelo detalhe do jogo.
- [x] Substituir o `prompt()` nativo usado ao adicionar jogo por um modal visual.
- [x] Criar modal de adicionar a biblioteca no detalhe do jogo.
- [x] Permitir escolher status inicial pelo modal.
- [x] Enviar status escolhido para `addToLibrary(gameId, status)`.
- [x] Atualizar [[Catalogo de Jogos]] para remover referencia ao `prompt`.
- [x] Garantir que `add_to_library_view` use metodo POST.
- [x] Validar listagem em `/library/` no navegador.
- [x] Criar interface para editar `status`.
- [x] Integrar edicao com `update_library_entry_view`.
- [x] Validar remocao com `remove_from_library_view` no navegador.
- [x] Garantir que todas as operacoes usam `request.user` para proteger dados.
- [x] Revisar mensagens de erro dos endpoints JSON.

Critério de pronto:

- [x] Usuario logado consegue adicionar, visualizar, editar e remover jogos da propria biblioteca.

Observacao da revisao:

- Adicao foi validada com todos os status.
- Listagem em `/library/` foi validada visualmente.
- Edicao altera apenas status, conforme decisao atual do produto.
- Remocao validada no navegador.

## Parte 5 - Avaliacoes

As avaliacoes serao tratadas como funcionalidade secundaria, pois o CRUD principal sera `LibraryEntry`.

- [x] Validar envio de avaliacao no detalhe do jogo.
- [x] Validar exibicao de avaliacoes.
- [x] Confirmar que apenas usuario logado pode avaliar.
- [x] Confirmar que uma nova avaliacao do mesmo usuario atualiza a anterior.
- [x] Melhorar feedback visual do modal de avaliacao.

Observacao da revisao:

- O envio de avaliacao foi validado no detalhe do jogo.
- A exibicao de avaliacoes foi revisada no detalhe do jogo.
- Uma nova avaliacao do mesmo usuario sobrescreve a anterior, conforme regra atual.
- O modal de avaliacao recebeu fundo opaco e feedback visual inline para reduzir dependencias de popup nativo.

## Parte 6 - Interface E Fluxo De Demonstracao

- [x] Revisar tela de login.
- [x] Revisar tela de cadastro.
- [x] Revisar catalogo.
- [x] Revisar detalhe do jogo.
- [x] Revisar biblioteca.
- [x] Validar responsividade das telas principais.
- [x] Trocar boa parte de `alert` e `prompt` por componentes visuais.
- [x] Garantir consistencia entre paginas demonstrativas e telas dinamicas reais.
- [x] Implementar [[Spec - Email Verificacao e Reset de Senha]].

## Parte 7 - Documentacao E Apresentacao

- [x] Atualizar [[Pendencias]] conforme as tarefas forem concluídas.
- [x] Atualizar [[Views e URLs]] se alguma rota mudar.
- [x] Atualizar [[Biblioteca do Usuario]] se o fluxo de edicao mudar.
- [x] Atualizar [[Autenticacao]] se houver ajuste de login/cadastro.
- [ ] Criar roteiro de apresentacao.
- [ ] Listar responsabilidades dos integrantes.
- [x] Registrar dificuldades tecnicas encontradas em [[Dificuldades Tecnicas]].
- [ ] Registrar pontos implementados que nao foram vistos em aula.

## Roteiro Sugerido Para Apresentacao

1. Apresentar o objetivo do [[GameVault]].
2. Explicar a escolha pela Alternativa A.
3. Mostrar os principais models em [[Models]].
4. Abrir o Django Admin e mostrar os dados.
5. Cadastrar ou logar usuario.
6. Abrir o catalogo.
7. Adicionar jogo a biblioteca.
8. Abrir a biblioteca do usuario.
9. Editar status na biblioteca.
10. Remover jogo da biblioteca.
11. Mostrar avaliacao no detalhe do jogo.
12. Encerrar explicando dificuldades e decisoes tecnicas.

## Ordem Recomendada De Execucao

1. Corrigir e validar autenticacao.
2. Configurar Django Admin.
3. Definir dados iniciais.
4. Fechar CRUD de `LibraryEntry`.
5. Validar avaliacoes.
6. Ajustar interface.
7. Atualizar documentacao.
8. Testar fluxo completo da apresentacao.

## Notas Relacionadas

- [[GameVault]]
- [[Autenticacao]]
- [[Biblioteca do Usuario]]
- [[Catalogo de Jogos]]
- [[Models]]
- [[Views e URLs]]
- [[Decisoes Tecnicas]]
- [[Pendencias]]
