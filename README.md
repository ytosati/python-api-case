# Python API Case - Gerenciador de Tarefas

Estudo de Api Restful desenvolvida com **FastAPI** e **MongoDB** que gera e gerencia tasks cadastradas pelo usuário de forma segura, performática e pronta para integração com Front-End.

O objetivo deste projeto é fornecer um sistema simples de gerenciamento de tarefas (tasks) onde cada usuário tem acesso privado aos seus próprios dados.

## 📋 Funcionalidades

- **Autenticação JWT:** Sistema de Login seguro. O usuário recebe um Token de acesso.
- **Segurança:** Senhas são salvas criptografadas (Hash) no banco de dados.
- **CRUD de Tarefas:**
  - Criar tarefas.
  - Listar apenas as tarefas do usuário logado.
  - Atualizar e Deletar tarefas (apenas se for o dono).
- **Banco de Dados NoSQL:** Persistência de dados utilizando MongoDB.
- **CORS Configurado:** Pronto integração e recebimento de requisições Front-end

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10
- **Framework:** FastAPI
- **Servidor:** Uvicorn
- **Banco de Dados:** MongoDB
- **Driver de Banco:** Motor (AsyncIO)
- **Segurança:** Bcrypt (Hash) e Python-Jose (JWT)
- **Validação:** Pydantic

## ⚙️ Pré-requisitos

1. **Python 3.10 ou superior**: [Download aqui](https://www.python.org/downloads/)
2. **MongoDB Community Server**: [Download aqui](https://www.mongodb.com/try/download/community)
   * Certifique-se de que o serviço do MongoDB está rodando na porta padrão `27017`.

## 🚀 Instalação e Execução

### 1. Clonar o repositório

```bash
git clone https://github.com/ytosati/python-api-case.git
cd python-api-case
```

### 2. Criação e ativação o ambiente virtual (venv)


* **Windows:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate
  ```

* **Mac/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalação de dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o Servidor

Com o ambiente virtual ativo e o MongoDB rodando, execute:

```bash
uvicorn main:app --reload
```

Mensagem de execução bem sucedida no terminal:
`INFO: Uvicorn running on http://127.0.0.1:8000`

## 📖 Documentação e guia da API

Swagger do projeto

* **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**


### Métodos da API:
 
  É necessário utilizar o bearer token para todas as operações com a task. As alterações serão aplicadas apenas ao usuário que gerou o bearer token, e está portanto logado e autenticado.

#### 1. Create User
* **POST** `http://127.0.0.1:8000/create`.

Body
```json
{
    "name": "joao",
    "email": "joao@outlook.com",
    "password": "senhadojoao"
}
```

#### 2. Get Token
* **POST** `http://127.0.0.1:8000/login`.

Body
```json
{
    "email": "joao@outlook.com",
    "password": "senhadojoao"
}
```

#### 3. Create Task
* **POST** `http://127.0.0.1:8000/task`.

Body
```json
{
    "title": "Título da task",
    "description": "Descrição da task"
}
```
#### 4. List Tasks
* **GET** `http://127.0.0.1:8000/task`.

Não há body, a lista é retornada de acordo com o bearer token

#### 5. Update Tasks
* **PUT** `http://127.0.0.1:8000/task/{TaskID}`.

Body
```json
{
    "title": "Título alterado",
    "description": "Descrição alterada"
}
```
#### 5. Delete Tasks
* **DELETE** `http://127.0.0.1:8000/task/{TaskID}`.

Não há body, a lista é retornada de acordo com o bearer token no endpoint

## 📂 Estrutura do Projeto

O projeto foi separado em arquivos com responsabilidades únicas:

* `main.py`: Contém as rotas, Chamadas das funções, injeção de dependências e configurações gerais da aplicação.
* `models.py`: Define os dados de request e response.
* `database.py`: Gerencia a conexão com o MongoDB e define as colections.
* `security.py`: Contém a lógica de Hashing das senhas e geração/validação de Tokens JWT.

## 🔧 Variáveis de Ambiente e Configurações

Atualmente por se tratar de um projeto de estudo, as configurações de banco (`localhost`) e chaves de segurança (`key`) estão fixas no código.
