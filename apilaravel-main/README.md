# API de Gerenciamento de Biblioteca

API desenvolvida como parte de um projeto de pós-graduação, utilizando o framework Laravel. O objetivo é gerenciar os recursos de uma biblioteca, como livros, autores e empréstimos, seguindo uma arquitetura de software robusta e documentando todos os endpoints.

## Tecnologias e Padrões Utilizados

- **Framework:** Laravel 9
- **Linguagem:** PHP 8.1
- **Autenticação:** JWT (JSON Web Tokens) com o pacote `tymon/jwt-auth`.
- **Documentação da API:** OpenAPI (Swagger) com o pacote `darkaonline/l5-swagger`.
- **Banco de Dados:** MySQL/MariaDB
- **Arquitetura:** Padrão em camadas (Controller, Service, Repository, Resource) para separação de responsabilidades.

## Funcionalidades

- Autenticação de usuários com JWT.
- CRUD completo para **Livros**.
- CRUD completo para **Autores**.
- Relacionamento entre os modelos: `User`, `Autor`, `Livro`, `Categoria` e `Emprestimo`.
- Job em segundo plano (`VerificarEmprestimosAtrasados`) para identificar empréstimos com devolução atrasada.
- Seeders para popular o banco de dados com dados de teste, incluindo um usuário administrador.

## Pré-requisitos

- [PHP](https://www.php.net/downloads.php) >= 8.1
- [Composer](https://getcomposer.org/download/)
- Um servidor de banco de dados (MySQL/MariaDB). Recomenda-se o uso do [XAMPP](https://www.apachefriends.org/index.html) para um ambiente de desenvolvimento local completo.

## Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd apilaravel
    ```

2.  **Instale as dependências:**
    ```bash
    composer install
    ```

3.  **Configure o ambiente:**
    - Copie o arquivo de exemplo `.env.example` para `.env`.
    ```bash
    copy .env.example .env
    ```
    - Gere a chave da aplicação:
    ```bash
    php artisan key:generate
    ```
    - Gere o segredo para o JWT:
    ```bash
    php artisan jwt:secret
    ```

4.  **Configure o Banco de Dados:**
    - Abra o arquivo `.env` e configure as credenciais do seu banco de dados:
    ```
    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=3306
    DB_DATABASE=sua_base_de_dados
    DB_USERNAME=seu_usuario
    DB_PASSWORD=sua_senha
    ```

5.  **Execute as Migrations e Seeders:**
    - Este comando irá criar todas as tabelas e popular o banco de dados com dados de teste, incluindo um usuário administrador.
    ```bash
    php artisan migrate --seed
    ```

## Executando a Aplicação

1.  **Inicie o servidor de desenvolvimento:**
    ```bash
    php artisan serve
    ```
    A API estará disponível em `http://127.0.0.1:8000`.

## Documentação e Testes da API

A API está documentada com Swagger e pode ser acessada no seguinte endpoint:

- **URL da Documentação:** [http://127.0.0.1:8000/api/documentation](http://127.0.0.1:8000/api/documentation)

### Autenticação

Para testar os endpoints protegidos, primeiro utilize o endpoint `POST /api/login` para obter um token de acesso.

**Credenciais do usuário administrador (criado pelo seeder):**
- **Email:** `admin@example.com`
- **Senha:** `password`

Após obter o token, clique no botão **"Authorize"** no topo da página do Swagger e insira o token no formato `Bearer seu_token_aqui`.

### Endpoints Disponíveis

- **Autenticação:**
  - `POST /api/login`: Autentica um usuário e retorna um token JWT.
  - `POST /api/logout`: Invalida o token do usuário autenticado.
  - `POST /api/me`: Retorna as informações do usuário autenticado.

- **Livros (`/api/livros`):**
  - `GET /`: Lista todos os livros.
  - `POST /`: Cria um novo livro.
  - `GET /{id}`: Exibe um livro específico.
  - `PUT /{id}`: Atualiza um livro.
  - `DELETE /{id}`: Remove um livro.

- **Autores (`/api/autores`):**
  - `GET /`: Lista todos os autores.
  - `POST /`: Cria um novo autor.
  - `GET /{id}`: Exibe um autor específico.
  - `PUT /{id}`: Atualiza um autor.
  - `DELETE /{id}`: Remove um autor.

## Job em Segundo Plano

O job `VerificarEmprestimosAtrasados` pode ser executado para verificar no banco de dados quais empréstimos estão com a data de devolução ultrapassada. Atualmente, ele apenas registra a informação no log do Laravel.

Para executá-lo manualmente (em um ambiente de produção, isso seria configurado para rodar periodicamente):
```bash
php artisan queue:work
```
E para despachar o job:
```bash
php artisan tinker
> App\Jobs\VerificarEmprestimosAtrasados::dispatch();
```

## Testes Automatizados

O projeto conta com uma suíte de testes automatizados para garantir a integridade e o funcionamento correto das principais funcionalidades da API. Os testes foram desenvolvidos com o PHPUnit, que já vem integrado ao Laravel.

Para executar todos os testes, utilize o seguinte comando na raiz do projeto:
```bash
php artisan test
```

### Testes Implementados

-   **`tests/Feature/Auth/AuthenticationTest.php`**: Testa todo o fluxo de autenticação.
    -   Login de usuário com sucesso.
    -   Falha de login com credenciais incorretas.
    -   Acesso a rotas protegidas com um token válido.
    -   Bloqueio de acesso a rotas protegidas sem um token.
    -   Logout e invalidação do token.

-   **`tests/Feature/Livro/LivroApiTest.php`**: Cobre todas as operações do CRUD de Livros.
    -   Listagem de todos os livros.
    -   Criação de um novo livro.
    -   Visualização de um livro específico.
    -   Atualização de um livro existente.
    -   Exclusão de um livro.
