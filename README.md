# 📊 **Gerenciador Financeiro - Receitas & Despesas**

**Tecnologias**: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT

---

## 💡 **Visão Geral**

O **Gerenciador Financeiro** é um sistema desenvolvido com foco no controle e gerenciamento de receitas e despesas, ideal para quem quer manter o fluxo de caixa em dia. Ele oferece funcionalidades para **criar, listar, atualizar, deletar e buscar** receitas e despesas de forma simples e eficiente, tudo em uma API RESTful construída com **FastAPI** e armazenado em um banco de dados **PostgreSQL**.

Foi desenvolvido como parte do meu estudo prático em **Back-end**, e para a participação no **Challenger-Alura**, visando aprimorar minhas habilidades com **APIs**, **frameworks web** e **bancos de dados**.

---

## 🔧 **Tecnologias Usadas**

- **Python**: Linguagem principal do projeto.
- **FastAPI**: Framework de alto desempenho para construção da API.
- **SQLAlchemy**: ORM para integração com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Alembic**: Para controle de versões e migrações de banco de dados.
- **JWT**: Utilizado para autenticação e controle de sessões de usuários.

---

## 🚀 **Funcionalidades**

- **Cadastro de Despesas e Receitas**: Adicione suas despesas e receitas facilmente.
- **Listagem**: Visualize suas despesas e receitas em uma lista filtrada por descrição.
- **Busca por ID**: Consulte uma despesa ou receita específica pelo ID.
- **Edição e Deleção**: Modifique ou exclua despesas e receitas com facilidade.
- **Resumo Financeiro Mensal**: Obtenha um resumo detalhado de receitas e despesas por mês.
- **Autenticação JWT**: Acesso seguro com token JWT para garantir que apenas usuários autenticados possam interagir com o sistema.

---

## ⚙️ **Como Usar**

1. Clone o repositório:
   git clone https://github.com/seu-usuario/gerenciador-financeiro.git 
2. Instale as dependências:
    pip install -r requirements.txt
3. Configure seu banco de dados PostgreSQL e crie as tabelas com Alembic:
    alembic upgrade head
4. Execute a aplicação:
    uvicorn app.main:app --reload

## 🛠️ **EndPoints da API**

**Despesas**
- *POST* /despesas/criar: Cria uma nova despesa.
- *GET* /despesas/listar/: Lista todas as despesas ou busca por descrição.
- *GET* /despesas/buscar/{despesa_id}: Busca uma despesa por ID.
- *PUT* /despesas/atualizar/{despesa_id}: Atualiza uma despesa existente.
- *DELETE* /despesas/deletar/{despesa_id}: Deleta uma despesa.
- *GET* /despesas/buscar_mes/{ano}/{mes}: Busca despesas de um mês específico.

**Receitas**
- *POST* /receitas/criar: Cria uma nova receita.
- *GET* /receitas/listas/: Lista todas as receitas ou busca por descrição.
- *GET* /receitas/buscar/{receita_id}: Busca uma receita por ID.
- *PUT* /receitas/atualizar/{receita_id}: Atualiza uma receita existente.
- *DELETE* /receitas/deletar/{receita_id}: Deleta uma receita.
- *GET* /receitas/buscar_mes/{ano}/{mes}: Busca receitas de um mês específico.

**Resumo**
- *GET* /resumo/{ano}/{mes}: Obtém um resumo financeiro do mês, somando receitas e despesas.

## 🔑 **Autenticação JWT**
Para acessar as rotas protegidas, é necessário um token JWT.
Utilize as credenciais para obter o token e passá-lo no cabeçalho das requisições:

Authorization: Bearer <seu_token_jwt>

## 📈 **Objetivo do Projeto**
Este projeto tem como principal objetivo consolidar meus conhecimentos em desenvolvimento Back-end, particularmente no uso de FastAPI, SQLAlchemy, PostgreSQL e JWT. Além disso, visa me preparar para desafios práticos, como o Challenger-Alura, com um sistema real de gerenciamento financeiro.