# Plano de Manutenção de Software
## Sistema de Gestão de Chamados Técnicos (Help Desk)

**Versão:** 1.0.0
**Data:** 2024
**Baseado em:** ISO/IEC 14764 — Manutenção de Software

---

## 1. Introdução

Este documento define o **Plano de Manutenção de Software** do Sistema Help Desk. Ele estabelece os tipos de manutenção, responsabilidades, calendário de atividades e procedimentos operacionais necessários para garantir a continuidade, segurança e evolução do sistema.

A manutenção de software é uma fase crítica do ciclo de vida do sistema — ela começa após a entrega e dura enquanto o sistema estiver em operação. Segundo a ISO/IEC 14764, estima-se que **60% a 80% do custo total de um sistema** seja gasto em manutenção.

---

## 2. Tipos de Manutenção (ISO/IEC 14764)

### 2.1 Manutenção Corretiva

**Objetivo:** Corrigir falhas, bugs e erros identificados após a entrega do sistema.

**Quando ocorre:** Quando um erro é reportado por usuário ou detectado em monitoramento.

**Exemplos no Help Desk:**
- Bug que impede o upload de anexos
- Erro no cálculo de estatísticas do dashboard
- Token JWT não sendo renovado corretamente
- Falha na geração do número de protocolo

**Procedimento:**
1. Usuário ou monitoramento detecta a falha
2. Técnico registra o bug com evidências (log, print, passos para reproduzir)
3. Desenvolvedor analisa, reproduz e identifica a causa raiz
4. Correção é implementada e testada em ambiente de desenvolvimento
5. Correção é aplicada em produção fora do horário de pico
6. Registro da correção no controle de versão (Git) com tag de versão patch (ex: v1.0.1)

**Prioridade de atendimento:**

| Severidade | Descrição                              | Prazo de correção |
|------------|----------------------------------------|-------------------|
| Crítica    | Sistema indisponível ou dados perdidos | 4 horas           |
| Alta       | Funcionalidade principal afetada       | 24 horas          |
| Média      | Funcionalidade secundária afetada      | 72 horas          |
| Baixa      | Estético ou de baixo impacto           | Próximo sprint    |

---

### 2.2 Manutenção Adaptativa

**Objetivo:** Adaptar o sistema a mudanças no ambiente externo sem alterar a funcionalidade.

**Quando ocorre:** Quando há mudanças em tecnologias, infraestrutura ou regulamentações.

**Exemplos no Help Desk:**
- Atualização do Python de 3.11 para 3.12 ou superior
- Migração do banco de dados para nova versão do PostgreSQL
- Adequação à Lei Geral de Proteção de Dados (LGPD)
- Mudança do servidor de hospedagem (ex: de VPS para nuvem)
- Atualização das dependências (FastAPI, SQLAlchemy) por vulnerabilidades

**Procedimento:**
1. Identificar a necessidade de adaptação (monitoramento de versões ou regulamentações)
2. Avaliar o impacto na aplicação atual
3. Criar ambiente de testes idêntico ao de produção
4. Aplicar as mudanças e executar todos os testes
5. Documentar as mudanças e atualizar o `requirements.txt`
6. Migrar para produção com plano de rollback pronto
7. Atualizar a documentação técnica

---

### 2.3 Manutenção Evolutiva (ou Perfectiva)

**Objetivo:** Adicionar novas funcionalidades ou melhorar funcionalidades existentes a pedido dos usuários ou da gestão.

**Quando ocorre:** Quando há requisitos novos ou oportunidades de melhoria identificadas.

**Exemplos de evoluções planejadas para o Help Desk:**

| Prioridade | Funcionalidade                              | Justificativa                         |
|------------|---------------------------------------------|---------------------------------------|
| Alta       | Notificações por e-mail                     | Alertar técnicos sobre novos chamados |
| Alta       | Relatórios em PDF/Excel                     | Gestão e auditoria                    |
| Média      | App mobile (PWA)                            | Acesso via smartphone                 |
| Média      | Integração com Active Directory (LDAP)      | Login com conta corporativa           |
| Média      | Chatbot de triagem (N1 automatizado)        | Reduzir carga de trabalho             |
| Baixa      | Módulo de base de conhecimento              | Soluções documentadas                 |
| Baixa      | Agendamento de manutenções preventivas      | Proatividade no suporte               |

**Procedimento:**
1. Requisito é levantado e documentado
2. Análise de impacto e estimativa de esforço
3. Aprovação pela gestão
4. Desenvolvimento em branch separada no Git
5. Testes unitários e de integração
6. Code review por outro desenvolvedor
7. Merge na branch principal e deploy planejado
8. Treinamento dos usuários para a nova funcionalidade

---

### 2.4 Manutenção Preventiva

**Objetivo:** Identificar e corrigir potenciais problemas antes que causem falhas, melhorando a estabilidade e manutenibilidade do sistema.

**Quando ocorre:** Em intervalos regulares, conforme o calendário de manutenção.

**Exemplos no Help Desk:**
- Refatoração de código complexo para melhor legibilidade
- Adição de logs detalhados em operações críticas
- Otimização de queries lentas identificadas no monitoramento
- Remoção de código morto (dead code)
- Atualização de comentários e documentação desatualizados
- Revisão das políticas de backup

**Procedimento:**
1. Análise estática do código (ex: flake8, pylint)
2. Revisão do desempenho das queries mais utilizadas (EXPLAIN ANALYZE)
3. Verificação de acúmulo de logs antigos (rotação de logs)
4. Validação da integridade dos backups
5. Teste dos procedimentos de recuperação de desastres (DR)
6. Documentação das melhorias realizadas

---

## 3. Calendário de Manutenção

### 3.1 Rotina Diária

| Tarefa                              | Responsável      | Horário Sugerido |
|-------------------------------------|------------------|-----------------|
| Backup completo do banco de dados   | Automatizado/DBA | 02:00           |
| Backup dos arquivos de upload       | Automatizado     | 02:30           |
| Verificação de espaço em disco      | Automatizado     | 06:00           |
| Verificação do status dos serviços  | Automatizado     | A cada 5 min    |
| Revisão dos alertas do monitoramento| Técnico N3       | Início do dia   |

**Script de backup recomendado (PostgreSQL):**
```bash
#!/bin/bash
# backup_diario.sh
DATA=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/helpdesk"
mkdir -p $BACKUP_DIR

# Dump do banco de dados
pg_dump -U postgres helpdesk_db | gzip > "$BACKUP_DIR/db_$DATA.sql.gz"

# Backup dos uploads
tar -czf "$BACKUP_DIR/uploads_$DATA.tar.gz" /app/uploads/

# Remove backups com mais de 30 dias
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Backup concluído: $DATA"
```

### 3.2 Rotina Semanal

| Tarefa                                    | Responsável   |
|-------------------------------------------|---------------|
| Análise dos logs de erro da semana        | Técnico N2/N3 |
| Verificação de tentativas de login falhas | Técnico N3    |
| Revisão de chamados com SLA vencido       | Gestor        |
| Teste de restauração de backup            | DBA           |
| Atualização de patches de segurança leves | Técnico N3    |

### 3.3 Rotina Mensal

| Tarefa                                         | Responsável   |
|------------------------------------------------|---------------|
| Aplicação de atualizações de segurança         | Técnico N3    |
| Revisão de usuários inativos                   | Administrador |
| Análise de métricas de desempenho              | Técnico N3    |
| Revisão dos logs de acesso                     | Técnico N3    |
| Teste completo das funcionalidades principais  | Equipe QA     |
| Relatório mensal de chamados para a gestão     | Gestor        |
| Verificação das permissões de acesso           | Administrador |

### 3.4 Rotina Trimestral

| Tarefa                                              | Responsável        |
|-----------------------------------------------------|--------------------|
| Revisão completa de desempenho e gargalos           | Técnico N3         |
| Análise de crescimento do banco de dados            | DBA                |
| Atualização das dependências do projeto             | Desenvolvedor      |
| Revisão do plano de manutenção                      | Gestor + Técnico   |
| Teste de plano de contingência (simulação de falha) | Toda a equipe      |
| Avaliação de novas funcionalidades a implementar    | Gestor             |
| Análise de satisfação dos usuários                  | Gestor             |

### 3.5 Rotina Anual

| Tarefa                                                   | Responsável        |
|----------------------------------------------------------|--------------------|
| Auditoria completa de segurança                          | Especialista externo |
| Revisão e atualização do Plano de Manutenção             | Gestor + Equipe    |
| Avaliação de migração para tecnologias mais recentes     | Arquiteto          |
| Revisão de conformidade com normas ISO                   | Responsável ISO    |
| Renovação de certificados SSL/TLS                        | Técnico N3         |
| Revisão da política de backup e retenção de dados        | DBA + Gestor       |
| Treinamento anual de segurança da informação             | Todos os usuários  |

---

## 4. Plano de Contingência e Recuperação de Desastres

### 4.1 Cenários de Falha

| Cenário                       | Probabilidade | Impacto   | Ação de Resposta                           |
|-------------------------------|---------------|-----------|--------------------------------------------|
| Banco de dados indisponível   | Baixa         | Crítico   | Restore do último backup + failover        |
| Servidor web derrubado        | Média         | Alto      | Reiniciar serviço + verificar logs         |
| Disco cheio                   | Média         | Alto      | Limpeza de logs antigos + expansão         |
| Ataque de força bruta         | Média         | Médio     | Bloqueio de IP + revisão de senhas         |
| Vazamento de credenciais      | Baixa         | Crítico   | Rotação de todas as chaves e senhas        |
| Corrupção de dados            | Muito baixa   | Crítico   | Restore do último backup íntegro           |

### 4.2 RTO e RPO

- **RTO (Recovery Time Objective):** Tempo máximo para restaurar o sistema = **4 horas**
- **RPO (Recovery Point Objective):** Perda máxima de dados aceitável = **24 horas** (backup diário)

### 4.3 Procedimento de Restauração do Banco

```bash
# 1. Parar a aplicação
systemctl stop helpdesk

# 2. Restaurar o backup do banco
gunzip < /backups/helpdesk/db_20241201_020000.sql.gz | psql -U postgres helpdesk_db

# 3. Restaurar os uploads
tar -xzf /backups/helpdesk/uploads_20241201_020000.tar.gz -C /app/

# 4. Reiniciar a aplicação
systemctl start helpdesk

# 5. Verificar integridade
curl http://localhost:8000/health
```

---

## 5. Monitoramento e Métricas

### 5.1 Métricas de Desempenho a Acompanhar

| Métrica                          | Meta          | Alerta em      |
|----------------------------------|---------------|----------------|
| Tempo de resposta da API         | < 500ms       | > 2000ms       |
| Uso de CPU do servidor           | < 70%         | > 90%          |
| Uso de memória                   | < 80%         | > 95%          |
| Espaço em disco                  | < 70%         | > 85%          |
| Conexões ativas no banco         | < 80% do pool | > 95% do pool  |
| Taxa de erros HTTP 5xx           | < 0.1%        | > 1%           |
| Chamados sem resposta há 24h     | 0             | > 5            |

### 5.2 Ferramentas Recomendadas

- **Monitoramento de servidor:** Prometheus + Grafana (gratuito e open source)
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana) ou simples arquivos de log
- **Uptime:** UptimeRobot (gratuito até 50 monitores)
- **Alertas:** Integração com e-mail ou Telegram

---

## 6. Treinamento da Equipe

### 6.1 Matriz de Treinamento

| Módulo                                 | N1  | N2  | N3  | Admin | Periodicidade |
|----------------------------------------|-----|-----|-----|-------|---------------|
| Uso básico do sistema (abertura/status)| ✓   | ✓   | ✓   | ✓     | Admissão      |
| Registro correto de chamados           | ✓   | ✓   | ✓   | ✓     | Admissão      |
| Fluxo entre níveis (N1→N2→N3)         | ✓   | ✓   | ✓   | ✓     | Admissão      |
| Uso do histórico e evidências          | ✓   | ✓   | ✓   | ✓     | Admissão      |
| Técnicas de diagnóstico N2             |     | ✓   | ✓   |       | Admissão + 6m |
| Procedimentos de engenharia N3         |     |     | ✓   |       | Admissão + 6m |
| Gestão de usuários e permissões        |     |     |     | ✓     | Admissão      |
| Procedimentos de backup e restore      |     |     | ✓   | ✓     | Anual         |
| Segurança da informação                | ✓   | ✓   | ✓   | ✓     | Anual         |
| Plano de contingência                  |     | ✓   | ✓   | ✓     | Anual         |
| LGPD e proteção de dados               | ✓   | ✓   | ✓   | ✓     | Anual         |

### 6.2 Conteúdo por Módulo

#### Módulo 1 — Uso Básico do Sistema
- Acesso e autenticação
- Abertura de chamados: preenchimento correto de título, descrição e prioridade
- Consulta de chamados e uso de filtros
- Adição de comentários e evidências (fotos)
- Verificação do status de um chamado

#### Módulo 2 — Fluxo entre Níveis de Suporte
- Diferença entre N1, N2 e N3
- Quando encaminhar (critérios objetivos)
- Como encaminhar pelo sistema
- Importância de documentar o motivo do encaminhamento
- Boas práticas de comunicação com o cliente

#### Módulo 3 — Segurança da Informação
- Política de senhas (mínimo 8 caracteres, trocas periódicas)
- Nunca compartilhar credenciais de acesso
- Identificação de phishing e engenharia social
- Proteção de dados dos clientes (LGPD)
- Procedimento em caso de suspeita de incidente de segurança

#### Módulo 4 — Procedimentos de Contingência
- Identificação de situações de emergência
- Contato com responsáveis técnicos
- Procedimento de escalonamento
- Comunicação com clientes durante indisponibilidade
- Registro do incidente

---

## 7. Controle de Versão e Releases

### 7.1 Convenção de Versionamento (Semantic Versioning)

O projeto adota o padrão **MAJOR.MINOR.PATCH** (ex: v1.2.3):

- **PATCH** (último número): Correção de bugs sem novos recursos. Ex: v1.0.1
- **MINOR** (número do meio): Nova funcionalidade sem quebrar compatibilidade. Ex: v1.1.0
- **MAJOR** (primeiro número): Mudança significativa ou incompatível. Ex: v2.0.0

### 7.2 Branches Git

```
main          ← código estável em produção (protegido)
  └── develop ← integração de novas funcionalidades
        ├── feature/notificacoes-email
        ├── feature/relatorios-pdf
        └── fix/bug-upload-anexo
```

### 7.3 Processo de Deploy (subida para produção)

1. Desenvolver em branch `feature/` ou `fix/`
2. Abrir Pull Request para `develop`
3. Code review por outro membro da equipe
4. Testes automatizados (se houver)
5. Merge em `develop` e teste em ambiente de homologação
6. Aprovação do gestor
7. Merge em `main` com tag de versão
8. Deploy em produção fora do horário de pico
9. Monitoramento pós-deploy por 1 hora

---

## 8. Responsáveis e Contatos

| Papel                       | Responsabilidade                              |
|-----------------------------|-----------------------------------------------|
| Gestor de TI                | Aprovação de mudanças, relatórios gerenciais  |
| Técnico N3 / Desenvolvedor  | Manutenção corretiva, evolutiva e preventiva  |
| DBA                         | Backup, restore, otimização do banco          |
| Técnico N2                  | Suporte avançado, monitoramento               |
| Técnico N1                  | Suporte básico, triagem de chamados           |

---

## 9. Registro de Manutenções Realizadas

Toda manutenção realizada deve ser documentada conforme o modelo abaixo:

| Data       | Tipo         | Descrição                          | Responsável | Versão |
|------------|--------------|------------------------------------|-------------|--------|
| 2024-01-15 | Corretiva    | Correção do bug de upload em PNG   | Carlos N3   | v1.0.1 |
| 2024-02-01 | Preventiva   | Otimização de índices do banco     | Ana DBA     | v1.0.1 |
| 2024-03-01 | Adaptativa   | Atualização FastAPI 0.110→0.111    | Carlos N3   | v1.0.2 |
| 2024-04-01 | Evolutiva    | Implementação de notif. por email  | Carlos N3   | v1.1.0 |

---

*Este Plano de Manutenção deve ser revisado trimestralmente e atualizado sempre que houver mudanças significativas no sistema ou na equipe.*
