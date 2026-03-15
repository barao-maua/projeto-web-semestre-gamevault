# Entrega 2 - Projeto Inicial

Nesta entrega será avaliado a configuração inicial de um projeto web utilizando o framework **Django**, as **rotas**, **views** e **estrutura das páginas estáticas**.

A entrega será feita no **mesmo repositório da Entrega 1**.  
A entrega será identificada pelo **commit final** ou **pull request**.

---       

## 1. Criar o projeto Django corretamente (1,0)

a. Recomenda-se utilizar o projeto `django-starter` disponível no repositório da disciplina (**repo baraoweb2026**) como padrão, mas se preferir pode iniciar um projeto do zero.

---

## 2. Implementação de páginas HTML e CSS (5,0)

Nesta entrega deverá ser implementado **no mínimo 3 páginas em HTML e CSS** no contexto do projeto.

Todas as páginas devem:

- Estar estruturadas corretamente com **tags estruturais**
- Possuir **pelo menos 1 menu** (possivelmente compartilhado entre elas, se fizer sentido no contexto)

### Exemplos de páginas estáticas
- Home
- Sobre o projeto
- Diferenciais
- Quem somos

### Requisitos desta parte

a. Criar **layout (template base)** e **componentes compartilhados corretamente** (na pasta `components`)  
b. Criar **as rotas e as views** para essas páginas corretamente  
c. Criar **o menu com link correto entre as 3 páginas**  
d. Utilizar **HTML corretamente com alguma tag estrutural/semântica**

---

## 3. Apresentação (4,0)

> Somente ganha essa nota quem **participar da apresentação**.

a. Apresentar a **idéia geral do projeto**  
b. Fazer um **overview das rotas e views** que foram criadas  
c. Explicar **como foi feito o CSS**, se foi utilizado algum **framework** e qual  
d. Explicar **a estrutura do HTML**, quais **tags estruturais/semânticas** foram utilizadas nas páginas e **componentes criados**

---

## Atenção

Podem utilizar alguma **LLM como apoio**, porém o **código gerado precisa ser entendido e explicável**.

Prefiram manter um **código mais simples e direto**, ao invés de algo que **não consigam entender ou explicar**.

---

# Requisitos

- Todos os projetos serão **MPA (Multi Page Applications)** com **server rendering** utilizando o framework **Django**
- Utilizar **HTML e CSS estático nesta entrega**
- Utilizar a **engine de template nativa do Django** ou a biblioteca `django-cotton` presente no projeto `django-starter`
- **Não utilizar frameworks front-end** como:
  - Vue
  - Angular
  - React

### CSS

Pode-se:

- Criar um **CSS próprio**
- Utilizar algum **framework CSS**, como:
  - DaisyUI
  - Bootstrap
  - Semantic
  - Tailwind
  - Materialize

Também é **opcional utilizar algum template pronto** como ponto de partida.

### Javascript

O uso de **JavaScript é opcional**.

---

# Regras de Entrega

A **data da entrega** será considerada a **data do commit** em que os arquivos foram enviados.

Incluir na **mensagem do commit** a palavra:

- `entrega 2`
- ou `E2`

para facilitar a identificação.

Também é possível:

- Criar uma **branch para representar a entrega**
- Fazer um **pull request até a data limite**

---

# Participação da Equipe

Para receber a **nota integral**, **todos os membros da equipe devem participar** com:

- commits próprios  
ou  
- pull requests próprios

---

# Sugestão de Organização

Dividir as tarefas entre os membros da equipe.

Exemplo:

- **Pessoa 1:** configuração inicial do projeto + template base  
- **Pessoa 2:** criação de páginas e rotas  
- **Pessoa 3:** criação de páginas e rotas adicionais