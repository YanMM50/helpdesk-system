# Arquitetura do Sistema — Help Desk

## 1. Visão Geral

O sistema utiliza uma **arquitetura em 3 camadas** (three-tier architecture), padrão amplamente adotado na indústria. Cada camada tem uma responsabilidade única e se comunica somente com a camada adjacente.

```
┌─────────────────────────────────────────┐
│         CAMADA 1 — FRONTEND             │
│   HTML + CSS + JavaScript (Vanilla)     │
│   Responsável pela interface do usuário │
└────────────────┬────────────────────────┘
                 │  HTTP REST (JSON)
                 ▼
┌─────────────────────────────────────────┐
│         CAMADA 2 — BACKEND              │
│         Python + FastAPI                │
│   Responsável pela lógica de negócio    │
│   e segurança                           │
└────────────────┬────────────────────────┘
                 │  SQL (SQLAlchemy ORM)
                 ▼
┌─────────────────────────────────────────┐
│         CAMADA 3 — BANCO DE DADOS       │
│              PostgreSQL                 │
│   Responsável pelo armazenamento        │
│   persistente dos dados                 │
└─────────────────────────────────────────┘
```

### Por que essa arquitetura?

- **Separação de responsabilidades**: cada camada faz apenas o que é de sua competência
- **Manutenibilidade**: é possível trocar o frontend sem mexer no backend
- **Escalabilidade**: o backend pode ser replicado horizontalmente
- **Segurança**: a lógica de negócio fica protegida no servidor, não exposta ao cliente
- **Testabilidade**: cada camada pode ser testada de forma independente

---

## 2. Stack Tecnológica

| Componente       | Tecnologia             | Justificativa                                           |
|-----------------|------------------------|---------------------------------------------------------|
| Backend          | Python 3.11 + FastAPI  | Moderno, rápido, auto-documentação via OpenAPI/Swagger  |
| ORM              | SQLAlchemy 2.0         | Abstração do banco, proteção contra SQL Injection       |
| Autenticação     | JWT (python-jose)      | Stateless, escalável, padrão da indústria               |
| Hash de senhas   | bcrypt (passlib)       | Algoritmo seguro para armazenamento de senhas           |
| Banco de Dados   | PostgreSQL (Supabase)  | Cloud gerenciado, ACID, gratuito, acesso via IPv4       |
| Frontend         | HTML5 + CSS3 + JS ES6  | Sem frameworks, ideal para aprendizado                  |
| Servidor ASGI    | Uvicorn                | Alta performance para APIs assíncronas                  |
| Hospedagem API   | Render.com (Free Tier) | Deploy automático via GitHub, HTTPS incluído            |
| Controle de vers.| Git + GitHub           | Padrão da indústria para versionamento                  |

---

## 3. Estrutura de Pastas

```
projeto-helpdesk/
│
├── backend/                    # Servidor da API
│   ├── app/
│   │   ├── main.py             # Ponto de entrada da aplicação
│   │   ├── config.py           # Configurações centralizadas
│   │   ├── database.py         # Conexão com o banco de dados
│   │   │
│   │   ├── models/             # Modelos do banco (SQLAlchemy)
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   ├── equipment.py
│   │   │   └── ticket.py       # Ticket, TicketHistory, Attachment
│   │   │
│   │   ├── schemas/            # Contratos da API (Pydantic)
│   │   │   ├── user.py
│   │   │   ├── company.py
│   │   │   └── ticket.py
│   │   │
│   │   ├── routers/            # Endpoints HTTP organizados por domínio
│   │   │   ├── auth.py         # Login, /me
│   │   │   ├── users.py        # CRUD usuários
│   │   │   ├── companies.py    # Empresas e Equipamentos
│   │   │   ├── tickets.py      # Chamados (lógica principal)
│   │   │   └── dashboard.py    # Estatísticas
│   │   │
│   │   ├── services/
│   │   │   └── auth_service.py # Dependency injection de autenticação
│   │   │
│   │   └── utils/
│   │       └── security.py     # Hash e JWT
│   │
│   ├── uploads/                # Arquivos enviados pelos usuários
│   ├── requirements.txt        # Dependências Python
│   ├── .env.example            # Template de variáveis de ambiente
│   └── run.py                  # Script para iniciar o servidor
│
├── frontend/                   # Interface do usuário
│   ├── index.html              # Tela de login (com background blur)
│   ├── cadastro.html           # Cadastro público de clientes
│   ├── dashboard.html          # Painel principal
│   ├── tickets.html            # Lista de chamados
│   ├── ticket-detail.html      # Detalhes + ações do chamado
│   ├── new-ticket.html         # Formulário de abertura (com upload de fotos)
│   ├── equipments.html         # Gestão de equipamentos
│   ├── companies.html          # Gestão de empresas
│   ├── users.html              # Gestão de usuários (admin) com edição
│   ├── css/
│   │   └── style.css           # Estilos globais
│   ├── img/
│   │   ├── help-desk.png       # Ícone do sistema (sidebar e favicon)
│   │   └── background helpdesk.jpg  # Imagem de fundo das telas de login
│   └── js/
│       ├── api.js              # Camada de comunicação com a API
│       └── utils.js            # Funções utilitárias e autenticação
│
├── database/
│   └── schema.sql              # Script SQL completo
│
├── docs/
│   ├── arquitetura.md          # Este documento
│   ├── plano-manutencao.md     # Plano de manutenção
│   └── manual-usuario.md       # Manual do usuário
│
└── README.md                   # Guia principal do projeto
```

---

## 4. Modelo de Dados (Diagrama ER)

```
COMPANIES ──────────────────────────────────────┐
│ id (PK)                                        │
│ nome                                           │
│ cnpj, telefone, email, endereco                │
│ ativo, criado_em                               │
└──────┬────────────────────────────────────────┘
       │ 1:N                    │ 1:N
       ▼                        ▼
USERS                     EQUIPMENTS
│ id (PK)                  │ id (PK)
│ nome, email              │ nome, tipo, modelo
│ senha_hash               │ numero_serie
│ nivel_suporte (ENUM)     │ company_id (FK)
│ tipo_usuario (ENUM)      │ responsavel_id (FK)
│ cargo, ativo             │ ativo
│ company_id (FK) ─────────┘
└──────┬──────────────────────────────┐
       │ 1:N (solicitante)            │ 1:N (tecnico)
       ▼                              ▼
             TICKETS
             │ id (PK)
             │ protocolo (UNIQUE)
             │ titulo, descricao
             │ prioridade (ENUM)
             │ status (ENUM)
             │ nivel_atual (ENUM)
             │ solicitante_id (FK → users)
             │ tecnico_id (FK → users)
             │ company_id (FK)
             │ equipamento_id (FK)
             │ data_abertura, data_fechamento
             └──────┬──────────────┬──────────
                    │ 1:N          │ 1:N
                    ▼              ▼
            TICKET_HISTORY    ATTACHMENTS
            │ id (PK)          │ id (PK)
            │ ticket_id (FK)   │ ticket_id (FK)
            │ usuario_id (FK)  │ usuario_id (FK)
            │ tipo_acao        │ nome_original
            │ comentario       │ nome_arquivo
            │ nivel_anterior   │ tipo_mime
            │ nivel_novo       │ tamanho_bytes
            │ status_anterior  │ caminho
            │ status_novo      └──────────────
            └──────────────────
```

---

## 5. Fluxo de Autenticação (JWT)

O sistema possui dois fluxos de entrada distintos conforme o tipo de usuário:

### 5.1 Login (Colaboradores e Clientes existentes)

```
Frontend                    Backend
   │                           │
   │──── POST /auth/login ────►│
   │     {email, senha}        │
   │                           │── Verifica email no banco
   │                           │── Compara hash bcrypt
   │                           │── Gera token JWT
   │◄─── {access_token,        │
   │       usuario} ───────────│
   │                           │
   │ (armazena no localStorage)│
   │                           │
   │ Se tipo_usuario=CLIENTE → redireciona para tickets.html
   │ Se tipo_usuario=COLABORADOR → redireciona para dashboard.html
```

### 5.2 Cadastro Público (Apenas Clientes)

```
Frontend (cadastro.html)     Backend
   │                           │
   │── POST /auth/register ───►│
   │   {nome, email, senha}    │
   │                           │── Cria usuário com:
   │                           │   tipo_usuario = CLIENTE
   │                           │   nivel_suporte = N1
   │◄── {access_token} ────────│
   │                           │
   │ Redireciona para tickets.html
```

> Colaboradores (N1/N2/N3/ADMIN) só podem ser criados pelo administrador via painel de usuários — nunca pelo cadastro público.

**Por que JWT?**
- O servidor não precisa armazenar sessões (stateless)
- O token contém as informações do usuário de forma segura
- Cada requisição é independente, facilitando escalabilidade
- O token expira automaticamente após o tempo configurado

---

## 6. Fluxo de um Chamado (N1 → N2 → N3)

```
SOLICITANTE                N1               N2               N3
    │                       │                │                │
    │── Abre chamado ──────►│                │                │
    │   Status: ABERTO      │                │                │
    │                       │                │                │
    │                       │── Triagem ─────│                │
    │                       │   Problema     │                │
    │                       │   simples?     │                │
    │                       │                │                │
    │                       │── Se SIM: resolve e fecha       │
    │                       │                │                │
    │                       │── Se NÃO: encaminha para N2 ──►│
    │                       │   Status: EM_ANALISE            │
    │                       │                │                │
    │                       │                │── Diagnóstico  │
    │                       │                │   avançado     │
    │                       │                │                │
    │                       │                │── Se resolve: fecha
    │                       │                │                │
    │                       │                │── Se NÃO: encaminha ──►│
    │                       │                │   Status: EM_ATENDIMENTO
    │                       │                │                │
    │                       │                │                │── Engenharia
    │                       │                │                │   Correção
    │                       │                │                │   estrutural
    │                       │                │                │
    │◄─────────────────── RESOLVIDO ─────────────────────────│
    │   Solicitante confirma ou é fechado automaticamente     │
```

**Registro em cada etapa:** toda ação (abertura, comentário, encaminhamento, mudança de status) é registrada automaticamente na tabela `ticket_history`, formando uma trilha de auditoria completa e imutável.

---

## 7. Segurança Implementada

| Mecanismo              | Onde              | Por quê                                               |
|------------------------|-------------------|-------------------------------------------------------|
| bcrypt (rounds=12)     | Senhas            | Resistente a ataques de força bruta                   |
| JWT com expiração      | Autenticação      | Tokens expirados são inválidos automaticamente        |
| HTTPS (produção)       | Transporte        | Criptografa toda a comunicação                        |
| ORM + Pydantic         | Queries           | Previne SQL Injection                                 |
| Soft delete            | Exclusão de dados | Registros nunca são apagados, apenas desativados      |
| Controle por nível     | Autorização       | N1 vê apenas seus chamados; Admin vê tudo             |
| Validação de upload    | Arquivos          | Apenas extensões e tamanhos permitidos                |
| UUID em uploads        | Nomes de arquivo  | Impede sobrescrita e path traversal                   |
| .env para secrets      | Configuração      | Credenciais nunca no código-fonte                     |

---

## 8. Conformidade com Normas ISO

### ISO/IEC 12207 — Ciclo de Vida do Software
Define processos para aquisição, fornecimento, desenvolvimento e manutenção.
- **Aplicação no projeto**: o desenvolvimento seguiu as fases de levantamento de requisitos, análise, projeto, implementação e teste. A documentação técnica e o plano de manutenção formalizam o processo de suporte pós-entrega.

### ISO/IEC 14764 — Manutenção de Software
Define tipos e processos de manutenção.
- **Aplicação no projeto**: o Plano de Manutenção detalha as quatro categorias (corretiva, adaptativa, evolutiva e preventiva) com procedimentos e calendário.

### ISO/IEC 9126 — Qualidade de Software
Define características de qualidade: funcionalidade, confiabilidade, usabilidade, eficiência, manutenibilidade e portabilidade.
- **Aplicação no projeto**:
  - *Funcionalidade*: todos os requisitos levantados foram implementados
  - *Confiabilidade*: histórico imutável, soft delete, backups diários
  - *Usabilidade*: interface intuitiva, mensagens de erro claras, badges coloridos
  - *Eficiência*: índices no banco, pool de conexões, queries otimizadas
  - *Manutenibilidade*: código modularizado, comentado e com separação de camadas
  - *Portabilidade*: funciona em qualquer SO com Python e PostgreSQL

### ISO/IEC 20000 — Gestão de Serviços de TI
Alinha com as melhores práticas de gerenciamento de serviços (próximo ao ITIL).
- **Aplicação no projeto**: o sistema implementa gestão de incidentes, controle de SLA, fluxo de escalação (N1→N2→N3) e registro de histórico — todos alinhados à norma.

---

## 9. Infraestrutura em Nuvem (Produção)

O sistema é hospedado inteiramente em serviços gratuitos de nuvem, tornando-o acessível de qualquer lugar sem custo:

```
┌─────────────────────────────────────────────────────────┐
│                   INTERNET                              │
└───────────┬─────────────────────────┬───────────────────┘
            │                         │
            ▼                         ▼
┌───────────────────────┐   ┌─────────────────────────────┐
│   GitHub Pages /      │   │       Render.com             │
│   Netlify             │   │   (Web Service — Free)       │
│                       │   │                             │
│   Frontend estático   │   │   FastAPI + Uvicorn          │
│   HTML + CSS + JS     │◄──│   Python 3.11               │
│                       │   │   Branch: PROD              │
└───────────────────────┘   └──────────────┬──────────────┘
                                           │ SQL (TLS)
                                           ▼
                            ┌─────────────────────────────┐
                            │         Supabase            │
                            │  PostgreSQL (Cloud)         │
                            │  Session Pooler (IPv4)      │
                            │  São Paulo — sa-east-1      │
                            └─────────────────────────────┘
```

### Branches e Ambientes

| Branch    | Ambiente     | Descrição                              |
|-----------|--------------|----------------------------------------|
| DEVELOP   | Local        | Desenvolvimento e testes locais        |
| PROD      | Render.com   | Produção — deploy automático via push  |

### Considerações do Plano Gratuito (Render)

- A instância "dorme" após 15 minutos sem requisições
- A primeira requisição após inatividade pode demorar ~30-50 segundos (cold start)
- Para uso acadêmico/demonstração isso é aceitável
- Upgrade para plano pago elimina o cold start em ambientes profissionais
