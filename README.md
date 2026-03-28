# Sistema de Gestão de Chamados Técnicos — Help Desk

> Projeto acadêmico desenvolvido para o curso técnico em TI (SENAI).
> Sistema completo de gerenciamento de chamados com suporte em três níveis (N1, N2, N3).

---

## Sistema Online (Produção)

| Serviço   | URL                                               |
|-----------|---------------------------------------------------|
| Frontend  | https://strong-kelpie-a93e9c.netlify.app          |
| Backend   | https://helpdesk-system-aodq.onrender.com         |
| API Docs  | https://helpdesk-system-aodq.onrender.com/docs    |

> **Atenção:** O backend usa o plano gratuito do Render e "dorme" após 15 min sem uso.
> A primeira requisição pode demorar ~50 segundos para acordar. Isso é normal.

---

## Credenciais de Acesso (dados iniciais)

| Usuário       | Email                  | Senha     | Nível |
|---------------|------------------------|-----------|-------|
| Administrador | admin@helpdesk.com     | Admin@123 | ADMIN |
| Técnico N1    | joao.n1@helpdesk.com   | Admin@123 | N1    |
| Técnico N2    | maria.n2@helpdesk.com  | Admin@123 | N2    |
| Técnico N3    | carlos.n3@helpdesk.com | Admin@123 | N3    |

Clientes podem se cadastrar diretamente pela tela de **Cadastro** do sistema.

---

## Sobre o Projeto

Sistema para registrar, acompanhar e resolver incidentes e solicitações técnicas de TI.
Desenvolvido com boas práticas de engenharia de software e conformidade com normas ISO.

### Funcionalidades

- Login com autenticação JWT + cadastro público para clientes
- Abertura de chamados com upload de até **3 fotos** (JPG, PNG, WEBP)
- Fluxo de escalação N1 → N2 → N3
- Histórico completo e imutável de cada chamado
- Dashboard com estatísticas em tempo real
- Gestão de empresas, equipamentos e usuários
- Admin pode editar nível de suporte, cargo e status de colaboradores
- Controle de acesso por tipo de usuário (Cliente / Colaborador) e nível

---

## Stack Tecnológica

| Camada       | Tecnologia                  |
|--------------|-----------------------------|
| Backend      | Python 3.11 + FastAPI       |
| Banco        | PostgreSQL (Supabase cloud) |
| Frontend     | HTML + CSS + JS (vanilla)   |
| Auth         | JWT (python-jose) + bcrypt  |
| ORM          | SQLAlchemy 2.0              |
| Servidor     | Uvicorn                     |
| Hospedagem   | Render (API) + Netlify (frontend) |
| Versionamento| Git + GitHub                |

---

## Branches

| Branch    | Finalidade                              |
|-----------|-----------------------------------------|
| `DEVELOP` | Desenvolvimento — onde o código é feito |
| `PROD`    | Produção — Render e Netlify monitoram   |

**Fluxo correto para subir mudanças:**
```bash
# 1. Desenvolva e commite no DEVELOP
git add .
git commit -m "feat: descrição da mudança"
git push origin DEVELOP

# 2. Mande para PROD
git checkout PROD
git merge DEVELOP
git push origin PROD
```
O Render e o Netlify fazem o deploy automaticamente após o push no PROD.

---

## Como Rodar Localmente

### Pré-requisitos

- Python 3.11 instalado
- Git instalado
- Conta no Supabase (ou PostgreSQL local)

### 1. Clonar o repositório

```bash
git clone https://github.com/YanMM50/helpdesk-system.git
cd helpdesk-system
git checkout DEVELOP
```

### 2. Configurar o backend

```bash
cd backend

# Criar e ativar ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo de configuração
copy .env.example .env
```

Edite o `.env` com as credenciais reais (peça ao Yan as variáveis do Supabase):

```env
DATABASE_URL=postgresql://...  # URL do Supabase (Session Pooler)
SECRET_KEY=...                 # Chave JWT
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
UPLOAD_DIR=uploads
DEBUG=True
```

### 3. Iniciar o backend

```bash
python run.py
```

API disponível em: `http://localhost:8000`
Documentação: `http://localhost:8000/docs`

### 4. Abrir o frontend

Para rodar localmente, edite `frontend/js/api.js` e troque a URL:

```js
// Para desenvolvimento local:
const API_BASE = "http://localhost:8000";

// Para produção (Render):
const API_BASE = "https://helpdesk-system-aodq.onrender.com";
```

Depois abra `frontend/index.html` no navegador ou use a extensão **Live Server** do VS Code.

---

## Estrutura do Projeto

```
helpdesk-system/
├── backend/
│   ├── app/
│   │   ├── main.py             # Ponto de entrada + CORS
│   │   ├── config.py           # Configurações (.env)
│   │   ├── database.py         # Conexão com banco
│   │   ├── models/             # Tabelas ORM (user, ticket, etc.)
│   │   ├── schemas/            # Validação de entrada/saída (Pydantic)
│   │   ├── routers/            # Endpoints: auth, users, tickets, dashboard
│   │   ├── services/           # Autenticação e permissões
│   │   └── utils/              # JWT e bcrypt
│   ├── requirements.txt        # Dependências Python
│   ├── runtime.txt             # Versão do Python para o Render (3.11.9)
│   └── .env.example            # Template de variáveis de ambiente
│
├── frontend/
│   ├── index.html              # Tela de login (background blur)
│   ├── cadastro.html           # Cadastro público de clientes
│   ├── dashboard.html          # Painel principal
│   ├── tickets.html            # Lista de chamados
│   ├── ticket-detail.html      # Detalhes + histórico + ações
│   ├── new-ticket.html         # Abrir chamado (upload de fotos)
│   ├── equipments.html         # Gestão de equipamentos
│   ├── companies.html          # Gestão de empresas
│   ├── users.html              # Gestão de usuários (somente admin)
│   ├── css/style.css           # Estilos globais
│   ├── img/
│   │   ├── help-desk.png       # Ícone do sistema
│   │   └── background helpdesk.jpg  # Fundo da tela de login
│   └── js/
│       ├── api.js              # Todas as chamadas HTTP à API
│       └── utils.js            # Funções reutilizáveis + autenticação
│
├── database/
│   └── schema.sql              # Script SQL completo (tabelas + seed)
│
├── docs/
│   ├── arquitetura.md          # Arquitetura técnica + normas ISO
│   ├── plano-manutencao.md     # Plano de manutenção ISO/IEC 14764
│   └── testes.md               # Levantamento de testes com evidências
│
└── README.md
```

---

## Tipos de Usuário

| Tipo         | Como é criado              | Acesso                          |
|--------------|----------------------------|---------------------------------|
| `CLIENTE`    | Cadastro público (tela)    | Apenas seus próprios chamados   |
| `COLABORADOR`| Admin via painel Usuários  | Dashboard, todos os chamados    |

Colaboradores têm níveis: **N1**, **N2**, **N3** ou **ADMIN**.

---

## Endpoints Principais da API

| Método | Endpoint                  | Descrição                   | Auth |
|--------|---------------------------|-----------------------------|------|
| POST   | /auth/login               | Login                       | Não  |
| POST   | /auth/register            | Cadastro de cliente         | Não  |
| GET    | /auth/me                  | Dados do usuário logado     | Sim  |
| GET    | /tickets                  | Listar chamados             | Sim  |
| POST   | /tickets                  | Abrir chamado               | Sim  |
| PATCH  | /tickets/{id}/status      | Alterar status              | Sim  |
| POST   | /tickets/{id}/encaminhar  | Encaminhar nível            | Sim  |
| POST   | /tickets/{id}/comentarios | Comentar                    | Sim  |
| POST   | /tickets/{id}/anexos      | Upload de foto (máx. 3)     | Sim  |
| GET    | /dashboard/resumo         | Estatísticas                | Sim  |
| GET    | /users                    | Listar usuários             | Sim  |
| POST   | /users                    | Criar usuário (admin)       | Sim  |
| PUT    | /users/{id}               | Editar usuário (admin)      | Sim  |

Documentação completa e interativa: `https://helpdesk-system-aodq.onrender.com/docs`

---

## Fluxo de Atendimento

```
Chamado Aberto (N1)
       │
       ├── Problema simples? ──→ Resolve e fecha
       │
       └── Problema complexo? ──→ Encaminha para N2
                                         │
                                         ├── Resolve? ──→ Fecha
                                         │
                                         └── Muito complexo? ──→ Encaminha para N3
                                                                        │
                                                                        └── Resolve e fecha
```

Cada etapa gera um registro automático no histórico com: usuário, data/hora, tipo de ação e status.

---

## Conformidade com Normas ISO

| Norma         | Aplicação                                          |
|---------------|----------------------------------------------------|
| ISO/IEC 12207 | Ciclo de vida estruturado com documentação completa|
| ISO/IEC 14764 | Plano de manutenção com os 4 tipos definidos       |
| ISO/IEC 9126  | Qualidade: funcionalidade, segurança, usabilidade  |
| ISO/IEC 20000 | Gestão de incidentes, SLA e escalação N1/N2/N3     |

---

## Histórico de Versões

| Versão | Data       | Mudanças                                                  |
|--------|------------|-----------------------------------------------------------|
| v1.0.0 | 2026-03-01 | Versão inicial — estrutura completa do sistema            |
| v1.1.0 | 2026-03-28 | Cadastro de clientes, upload de fotos, edição de usuários, background blur, deploy em nuvem |

---

## Documentação

- [Arquitetura técnica](docs/arquitetura.md)
- [Plano de Manutenção ISO/IEC 14764](docs/plano-manutencao.md)
- [Levantamento de Testes](docs/testes.md)

---

*Projeto acadêmico — SENAI — Curso Técnico em TI*
*Desenvolvido por Yan Mendes (YanMM50)*
