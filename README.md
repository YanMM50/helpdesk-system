# Sistema de Gestão de Chamados Técnicos — Help Desk

> Projeto acadêmico desenvolvido para o curso técnico em TI.
> Sistema completo de gerenciamento de chamados com suporte em três níveis (N1, N2, N3).

---

## Sobre o Projeto

Este sistema permite registrar, acompanhar e resolver incidentes e solicitações técnicas de TI. Desenvolvido com foco em boas práticas de engenharia de software e conformidade com normas ISO.

### Funcionalidades

- Login com autenticação JWT
- Abertura e acompanhamento de chamados técnicos
- Fluxo de escalação N1 → N2 → N3
- Histórico completo e imutável de cada chamado
- Upload de evidências (fotos, PDFs)
- Dashboard com estatísticas em tempo real
- Gestão de empresas, equipamentos e usuários
- Controle de acesso por nível de suporte

---

## Stack Tecnológica

| Camada      | Tecnologia           |
|-------------|----------------------|
| Backend     | Python 3.11 + FastAPI|
| Banco       | PostgreSQL           |
| Frontend    | HTML + CSS + JS      |
| Auth        | JWT (python-jose)    |
| ORM         | SQLAlchemy 2.0       |
| Servidor    | Uvicorn              |
| Versionamento| Git + GitHub        |

---

## Como Rodar o Projeto

### Pré-requisitos

- Python 3.10 ou superior instalado
- PostgreSQL instalado e rodando
- Git instalado

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/helpdesk-system.git
cd helpdesk-system
```

### 2. Configurar o banco de dados

```sql
-- No psql ou pgAdmin, execute:
CREATE DATABASE helpdesk_db;
```

Em seguida, execute o script SQL para criar as tabelas:

```bash
psql -U postgres -d helpdesk_db -f database/schema.sql
```

### 3. Configurar o backend

```bash
cd backend

# Criar ambiente virtual Python (isola as dependências do projeto)
python -m venv venv

# Ativar o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo de configuração
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
DATABASE_URL=postgresql://postgres:SUASENHA@localhost:5432/helpdesk_db
SECRET_KEY=gere-uma-chave-segura-aqui
```

> Para gerar uma SECRET_KEY segura:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

### 4. Iniciar o backend

```bash
python run.py
```

A API estará disponível em: `http://localhost:8000`
Documentação interativa: `http://localhost:8000/docs`

### 5. Abrir o frontend

Abra o arquivo `frontend/index.html` diretamente no navegador.

> **Dica:** Para evitar problemas de CORS ao desenvolver, use a extensão "Live Server" no VS Code.

### Credenciais de acesso (dados iniciais)

| Usuário         | Email                   | Senha      | Nível |
|-----------------|-------------------------|------------|-------|
| Administrador   | admin@helpdesk.com      | Admin@123  | ADMIN |
| Técnico N1      | joao.n1@helpdesk.com    | Admin@123  | N1    |
| Técnico N2      | maria.n2@helpdesk.com   | Admin@123  | N2    |
| Técnico N3      | carlos.n3@helpdesk.com  | Admin@123  | N3    |

> **Atenção:** Troque as senhas em ambiente de produção!

---

## Estrutura do Projeto

```
projeto-helpdesk/
├── backend/              # API REST em Python/FastAPI
│   ├── app/
│   │   ├── main.py       # Ponto de entrada
│   │   ├── models/       # Tabelas do banco (ORM)
│   │   ├── schemas/      # Contratos da API (Pydantic)
│   │   ├── routers/      # Endpoints HTTP
│   │   ├── services/     # Lógica de autenticação
│   │   └── utils/        # Segurança (JWT, bcrypt)
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # Interface HTML/CSS/JS
│   ├── index.html        # Login
│   ├── dashboard.html    # Painel principal
│   ├── tickets.html      # Lista de chamados
│   ├── ticket-detail.html# Detalhes + ações
│   ├── new-ticket.html   # Abrir chamado
│   ├── css/style.css
│   └── js/
│       ├── api.js        # Comunicação com API
│       └── utils.js      # Utilitários
├── database/
│   └── schema.sql        # Script SQL completo
├── docs/
│   ├── arquitetura.md    # Documentação técnica
│   └── plano-manutencao.md
└── README.md
```

---

## Fluxo de Atendimento (N1 → N2 → N3)

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

**Cada etapa é registrada no histórico com:**
- Usuário responsável pela ação
- Data e hora
- Tipo de ação (abertura, comentário, encaminhamento, etc.)
- Status anterior e novo

---

## Endpoints Principais da API

| Método | Endpoint                     | Descrição                   |
|--------|------------------------------|-----------------------------|
| POST   | /auth/login                  | Realizar login              |
| GET    | /auth/me                     | Dados do usuário logado     |
| GET    | /tickets                     | Listar chamados             |
| POST   | /tickets                     | Abrir chamado               |
| GET    | /tickets/{id}                | Detalhes do chamado         |
| PATCH  | /tickets/{id}/status         | Alterar status              |
| POST   | /tickets/{id}/encaminhar     | Encaminhar para outro nível |
| POST   | /tickets/{id}/comentarios    | Adicionar comentário        |
| POST   | /tickets/{id}/anexos         | Upload de arquivo           |
| GET    | /dashboard/resumo            | Estatísticas do dashboard   |
| GET    | /users                       | Listar usuários             |
| POST   | /users                       | Criar usuário               |
| GET    | /companies                   | Listar empresas             |
| GET    | /equipments                  | Listar equipamentos         |

Documentação completa e interativa disponível em `/docs` (Swagger UI).

---

## Conformidade com Normas ISO

| Norma           | Aplicação no Projeto                                  |
|-----------------|-------------------------------------------------------|
| ISO/IEC 12207   | Ciclo de vida estruturado com documentação completa   |
| ISO/IEC 14764   | Plano de manutenção com os 4 tipos definidos          |
| ISO/IEC 9126    | Qualidade: funcionalidade, segurança, usabilidade     |
| ISO/IEC 20000   | Gestão de incidentes, SLA e escalação N1/N2/N3        |

---

## Segurança

- Senhas com hash bcrypt (nunca armazenadas em texto puro)
- Autenticação via JWT com expiração configurável
- Controle de acesso por nível (N1, N2, N3, Admin)
- Soft delete (registros nunca apagados permanentemente)
- Proteção contra SQL Injection via ORM
- Validação de tipos de arquivo no upload
- Variáveis sensíveis em arquivo `.env` (fora do Git)

---

## Plano de Manutenção

O projeto inclui um Plano de Manutenção completo conforme a ISO/IEC 14764 com:

- Manutenção **Corretiva** — correção de bugs
- Manutenção **Adaptativa** — adequação a novos ambientes
- Manutenção **Evolutiva** — novas funcionalidades
- Manutenção **Preventiva** — melhorias para evitar falhas

Calendário: diário, semanal, mensal, trimestral e anual.

Ver: [docs/plano-manutencao.md](docs/plano-manutencao.md)

---

## Licença

Projeto acadêmico — uso educacional.

---

*Desenvolvido como projeto acadêmico de curso técnico em TI.*
*Arquitetura baseada em normas ISO/IEC 12207, 14764, 9126 e 20000.*
