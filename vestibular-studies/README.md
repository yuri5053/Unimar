## **Documentação do Sistema de Simulação de Provas**

### **1. Introdução**

Este sistema foi desenvolvido para oferecer uma plataforma online de simulação de provas como ENEM e vestibulares, proporcionando aos estudantes um ambiente gratuito, acessível e eficiente para praticar seus conhecimentos.

---

### **2. Tecnologias Utilizadas**

#### **2.1 Linguagem de Programação**

* **Backend:** C#

  * Recursos modernos
  * Tipagem estática
  * Integração com o ecossistema .NET
  * Performance robusta e segura

#### **2.2 Frameworks**

* **Backend:** .NET

  * Arquitetura baseada em **DDD (Domain-Driven Design)**
  * Separação clara de responsabilidades
* **Frontend:** React

  * Biblioteca declarativa e eficiente para construção de interfaces modernas
  * Criação de experiências dinâmicas e fluidas para o usuário

#### **2.3 Banco de Dados**

* **SGBD:** MySQL

  * Armazenamento relacional das informações
  * Estrutura de dados normalizada
  * Garantia de integridade e desempenho através de constraints e índices

---

### **3. Arquitetura do Sistema**

#### **3.1 Estilo Arquitetural: DDD**

Separação em quatro camadas principais:

* **Domínio:** Regras de negócio, entidades e agregados.
* **Aplicação:** Serviços que coordenam operações no domínio.
* **Infraestrutura:** Persistência de dados, integração com serviços externos.
* **Apresentação:** Camada web para interação com os usuários.

#### **3.2 Frontend**

* Desenvolvido em **React**.
* Funcionalidades principais:

  * Seleção de provas.
  * Realização e envio de respostas.
  * Visualização de resultados.
  * Uso de componentes reutilizáveis e controle eficiente de estado.

#### **3.3 Backend**

* Desenvolvido em **.NET** com **C#**.
* Responsável por:

  * Lógica de negócios.
  * Autenticação.
  * Correção automática das provas.
  * Exposição de APIs REST.
* Arquitetura DDD mantém o domínio isolado e testável.

---

### **4. Requisitos do Sistema**

#### **4.1 Requisitos Funcionais**

| Nº | Descrição                                          |
| -- | -------------------------------------------------- |
| 01 | Cadastro de usuários.                              |
| 02 | Login com e-mail e senha.                          |
| 03 | Redefinição de senha via e-mail.                   |
| 04 | Escolha de matérias para estudo.                   |
| 05 | Apresentação de questões de múltipla escolha.      |
| 06 | Indicação de respostas corretas ou incorretas.     |
| 07 | Exibição de explicação da resposta correta.        |
| 08 | Favoritar questões para revisão futura.            |
| 09 | Revisão de questões respondidas incorretamente.    |
| 10 | Registro de desempenho por matéria.                |
| 11 | Filtro de questões por nível de dificuldade.       |
| 12 | Seleção de temas ou assuntos específicos.          |
| 13 | Geração de simulados cronometrados.                |
| 14 | Correção automática dos simulados.                 |
| 15 | Exibição de estatísticas de acertos e erros.       |
| 16 | Envio de notificações de lembretes de estudo.      |
| 17 | Definição de metas de estudo semanais ou mensais.  |
| 18 | Exibição de ranking com melhores desempenhos.      |
| 19 | Cadastro e edição de questões por administradores. |
| 20 | Salvamento do progresso de simulados inacabados.   |

---

#### **4.2 Requisitos Não Funcionais**

| Nº | Descrição                                         |
| -- | ------------------------------------------------- |
| 01 | Páginas carregam em até 3 segundos.               |
| 02 | Disponibilidade: 24/7.                            |
| 03 | Responsivo: funciona em celular, tablet e PC.     |
| 04 | Suporte a pelo menos 10.000 usuários simultâneos. |
| 05 | Senhas armazenadas com criptografia.              |
| 06 | Conformidade com a LGPD.                          |
| 07 | Uso de banco de dados relacional.                 |
| 08 | Backups automáticos diários.                      |
| 09 | Conexão segura (HTTPS).                           |
| 10 | Interface amigável, intuitiva e acessível.        |
| 11 | Compatibilidade: Android 8+ e iOS 12+.            |
| 12 | Consumo leve de internet e armazenamento.         |
| 13 | Resposta ao envio inferior a 1 segundo.           |
| 14 | Facilidade de manutenção e atualização.           |
| 15 | Registro de logs de acesso para análise.          |

---

### **5. Banco de dados**

![Schema do banco de dados](database/SCHEMA.png) 

### ** Fluxo previsto:**
#### **5.1 Usuário entra com conta do Google → dados salvos em User.**
#### **5.2 Usuário escolhe matéria → carrega questões de Question filtradas por subject_id.**
#### **5.3 Usuário responde → salva em User_Question_Response.**
#### **5.4 Sistema mostra feedback: acertou ou errou, + explanation da questão.**

---

### **6. Considerações Finais**

Este sistema foi projetado com foco na escalabilidade, segurança, usabilidade e manutenção, utilizando tecnologias modernas e uma arquitetura robusta baseada em DDD. Ele visa proporcionar uma experiência completa para estudantes, administradores e desenvolvedores.

