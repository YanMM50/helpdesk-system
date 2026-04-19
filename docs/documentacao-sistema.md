# DOCUMENTAÇÃO DO SISTEMA
# Help Desk — Sistema de Gestão de Chamados Técnicos

**Versão:** 1.3.0
**Data:** 19/04/2026
**Autores:** Camila Alban | Yan Mendes
**Instituição:** SENAI — Curso Técnico em Informática

---

---

# 1. VISÃO GERAL DO SISTEMA

## 1.1 Objetivo

O Help Desk é um sistema web de gestão de chamados técnicos desenvolvido para centralizar, organizar e acompanhar incidentes e solicitações de suporte de TI. Seu objetivo é substituir canais informais de atendimento (e-mail, telefone, WhatsApp) por uma plataforma estruturada que garante rastreabilidade, responsabilidade e qualidade no atendimento.

## 1.2 Público-Alvo

| Perfil | Descrição |
|--------|-----------|
| Clientes | Usuários finais que abrem chamados para reportar problemas ou solicitar suporte |
| Técnicos (N1/N2/N3) | Colaboradores responsáveis por atender, resolver e escalonar chamados |
| Administradores | Gestores do sistema com acesso total a todas as funcionalidades |

## 1.3 Problema que Resolve

Organizações que dependem de suporte técnico frequentemente enfrentam:

- Chamados perdidos ou sem resposta por falta de registro formal
- Ausência de histórico e rastreabilidade das ações tomadas
- Dificuldade em priorizar atendimentos por urgência
- Falta de métricas sobre desempenho da equipe de suporte
- Ausência de feedback dos usuários sobre a qualidade do atendimento

O sistema resolve esses problemas oferecendo uma plataforma centralizada com fluxo de atendimento estruturado, histórico imutável e relatórios gerenciais.

## 1.4 Principais Funcionalidades

- Abertura de chamados com upload de imagens (até 3 fotos)
- Fluxo de escalação em três níveis: N1 → N2 → N3
- Aceite de chamados pelos técnicos (sem atribuição forçada)
- Avaliação do atendimento pelo cliente (CSAT 1–5 estrelas)
- Dashboard com indicadores em tempo real
- Relatórios exportáveis em CSV e PDF
- Controle de acesso por perfil de usuário
- Histórico completo e imutável de cada chamado
- Gestão de empresas, equipamentos e usuários

---

---

# 2. REQUISITOS FUNCIONAIS

## RF-01 — Autenticação de Usuários
O sistema deve permitir login com e-mail e senha, retornando um token JWT válido por 8 horas. Credenciais inválidas devem exibir mensagem de erro sem revelar qual campo está errado.

## RF-02 — Cadastro Público de Clientes
O sistema deve permitir que qualquer pessoa se cadastre como cliente pela tela pública de cadastro, sem necessidade de aprovação prévia.

## RF-03 — Abertura de Chamados
Usuários autenticados devem poder abrir chamados informando: título, descrição detalhada, prioridade (Baixa/Média/Alta/Crítica), empresa e equipamento associado. É permitido anexar até 3 imagens (JPG, PNG ou WEBP).

## RF-04 — Listagem e Filtro de Chamados
O sistema deve exibir chamados em lista com filtros por status, prioridade e nível de suporte. A listagem respeita o perfil do usuário logado:

- **Cliente:** visualiza apenas seus próprios chamados
- **Técnico N1/N2/N3:** visualiza chamados do seu nível sem técnico atribuído ou atribuídos a si
- **Administrador:** visualiza todos os chamados

## RF-05 — Detalhamento do Chamado
Cada chamado deve exibir: protocolo, título, descrição, prioridade, status, nível atual, solicitante, técnico responsável, empresa, equipamento, datas de abertura e fechamento, histórico completo de ações e anexos.

## RF-06 — Aceitar Chamado
Técnicos devem poder aceitar chamados não atribuídos dentro do seu nível. Ao aceitar, o técnico é registrado como responsável e o status muda automaticamente para "Em Atendimento".

## RF-07 — Alteração de Status
Colaboradores e administradores devem poder alterar o status de um chamado com registro obrigatório de comentário de motivo.

## RF-08 — Comentários no Chamado
Qualquer usuário com acesso ao chamado pode adicionar comentários. Todos os comentários são registrados no histórico com data, hora e usuário.

## RF-09 — Escalação de Nível
Técnicos podem encaminhar chamados para níveis superiores (N1 → N2, N1 → N3, N2 → N3). A escalação é irreversível — não é possível retornar para nível inferior. Ao encaminhar, o técnico anterior é removido e o chamado fica disponível para aceite no novo nível.

## RF-10 — Upload de Anexos
O sistema deve permitir upload de arquivos (imagens e documentos) tanto na abertura do chamado quanto durante o atendimento. Arquivos são armazenados no Supabase Storage com URLs públicas permanentes.

## RF-11 — Avaliação do Atendimento (CSAT)
Após o chamado ser marcado como Resolvido ou Fechado, o cliente solicitante deve poder avaliá-lo com uma nota de 1 a 5 estrelas. A avaliação é permitida apenas uma vez por chamado.

## RF-12 — Dashboard Gerencial
O sistema deve exibir indicadores em tempo real: total de chamados abertos, chamados por prioridade crítica, distribuição por nível (N1/N2/N3), total de resolvidos, lista dos últimos chamados e barras de progresso por status.

## RF-13 — Relatórios Exportáveis
Administradores devem poder filtrar chamados por status, prioridade, nível e período, visualizar resumo estatístico e exportar os dados em CSV ou imprimir em PDF.

## RF-14 — Gestão de Usuários (Admin)
O administrador deve poder criar, editar e excluir (soft delete) usuários, definindo tipo (Cliente/Colaborador) e nível de suporte (N1/N2/N3/Admin).

## RF-15 — Gestão de Empresas e Equipamentos (Admin)
O administrador deve poder cadastrar e excluir empresas e equipamentos que ficam disponíveis para seleção ao abrir chamados.

---

---

# 3. REQUISITOS NÃO FUNCIONAIS

## 3.1 Desempenho
- O tempo de resposta da API deve ser inferior a 2 segundos para requisições simples
- A listagem de chamados deve suportar até 1.000 registros sem degradação perceptível
- Imagens devem ser carregadas via URL do Supabase Storage (CDN), sem tráfego pelo servidor da API

## 3.2 Segurança
- Toda comunicação deve ocorrer via HTTPS
- Autenticação por token JWT com expiração de 8 horas
- Senhas armazenadas com hash bcrypt (fator de custo 12)
- Endpoints protegidos por middleware de autenticação
- Controle de acesso por perfil em todos os endpoints sensíveis
- Usuários excluídos recebem soft delete (campo `ativo = false`), preservando integridade referencial

## 3.3 Usabilidade
- Interface responsiva para desktop e tablet
- Feedback visual imediato para todas as ações (toasts de sucesso/erro)
- Navegação por menu lateral fixo com indicação da página ativa
- Formulários com validação client-side antes do envio
- Histórico de chamados em linha do tempo visual

## 3.4 Escalabilidade
- Arquitetura stateless (API sem sessão) permite escalabilidade horizontal
- Banco de dados hospedado em serviço gerenciado (Supabase/PostgreSQL)
- Storage de arquivos desacoplado da API (Supabase Storage)
- Frontend estático hospedado em CDN (Netlify)

## 3.5 Disponibilidade
- Frontend: disponível 24/7 via Netlify CDN
- Backend: hospedado no Render (plano gratuito — pode ter cold start de ~50 segundos após inatividade)
- Banco de dados: Supabase (pausa automática após 7 dias de inatividade no plano gratuito)
- Recomendação para produção real: planos pagos eliminam cold starts e pausas automáticas

---

---

# 4. REGRAS DE NEGÓCIO

## RN-01 — Cliente não atribui técnico
Ao abrir um chamado, o cliente não seleciona o técnico responsável. O chamado é criado sem técnico atribuído e disponibilizado para aceite pelos técnicos do nível N1.

## RN-02 — Técnico vê apenas chamados do seu nível
Cada técnico visualiza exclusivamente os chamados que estão no seu nível de suporte E que estejam sem técnico atribuído OU atribuídos especificamente a ele. Técnicos de outros níveis não visualizam os chamados.

## RN-03 — Aceite de chamado
Um técnico pode aceitar qualquer chamado do seu nível que esteja sem técnico atribuído. Após o aceite, o chamado é bloqueado para outros técnicos do mesmo nível (já possui responsável).

## RN-04 — Escalação unidirecional
A escalação de nível só pode avançar: N1 → N2 ou N3; N2 → N3. Nunca é permitido retroceder (N2 → N1, N3 → N2). Ao encaminhar, o técnico anterior é desatribuído.

## RN-05 — Avaliação única por chamado
O cliente só pode avaliar um chamado após ele estar com status Resolvido ou Fechado. A avaliação é permitida apenas uma vez — não pode ser alterada após o envio.

## RN-06 — Histórico imutável
Todo evento do chamado (abertura, comentário, mudança de status, encaminhamento) é registrado automaticamente no histórico com: usuário, data/hora e detalhes da ação. Registros do histórico não podem ser editados ou excluídos.

## RN-07 — Soft delete para exclusões
Usuários, empresas e equipamentos excluídos pelo administrador recebem o campo `ativo = false`. Os dados são preservados no banco para manter integridade do histórico de chamados já registrados.

## RN-08 — Recadastro com e-mail excluído
Se um usuário com soft delete tentar se registrar com o mesmo e-mail, o sistema reativa a conta (atualiza nome, senha e define `ativo = true`) em vez de criar um novo registro, evitando violação de unicidade.

## RN-09 — Prioridade e SLA
Chamados são classificados por prioridade:

| Prioridade | Descrição | Impacto |
|------------|-----------|---------|
| Baixa | Dúvidas, melhorias | Sem impacto operacional |
| Média | Problema sem bloqueio | Impacto parcial |
| Alta | Problema com impacto | Operação comprometida |
| Crítica | Sistema parado | Impacto total no negócio |

---

---

# 5. PERFIS DE USUÁRIO

## 5.1 Cliente

**Como é criado:** Auto-cadastro pela tela pública de cadastro.

**Permissões:**
- Abrir novos chamados com título, descrição, prioridade, empresa e equipamento
- Visualizar apenas seus próprios chamados
- Adicionar comentários nos seus chamados
- Avaliar o atendimento após resolução (nota 1–5)
- Visualizar histórico e anexos dos seus chamados

**Restrições:**
- Não pode atribuir técnico ao abrir chamado
- Não pode alterar status de chamados
- Não pode encaminhar chamados
- Não acessa chamados de outros clientes

---

## 5.2 Técnico N1 — Suporte Básico

**Como é criado:** Cadastrado pelo administrador.

**Escopo:** Atendimento a problemas de nível básico (conectividade, configuração, dúvidas gerais).

**Permissões:**
- Visualizar chamados N1 sem técnico atribuído ou atribuídos a si
- Aceitar chamados disponíveis no seu nível
- Comentar, alterar status, anexar arquivos
- Encaminhar chamados para N2 ou N3 quando necessário
- Visualizar dashboard e relatórios

---

## 5.3 Técnico N2 — Suporte Especializado

**Como é criado:** Cadastrado pelo administrador.

**Escopo:** Atendimento a problemas especializados (configurações avançadas, análise de sistemas).

**Permissões:** Idênticas ao N1, porém limitadas ao nível N2.

**Diferencial:** Pode encaminhar apenas para N3.

---

## 5.4 Técnico N3 — Engenharia / Desenvolvimento

**Como é criado:** Cadastrado pelo administrador.

**Escopo:** Problemas críticos de infraestrutura, desenvolvimento e engenharia.

**Permissões:** Idênticas ao N1 e N2, porém limitadas ao nível N3.

**Diferencial:** Nível máximo — não pode encaminhar para outros níveis.

---

## 5.5 Administrador

**Como é criado:** Cadastrado diretamente no banco de dados (seed inicial).

**Permissões:**
- Acesso total a todos os chamados (todos os níveis)
- Criar, editar e excluir usuários, empresas e equipamentos
- Visualizar relatórios completos e exportar dados
- Alterar perfil e nível de qualquer usuário
- Acesso a todos os recursos do sistema sem restrições

---

---

# 6. CASOS DE USO

## UC-01 — Abrir Chamado

**Ator:** Cliente

**Descrição:** O cliente registra um novo chamado técnico no sistema.

**Fluxo Principal:**
1. Cliente acessa "Novo Chamado" no menu
2. Preenche título e descrição do problema
3. Seleciona prioridade (Baixa / Média / Alta / Crítica)
4. Opcionalmente seleciona empresa e equipamento relacionado
5. Opcionalmente anexa até 3 fotos do problema
6. Clica em "Abrir Chamado"
7. Sistema gera protocolo único (ex: CHM-2026-00010)
8. Sistema redireciona para o detalhe do chamado criado

**Fluxo Alternativo — Upload com erro:**
- Se a imagem exceder o tipo permitido, exibe mensagem de erro e ignora o arquivo

---

## UC-02 — Aceitar Chamado

**Ator:** Técnico (N1, N2 ou N3)

**Descrição:** O técnico assume a responsabilidade por um chamado do seu nível.

**Pré-condição:** Chamado está no mesmo nível do técnico e sem técnico atribuído.

**Fluxo Principal:**
1. Técnico acessa o detalhe de um chamado disponível
2. Sistema exibe botão "✅ Aceitar Chamado"
3. Técnico clica no botão e confirma
4. Sistema atribui o técnico ao chamado
5. Status muda automaticamente para "Em Atendimento"
6. Histórico registra a ação

**Fluxo Alternativo — Chamado já aceito:**
- Se outro técnico aceitou primeiro, sistema exibe erro e o botão desaparece ao recarregar

---

## UC-03 — Encaminhar Chamado

**Ator:** Técnico (N1 ou N2)

**Descrição:** O técnico escalona o chamado para o próximo nível por impossibilidade de resolução.

**Pré-condição:** Chamado está no nível do técnico; existe nível superior disponível.

**Fluxo Principal:**
1. Técnico acessa o detalhe do chamado
2. Clica em "↗️ Encaminhar"
3. Seleciona o nível de destino (apenas níveis superiores são exibidos)
4. Preenche motivo do encaminhamento
5. Confirma a ação
6. Sistema remove o técnico atual, move o chamado para o nível destino
7. Chamado fica disponível para aceite pelos técnicos do novo nível

**Fluxo Alternativo — Chamado N3:**
- Botão "Encaminhar" não é exibido pois N3 é o nível máximo

---

## UC-04 — Avaliar Atendimento

**Ator:** Cliente

**Descrição:** O cliente avalia a qualidade do atendimento recebido.

**Pré-condição:** Chamado com status Resolvido ou Fechado; cliente é o solicitante; chamado ainda não foi avaliado.

**Fluxo Principal:**
1. Cliente acessa o detalhe do seu chamado resolvido
2. Sistema exibe botão "⭐ Avaliar Atendimento"
3. Cliente clica no botão — modal de avaliação abre
4. Cliente seleciona nota de 1 a 5 estrelas com legenda descritiva
5. Clica em "Enviar Avaliação"
6. Sistema salva a nota e exibe as estrelas no cabeçalho do chamado

**Fluxo Alternativo — Tentativa de dupla avaliação:**
- Botão "Avaliar" não é exibido se chamado já foi avaliado

---

## UC-05 — Gerar Relatório

**Ator:** Administrador

**Descrição:** O administrador filtra e exporta dados dos chamados para análise gerencial.

**Fluxo Principal:**
1. Administrador acessa "Relatórios" no menu lateral
2. Aplica filtros (status, prioridade, nível, período)
3. Sistema exibe tabela com chamados filtrados e resumo estatístico
4. Administrador clica em "⬇️ Exportar CSV" ou "🖨️ Imprimir / PDF"
5. Arquivo é gerado e baixado (CSV) ou página de impressão é aberta (PDF)

---

---

# 7. MODELAGEM DO SISTEMA

## 7.1 Entidades Principais

### Usuário (users)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador único |
| nome | String(100) | Nome completo |
| email | String(150) | E-mail único (login) |
| senha_hash | String | Hash bcrypt da senha |
| tipo_usuario | Enum | CLIENTE ou COLABORADOR |
| nivel_suporte | Enum | N1, N2, N3 ou ADMIN |
| cargo | String(100) | Cargo do colaborador |
| ativo | Boolean | Soft delete (padrão: true) |
| criado_em | DateTime | Data de criação |

### Chamado (tickets)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador único |
| protocolo | String(20) | Código único (CHM-AAAA-NNNNN) |
| titulo | String(200) | Título do chamado |
| descricao | Text | Descrição detalhada |
| prioridade | Enum | BAIXA, MEDIA, ALTA, CRITICA |
| status | Enum | ABERTO, EM_ANALISE, EM_ATENDIMENTO, AGUARDANDO_CLIENTE, RESOLVIDO, FECHADO |
| nivel_atual | Enum | N1, N2, N3 |
| solicitante_id | FK → users | Quem abriu o chamado |
| tecnico_id | FK → users | Técnico responsável (nullable) |
| company_id | FK → companies | Empresa associada (nullable) |
| equipamento_id | FK → equipments | Equipamento associado (nullable) |
| avaliacao | Integer | Nota CSAT 1–5 (nullable) |
| data_abertura | DateTime | Data/hora de abertura |
| data_fechamento | DateTime | Data/hora de fechamento (nullable) |
| prazo_sla | DateTime | Prazo de SLA (nullable) |

### Histórico (ticket_history)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador único |
| ticket_id | FK → tickets | Chamado relacionado |
| usuario_id | FK → users | Usuário que realizou a ação |
| tipo_acao | Enum | ABERTURA, COMENTARIO, MUDANCA_STATUS, ENCAMINHAMENTO, RESOLUCAO, FECHAMENTO, EDICAO |
| comentario | Text | Texto da ação (nullable) |
| nivel_anterior | Enum | Nível antes da mudança (nullable) |
| nivel_novo | Enum | Nível após a mudança (nullable) |
| status_anterior | Enum | Status antes da mudança (nullable) |
| status_novo | Enum | Status após a mudança (nullable) |
| criado_em | DateTime | Data/hora do registro |

### Empresa (companies)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador único |
| nome | String(150) | Nome da empresa |
| cnpj | String(18) | CNPJ (nullable, único) |
| telefone | String(20) | Telefone de contato (nullable) |
| email | String(150) | E-mail de contato (nullable) |
| ativo | Boolean | Soft delete (padrão: true) |

### Equipamento (equipments)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador único |
| nome | String(150) | Nome do equipamento |
| tipo | String(80) | Tipo (Desktop, Notebook, Servidor...) |
| fabricante | String(100) | Fabricante (nullable) |
| modelo | String(100) | Modelo (nullable) |
| numero_serie | String(100) | Número de série (nullable, único) |
| company_id | FK → companies | Empresa proprietária (nullable) |
| ativo | Boolean | Soft delete (padrão: true) |

### Anexo (attachments)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | Identificador único |
| ticket_id | FK → tickets | Chamado relacionado |
| nome_original | String | Nome original do arquivo |
| nome_arquivo | String | Nome no storage (UUID) |
| tipo_mime | String | Tipo MIME do arquivo |
| tamanho_bytes | BigInteger | Tamanho em bytes |
| caminho | String | URL pública no Supabase Storage |
| criado_em | DateTime | Data/hora do upload |

## 7.2 Relacionamentos

```
users (1) ──────── (N) tickets [solicitante_id]
users (1) ──────── (N) tickets [tecnico_id]
users (1) ──────── (N) ticket_history [usuario_id]
tickets (1) ─────── (N) ticket_history
tickets (1) ─────── (N) attachments
companies (1) ──── (N) tickets
companies (1) ──── (N) equipments
equipments (1) ─── (N) tickets
```

---

---

# 8. FLUXO DO SISTEMA

## 8.1 Fluxo Completo de Atendimento

```
[CLIENTE]
    │
    ▼
Abre chamado → Gera protocolo CHM-AAAA-NNNNN
    │           Status: ABERTO | Nível: N1
    ▼
[TÉCNICO N1]
    │
    ├── Aceita chamado → Status: EM_ATENDIMENTO
    │       │
    │       ├── Resolve? → Status: RESOLVIDO
    │       │                   │
    │       │                   ▼
    │       │           [CLIENTE avalia 1-5 ⭐]
    │       │
    │       └── Precisa de mais? → Encaminha para N2
    │                               Status mantido | Nível: N2
    │                               Técnico: removido
    │
    ▼
[TÉCNICO N2]
    │
    ├── Aceita chamado
    │       │
    │       ├── Resolve? → Status: RESOLVIDO
    │       │
    │       └── Muito complexo? → Encaminha para N3
    │                              Nível: N3 | Técnico: removido
    │
    ▼
[TÉCNICO N3]
    │
    └── Aceita → Resolve → Status: RESOLVIDO
                               │
                           [CLIENTE avalia]
                               │
                           [ADMIN fecha] → Status: FECHADO
```

## 8.2 Estados do Chamado

| Status | Descrição | Transições Possíveis |
|--------|-----------|----------------------|
| ABERTO | Chamado criado, aguardando aceite | → EM_ANALISE, EM_ATENDIMENTO |
| EM_ANALISE | Técnico analisando o problema | → EM_ATENDIMENTO, AGUARDANDO_CLIENTE |
| EM_ATENDIMENTO | Técnico trabalhando ativamente | → AGUARDANDO_CLIENTE, RESOLVIDO |
| AGUARDANDO_CLIENTE | Aguardando retorno do solicitante | → EM_ATENDIMENTO, FECHADO |
| RESOLVIDO | Problema solucionado | → FECHADO |
| FECHADO | Chamado encerrado definitivamente | — (estado final) |

---

---

# 9. ARQUITETURA E BOAS PRÁTICAS

## 9.1 Arquitetura Geral

O sistema segue arquitetura **cliente-servidor** com separação clara entre frontend e backend:

```
[NAVEGADOR]                     [RENDER.COM]              [SUPABASE]
Frontend (Netlify)    ──HTTP──▶  Backend (FastAPI)  ──▶  PostgreSQL
HTML + CSS + JS                  Python 3.11               banco de dados
                                      │
                                      └──▶  Supabase Storage
                                             (arquivos/imagens)
```

## 9.2 Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|--------|------------|---------------|
| Backend | Python 3.11 + FastAPI | Alto desempenho, tipagem forte, documentação automática (Swagger) |
| ORM | SQLAlchemy 2.0 | Abstração do banco, evita SQL injection, suporte a migrations |
| Banco | PostgreSQL (Supabase) | Banco relacional robusto, gerenciado, com backup automático |
| Storage | Supabase Storage | CDN integrado, URLs públicas permanentes, sem custo adicional |
| Autenticação | JWT + bcrypt | Padrão da indústria, stateless, seguro |
| Frontend | HTML + CSS + JS vanilla | Sem dependências externas, carregamento rápido, fácil manutenção |
| Hospedagem API | Render | Deploy automático via GitHub, SSL gratuito |
| Hospedagem Frontend | Netlify | CDN global, deploy automático, SSL gratuito |

## 9.3 Organização do Backend (Camadas)

```
backend/app/
├── main.py          — Inicialização da aplicação + configuração de CORS
├── config.py        — Variáveis de ambiente (.env)
├── database.py      — Conexão com banco (Session + engine)
├── models/          — Modelos ORM (mapeamento das tabelas)
│   ├── user.py
│   ├── ticket.py
│   ├── company.py
│   └── equipment.py
├── schemas/         — Validação de dados com Pydantic (entrada e saída)
│   ├── user.py
│   └── ticket.py
├── routers/         — Endpoints da API organizados por domínio
│   ├── auth.py      — /auth/login, /auth/register, /auth/me
│   ├── tickets.py   — /tickets (CRUD + ações)
│   ├── users.py     — /users (CRUD)
│   ├── companies.py — /companies e /equipments
│   └── dashboard.py — /dashboard/resumo
├── services/
│   └── auth_service.py — Middleware de autenticação JWT
└── utils/
    └── security.py     — Hash e verificação de senhas
```

## 9.4 Boas Práticas Aplicadas

**Segurança:**
- Senhas nunca armazenadas em texto puro (bcrypt)
- Tokens JWT com expiração configurável
- Middleware de autenticação em todos os endpoints protegidos
- Controle de acesso por perfil (RBAC) em cada endpoint
- Soft delete preserva integridade referencial

**Qualidade de Código:**
- Separação clara de responsabilidades (Models, Schemas, Routers, Services)
- Schemas Pydantic garantem validação automática de entrada e saída
- Tratamento centralizado de erros (HTTPException com mensagens descritivas)
- Nomenclatura consistente em português no domínio de negócio

**Banco de Dados:**
- Uso de enums para campos com valores fixos (status, prioridade, nível)
- Chaves estrangeiras com integridade referencial
- Soft delete com campo `ativo` para preservar histórico
- Índices nas colunas mais consultadas (email, ticket_id)

**Frontend:**
- API centralizada em `api.js` — troca de URL em um único lugar
- Utilitários reutilizáveis em `utils.js` (autenticação, badges, formatação)
- Feedback visual imediato em todas as operações (toasts)
- Controle de acesso aplicado tanto no frontend quanto no backend

## 9.5 Conformidade com Normas ISO

| Norma | Aplicação no Sistema |
|-------|----------------------|
| ISO/IEC 12207 | Ciclo de vida estruturado: análise de requisitos, projeto, implementação, testes e documentação |
| ISO/IEC 14764 | Plano de manutenção com os 4 tipos: corretiva, adaptativa, perfectiva e preventiva |
| ISO/IEC 9126 | Atributos de qualidade: funcionalidade, confiabilidade, usabilidade, eficiência, manutenibilidade e portabilidade |
| ISO/IEC 20000 | Gestão de serviços: categorização de incidentes, SLA por prioridade, escalação N1/N2/N3 |

---

---

# 10. SUGESTÕES DE MELHORIA — UX/UI

## 10.1 Paleta de Cores Recomendada (Padrão SaaS)

| Uso | Cor | Hex |
|-----|-----|-----|
| Primária (ações principais) | Azul profundo | #2563EB |
| Secundária (hover) | Azul médio | #1D4ED8 |
| Sucesso | Verde suave | #16A34A |
| Alerta | Âmbar | #D97706 |
| Perigo | Vermelho | #DC2626 |
| Fundo principal | Cinza claro | #F8FAFC |
| Fundo cards | Branco | #FFFFFF |
| Texto principal | Cinza escuro | #0F172A |
| Texto secundário | Cinza médio | #64748B |
| Bordas | Cinza claro | #E2E8F0 |

## 10.2 Tipografia Recomendada

- **Família:** Inter (Google Fonts) — moderna, legível, usada em Notion, Linear, Vercel
- **Tamanhos:**
  - Títulos H1: 24px / bold
  - Títulos H2: 18px / semibold
  - Texto padrão: 14px / regular
  - Texto auxiliar: 12px / regular
  - Código (protocolo): 12px / monospace (ex: JetBrains Mono)

## 10.3 Componentes Visuais Recomendados

- **Cards com sombra sutil** (`box-shadow: 0 1px 3px rgba(0,0,0,0.08)`) ao invés de bordas visíveis
- **Status badges** com background suave (ex: verde 10% opacidade + texto verde escuro)
- **Sidebar recolhível** em telas menores (ícone apenas, sem texto)
- **Tabelas com hover** em linhas (`background: #F8FAFC` ao passar o mouse)
- **Skeleton loading** ao invés de spinner — mais moderno e menos intrusivo
- **Avatar com iniciais** coloridas baseadas no nome do usuário
- **Breadcrumb** no topbar para orientação de navegação

## 10.4 Inspirações de Mercado

| Sistema | O que aplicar |
|---------|---------------|
| **Zendesk** | Status de chamados com cores sólidas, barra de progresso do SLA |
| **Freshdesk** | Dashboard limpo com métricas grandes e cards clicáveis |
| **Linear** | Sidebar compacta, tipografia moderna, ações inline |
| **Notion** | Espaço em branco generoso, hierarquia visual clara |
| **Intercom** | Histórico de conversa estilo chat, mais amigável para clientes |

---

*Documento gerado em 19/04/2026 — Versão 1.3.0*
*Desenvolvido por Camila Alban e Yan Mendes — SENAI Curso Técnico em TI*
