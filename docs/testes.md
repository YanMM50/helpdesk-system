# Levantamento de Testes — Help Desk System

**Versão:** 1.1.0
**Data:** 28/03/2026
**Responsável:** Yan Mendes

---

## 1. Objetivo

Este documento registra os testes funcionais realizados no sistema Help Desk, com evidências visuais (prints de tela) comprovando o correto funcionamento das funcionalidades implementadas.

Os testes seguem o conceito de **teste funcional de caixa preta**: verifica-se o comportamento do sistema do ponto de vista do usuário, sem analisar o código interno.

---

## 2. Ambiente de Teste

| Item              | Descrição                                 |
|-------------------|-------------------------------------------|
| Backend           | FastAPI rodando em localhost:8000          |
| Banco de dados    | PostgreSQL via Supabase (cloud)           |
| Navegador         | Google Chrome / Microsoft Edge            |
| Sistema Operacional | Windows 11                              |
| Data dos testes   | 28/03/2026                               |

---

## 3. Casos de Teste

---

### CT-01 — Upload de Fotos ao Abrir Chamado

**Objetivo:** Verificar se o cliente consegue anexar fotos (máx. 3) ao abrir um novo chamado.

**Pré-condição:** Usuário autenticado com acesso à tela "Novo Chamado".

**Passos executados:**
1. Acessar a tela "Novo Chamado"
2. Preencher título, descrição e prioridade
3. Clicar na área de upload de fotos
4. Selecionar uma imagem no formato JPG/PNG/WEBP
5. Verificar o preview da imagem na tela
6. Clicar em "Abrir Chamado"

**Resultado esperado:** Chamado criado com sucesso e foto anexada corretamente.

**Resultado obtido:** ✅ **APROVADO**

**Evidência:**

![CT-01 — Upload de fotos no chamado](../frontend/img/adicionar%20a%20função%20de%20armazena%20foto%20nos%20chamados.jpg)

---

### CT-02 — Administrador Gerencia Cargos dos Colaboradores

**Objetivo:** Verificar se o administrador consegue editar o nível de suporte e cargo de um colaborador.

**Pré-condição:** Usuário autenticado com nível ADMIN e acesso à tela "Usuários".

**Passos executados:**
1. Acessar a tela "Usuários" pelo menu lateral
2. Localizar um colaborador na tabela
3. Clicar no botão "✏️ Editar" da linha do colaborador
4. Alterar o campo "Nível de Suporte" (ex: de N1 para N2)
5. Alterar o campo "Cargo"
6. Clicar em "Salvar Alterações"

**Resultado esperado:** Dados do colaborador atualizados e refletidos na tabela.

**Resultado obtido:** ✅ **APROVADO**

**Evidência:**

![CT-02 — Admin gerencia cargos](../frontend/img/construir%20nova%20função%20admin%20administrar%20cargos%20dos%20colaboradores.jpg)

---

## 4. Resumo dos Resultados

| Caso de Teste | Funcionalidade                          | Resultado   |
|---------------|-----------------------------------------|-------------|
| CT-01         | Upload de fotos ao abrir chamado        | ✅ Aprovado |
| CT-02         | Admin edita cargo/nível de colaborador  | ✅ Aprovado |

**Total de testes executados:** 2
**Aprovados:** 2
**Reprovados:** 0
**Taxa de aprovação:** 100%

---

## 5. Funcionalidades Testadas Informalmente

Além dos casos de teste documentados acima, as seguintes funcionalidades foram validadas durante o desenvolvimento:

| Funcionalidade                          | Resultado   |
|-----------------------------------------|-------------|
| Login com credenciais corretas          | ✅ Aprovado |
| Mensagem de erro com senha incorreta    | ✅ Aprovado |
| Cadastro público de cliente             | ✅ Aprovado |
| Redirecionamento por tipo de usuário    | ✅ Aprovado |
| Background com blur na tela de login    | ✅ Aprovado |
| Ícone do sistema na sidebar e favicon   | ✅ Aprovado |
| Limite de 3 fotos por chamado           | ✅ Aprovado |
| Validação de tipo de arquivo (imagens)  | ✅ Aprovado |

---

## 6. Observações

- Os testes foram realizados com o banco de dados hospedado no **Supabase** (nuvem), confirmando que a aplicação funciona corretamente em ambiente de produção.
- O sistema foi implantado no **Render.com** (branch `PROD`) e testado remotamente, validando o funcionamento fora do ambiente local.
- Todos os bugs identificados durante os testes foram corrigidos antes da documentação deste levantamento.
