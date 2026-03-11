-- =============================================================
-- SISTEMA DE GESTÃO DE CHAMADOS TÉCNICOS (HELP DESK)
-- Script de criação do banco de dados
-- Banco: PostgreSQL
-- Versão: 1.0.0
-- =============================================================

-- Criação do banco (execute separadamente se necessário)
-- CREATE DATABASE helpdesk_db;
-- \c helpdesk_db;

-- =============================================================
-- ENUMS (tipos enumerados — garantem integridade dos dados)
-- =============================================================

-- Níveis de suporte dos técnicos
CREATE TYPE nivel_suporte AS ENUM ('N1', 'N2', 'N3', 'ADMIN');

-- Prioridade dos chamados
CREATE TYPE prioridade_chamado AS ENUM ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA');

-- Status possíveis de um chamado
CREATE TYPE status_chamado AS ENUM (
    'ABERTO',
    'EM_ANALISE',
    'EM_ATENDIMENTO',
    'AGUARDANDO_CLIENTE',
    'RESOLVIDO',
    'FECHADO'
);

-- Tipos de ação no histórico
CREATE TYPE tipo_acao AS ENUM (
    'ABERTURA',
    'COMENTARIO',
    'MUDANCA_STATUS',
    'ENCAMINHAMENTO',
    'RESOLUCAO',
    'FECHAMENTO',
    'EDICAO'
);

-- =============================================================
-- TABELA: companies (Empresas / Clientes)
-- Armazena os clientes que utilizam o sistema de suporte
-- =============================================================
CREATE TABLE companies (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(150) NOT NULL,
    cnpj        VARCHAR(18) UNIQUE,
    telefone    VARCHAR(20),
    email       VARCHAR(150),
    endereco    VARCHAR(255),
    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em   TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE companies IS 'Empresas clientes que abrem chamados de suporte';
COMMENT ON COLUMN companies.cnpj IS 'CNPJ no formato XX.XXX.XXX/XXXX-XX';

-- =============================================================
-- TABELA: users (Usuários do Sistema)
-- Armazena tanto técnicos quanto solicitantes
-- =============================================================
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(150) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    senha_hash      VARCHAR(255) NOT NULL,          -- senha criptografada (bcrypt)
    nivel_suporte   nivel_suporte NOT NULL DEFAULT 'N1',
    cargo           VARCHAR(100),
    company_id      INTEGER REFERENCES companies(id) ON DELETE SET NULL,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    ultimo_login    TIMESTAMP,
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE users IS 'Usuários do sistema: técnicos N1/N2/N3, administradores e solicitantes';
COMMENT ON COLUMN users.senha_hash IS 'Hash bcrypt da senha. NUNCA armazenar senha em texto puro.';
COMMENT ON COLUMN users.nivel_suporte IS 'N1=Suporte básico, N2=Especializado, N3=Engenharia, ADMIN=Administrador';

-- =============================================================
-- TABELA: equipments (Equipamentos)
-- Inventário de equipamentos associados às empresas
-- =============================================================
CREATE TABLE equipments (
    id              SERIAL PRIMARY KEY,
    nome            VARCHAR(150) NOT NULL,
    tipo            VARCHAR(100),                   -- ex: Desktop, Notebook, Impressora
    fabricante      VARCHAR(100),
    modelo          VARCHAR(100),
    numero_serie    VARCHAR(100) UNIQUE,
    patrimonio      VARCHAR(50),                    -- número de patrimônio interno
    company_id      INTEGER REFERENCES companies(id) ON DELETE SET NULL,
    responsavel_id  INTEGER REFERENCES users(id) ON DELETE SET NULL,
    ativo           BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE equipments IS 'Inventário de equipamentos de TI dos clientes';
COMMENT ON COLUMN equipments.numero_serie IS 'Número de série único do fabricante';

-- =============================================================
-- TABELA: tickets (Chamados Técnicos)
-- Tabela central do sistema. Registra todos os chamados.
-- =============================================================
CREATE TABLE tickets (
    id              SERIAL PRIMARY KEY,
    titulo          VARCHAR(200) NOT NULL,
    descricao       TEXT NOT NULL,
    prioridade      prioridade_chamado NOT NULL DEFAULT 'MEDIA',
    status          status_chamado NOT NULL DEFAULT 'ABERTO',
    nivel_atual     nivel_suporte NOT NULL DEFAULT 'N1',  -- nível responsável agora

    -- Relacionamentos
    solicitante_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    tecnico_id      INTEGER REFERENCES users(id) ON DELETE SET NULL,  -- técnico responsável
    company_id      INTEGER REFERENCES companies(id) ON DELETE SET NULL,
    equipamento_id  INTEGER REFERENCES equipments(id) ON DELETE SET NULL,

    -- Datas de controle
    data_abertura   TIMESTAMP NOT NULL DEFAULT NOW(),
    data_fechamento TIMESTAMP,
    prazo_sla       TIMESTAMP,                      -- prazo máximo conforme SLA

    -- Controle interno
    protocolo       VARCHAR(20) UNIQUE,             -- número único para o cliente (ex: CHM-2024-00001)
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em   TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE tickets IS 'Chamados técnicos — registro central de incidentes e solicitações';
COMMENT ON COLUMN tickets.nivel_atual IS 'Indica em qual nível (N1/N2/N3) o chamado está agora';
COMMENT ON COLUMN tickets.protocolo IS 'Número de protocolo visível para o cliente';
COMMENT ON COLUMN tickets.prazo_sla IS 'Prazo definido pelo SLA (acordo de nível de serviço)';

-- =============================================================
-- TABELA: ticket_history (Histórico de Chamados)
-- Registra TUDO que acontece com um chamado — imutável!
-- =============================================================
CREATE TABLE ticket_history (
    id              SERIAL PRIMARY KEY,
    ticket_id       INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    usuario_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    tipo_acao       tipo_acao NOT NULL,
    comentario      TEXT,                           -- detalhe da ação
    nivel_anterior  nivel_suporte,                 -- antes do encaminhamento
    nivel_novo      nivel_suporte,                 -- após o encaminhamento
    status_anterior status_chamado,
    status_novo     status_chamado,
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE ticket_history IS 'Histórico completo e imutável de todas as ações em um chamado';
COMMENT ON COLUMN ticket_history.tipo_acao IS 'Tipo: ABERTURA, COMENTARIO, MUDANCA_STATUS, ENCAMINHAMENTO, etc.';

-- =============================================================
-- TABELA: attachments (Anexos / Evidências)
-- Armazena metadados dos arquivos enviados nos chamados
-- =============================================================
CREATE TABLE attachments (
    id              SERIAL PRIMARY KEY,
    ticket_id       INTEGER NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    usuario_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    nome_original   VARCHAR(255) NOT NULL,         -- nome original do arquivo
    nome_arquivo    VARCHAR(255) NOT NULL,         -- nome salvo no servidor (UUID)
    tipo_mime       VARCHAR(100),                  -- ex: image/jpeg, application/pdf
    tamanho_bytes   BIGINT,
    caminho         VARCHAR(500) NOT NULL,         -- caminho relativo no servidor
    criado_em       TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE attachments IS 'Arquivos e evidências (fotos, prints) anexados aos chamados';
COMMENT ON COLUMN attachments.nome_arquivo IS 'Nome gerado pelo sistema (UUID) para evitar conflitos';

-- =============================================================
-- ÍNDICES — melhoram a performance nas consultas mais comuns
-- =============================================================

-- Tickets mais consultados por status e prioridade
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_prioridade ON tickets(prioridade);
CREATE INDEX idx_tickets_nivel_atual ON tickets(nivel_atual);
CREATE INDEX idx_tickets_tecnico ON tickets(tecnico_id);
CREATE INDEX idx_tickets_solicitante ON tickets(solicitante_id);
CREATE INDEX idx_tickets_company ON tickets(company_id);
CREATE INDEX idx_tickets_data_abertura ON tickets(data_abertura DESC);

-- Histórico consultado por chamado
CREATE INDEX idx_history_ticket ON ticket_history(ticket_id);
CREATE INDEX idx_history_criado ON ticket_history(criado_em DESC);

-- Equipamentos por empresa
CREATE INDEX idx_equipments_company ON equipments(company_id);

-- Usuários por email (login)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_nivel ON users(nivel_suporte);

-- =============================================================
-- FUNÇÃO: gerar protocolo automático
-- Formato: CHM-YYYY-NNNNN (ex: CHM-2024-00001)
-- =============================================================
CREATE OR REPLACE FUNCTION gerar_protocolo()
RETURNS TRIGGER AS $$
DECLARE
    ano TEXT;
    sequencia INTEGER;
    novo_protocolo TEXT;
BEGIN
    ano := EXTRACT(YEAR FROM NOW())::TEXT;
    SELECT COUNT(*) + 1 INTO sequencia
    FROM tickets
    WHERE EXTRACT(YEAR FROM data_abertura) = EXTRACT(YEAR FROM NOW());
    novo_protocolo := 'CHM-' || ano || '-' || LPAD(sequencia::TEXT, 5, '0');
    NEW.protocolo := novo_protocolo;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger que executa a função ao inserir um novo chamado
CREATE TRIGGER trigger_gerar_protocolo
BEFORE INSERT ON tickets
FOR EACH ROW
WHEN (NEW.protocolo IS NULL)
EXECUTE FUNCTION gerar_protocolo();

-- =============================================================
-- FUNÇÃO: atualizar campo atualizado_em automaticamente
-- =============================================================
CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_tickets_update
BEFORE UPDATE ON tickets
FOR EACH ROW EXECUTE FUNCTION atualizar_timestamp();

CREATE TRIGGER trigger_users_update
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION atualizar_timestamp();

CREATE TRIGGER trigger_companies_update
BEFORE UPDATE ON companies
FOR EACH ROW EXECUTE FUNCTION atualizar_timestamp();

CREATE TRIGGER trigger_equipments_update
BEFORE UPDATE ON equipments
FOR EACH ROW EXECUTE FUNCTION atualizar_timestamp();

-- =============================================================
-- DADOS INICIAIS (seed) — para testar o sistema
-- =============================================================

-- Empresa exemplo
INSERT INTO companies (nome, cnpj, telefone, email, endereco)
VALUES ('Empresa Demonstração LTDA', '00.000.000/0001-00', '(11) 9999-8888',
        'contato@demo.com.br', 'Rua Exemplo, 100 - São Paulo/SP');

-- Administrador do sistema (senha: Admin@123)
-- Hash gerado com bcrypt, rounds=12
INSERT INTO users (nome, email, senha_hash, nivel_suporte, cargo, company_id)
VALUES (
    'Administrador',
    'admin@helpdesk.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBpj2PJOJfGmjm',
    'ADMIN',
    'Administrador do Sistema',
    1
);

-- Técnico N1
INSERT INTO users (nome, email, senha_hash, nivel_suporte, cargo, company_id)
VALUES (
    'Técnico N1 - João Silva',
    'joao.n1@helpdesk.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBpj2PJOJfGmjm',
    'N1',
    'Analista de Suporte N1',
    1
);

-- Técnico N2
INSERT INTO users (nome, email, senha_hash, nivel_suporte, cargo, company_id)
VALUES (
    'Técnico N2 - Maria Santos',
    'maria.n2@helpdesk.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBpj2PJOJfGmjm',
    'N2',
    'Analista de Suporte N2',
    1
);

-- Técnico N3
INSERT INTO users (nome, email, senha_hash, nivel_suporte, cargo, company_id)
VALUES (
    'Técnico N3 - Carlos Oliveira',
    'carlos.n3@helpdesk.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBpj2PJOJfGmjm',
    'N3',
    'Engenheiro de Sistemas',
    1
);

-- Equipamento exemplo
INSERT INTO equipments (nome, tipo, fabricante, modelo, numero_serie, company_id)
VALUES ('Desktop RH-01', 'Desktop', 'Dell', 'OptiPlex 7090', 'SN-DELL-001', 1);

-- =============================================================
-- VIEW: visão geral dos chamados (útil para o dashboard)
-- =============================================================
CREATE OR REPLACE VIEW vw_tickets_resumo AS
SELECT
    t.id,
    t.protocolo,
    t.titulo,
    t.prioridade,
    t.status,
    t.nivel_atual,
    t.data_abertura,
    t.data_fechamento,
    t.prazo_sla,
    u_sol.nome  AS solicitante,
    u_tec.nome  AS tecnico,
    c.nome      AS empresa,
    e.nome      AS equipamento,
    -- Calcula se está atrasado
    CASE
        WHEN t.prazo_sla IS NOT NULL AND NOW() > t.prazo_sla
             AND t.status NOT IN ('RESOLVIDO', 'FECHADO')
        THEN TRUE ELSE FALSE
    END AS atrasado
FROM tickets t
LEFT JOIN users u_sol ON u_sol.id = t.solicitante_id
LEFT JOIN users u_tec ON u_tec.id = t.tecnico_id
LEFT JOIN companies c ON c.id = t.company_id
LEFT JOIN equipments e ON e.id = t.equipamento_id;

COMMENT ON VIEW vw_tickets_resumo IS 'View consolidada para exibição dos chamados no dashboard';
