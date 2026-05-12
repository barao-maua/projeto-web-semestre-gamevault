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
| Update | Usuario altera status e progresso do jogo salvo. |
| Delete | Usuario remove jogo da biblioteca. |

## Parte 1 - Base Tecnica

- [ ] Confirmar ambiente virtual do projeto.
- [ ] Rodar `python manage.py check`.
- [ ] Rodar `python manage.py migrate`.
- [ ] Confirmar que o servidor inicia com `python manage.py runserver`.
- [ ] Confirmar que `/`, `/catalog/`, `/login/`, `/register/` e `/admin/` abrem corretamente.
- [ ] Verificar se `db.sqlite3` sera mantido localmente ou se a entrega dependera de fixtures.

## Parte 2 - Autenticacao

- [ ] Testar cadastro em `/register/`.
- [ ] Confirmar que o cadastro cria usuario real no banco.
- [x] Corrigir exibicao dos erros reais no formulario de cadastro.
- [x] Ajustar labels e placeholders dos formularios de login/cadastro.
- [ ] Testar login em `/login/`.
- [ ] Confirmar que a navbar muda quando `user.is_authenticated` e verdadeiro.
- [ ] Testar logout em `/logout/`.
- [x] Testar acesso protegido a `/library/` sem login.
- [x] Corrigir redirecionamento de `/accounts/login/` para a rota `core:login`.
- [ ] Confirmar que login com `next=/library/` retorna para a biblioteca.
- [ ] Confirmar mensagens de erro e sucesso.

Critério de pronto:

- [ ] Um usuario novo consegue se cadastrar, entrar, acessar a biblioteca e sair.

## Parte 3 - ORM, Admin E Dados

- [ ] Registrar `Game` no Django Admin.
- [ ] Registrar `LibraryEntry` no Django Admin.
- [ ] Registrar `Review` no Django Admin.
- [ ] Registrar `GameList` no Django Admin.
- [ ] Registrar `GameListItem` no Django Admin.
- [ ] Configurar `list_display` nos admins principais.
- [ ] Configurar `search_fields` para facilitar demonstracao.
- [ ] Configurar `list_filter` para status, genero e usuario quando fizer sentido.
- [ ] Criar superusuario para demonstracao.
- [ ] Definir dados iniciais: fixture ou script `seed_games.py`.
- [ ] Documentar comando para carregar jogos iniciais.

Critério de pronto:

- [ ] O admin mostra os models principais e permite consultar os dados do projeto.

## Parte 4 - CRUD Da Biblioteca

- [ ] Validar adicao de jogo a biblioteca pelo detalhe do jogo.
- [ ] Melhorar fluxo de adicionar jogo sem depender de `prompt`, se houver tempo.
- [ ] Garantir que `add_to_library_view` use metodo POST.
- [ ] Validar listagem em `/library/`.
- [ ] Criar interface completa para editar `status` e `progress`.
- [ ] Integrar edicao com `update_library_entry_view`.
- [ ] Validar remocao com `remove_from_library_view`.
- [ ] Garantir que todas as operacoes usam `request.user` para proteger dados.
- [ ] Revisar mensagens de erro dos endpoints JSON.

Critério de pronto:

- [ ] Usuario logado consegue adicionar, visualizar, editar e remover jogos da propria biblioteca.

## Parte 5 - Avaliacoes

As avaliacoes serao tratadas como funcionalidade secundaria, pois o CRUD principal sera `LibraryEntry`.

- [ ] Validar envio de avaliacao no detalhe do jogo.
- [ ] Validar exibicao de avaliacoes.
- [ ] Confirmar que apenas usuario logado pode avaliar.
- [ ] Confirmar que uma nova avaliacao do mesmo usuario atualiza a anterior.
- [ ] Se sobrar tempo, melhorar feedback visual do modal de avaliacao.

## Parte 6 - Interface E Fluxo De Demonstracao

- [ ] Revisar tela de login.
- [ ] Revisar tela de cadastro.
- [ ] Revisar catalogo.
- [ ] Revisar detalhe do jogo.
- [ ] Revisar biblioteca.
- [ ] Validar responsividade das telas principais.
- [ ] Trocar `alert` e `prompt` por componentes visuais, se houver tempo.
- [ ] Garantir consistencia entre paginas demonstrativas e telas dinamicas reais.

## Parte 7 - Documentacao E Apresentacao

- [ ] Atualizar [[Pendencias]] conforme as tarefas forem concluídas.
- [ ] Atualizar [[Views e URLs]] se alguma rota mudar.
- [ ] Atualizar [[Biblioteca do Usuario]] se o fluxo de edicao mudar.
- [ ] Atualizar [[Autenticacao]] se houver ajuste de login/cadastro.
- [ ] Criar roteiro de apresentacao.
- [ ] Listar responsabilidades dos integrantes.
- [ ] Registrar dificuldades tecnicas encontradas.
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
9. Editar status e progresso.
10. Remover jogo da biblioteca.
11. Mostrar avaliacao no detalhe do jogo, se estiver estavel.
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
