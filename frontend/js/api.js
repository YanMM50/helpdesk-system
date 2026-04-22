/**
 * api.js — Camada de comunicação com o backend
 *
 * Centraliza todas as chamadas HTTP (fetch) para a API.
 * Vantagem: se a URL da API mudar, basta alterar aqui.
 */

const API_BASE = "https://helpdesk-system-aodq.onrender.com";

/**
 * Função base para todas as requisições à API.
 * Adiciona automaticamente o token JWT no cabeçalho.
 * Trata erros de forma padronizada.
 */
async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("token");

  const config = {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
    ...options,
  };

  // Remover Content-Type se for FormData (upload de arquivos)
  if (options.body instanceof FormData) {
    delete config.headers["Content-Type"];
  }

  try {
    const response = await fetch(`${API_BASE}${endpoint}`, config);

    // Token expirado → redirecionar para login (exceto nas páginas públicas)
    if (response.status === 401) {
      const path = window.location.pathname;
      const isPublic = path.endsWith("index.html") || path.endsWith("cadastro.html") || path === "/" || path === "";
      if (!isPublic) {
        localStorage.clear();
        window.location.href = "index.html";
        return;
      }
    }

    const data = response.status !== 204 ? await response.json() : null;

    if (!response.ok) {
      throw new Error(data?.detail || `Erro ${response.status}`);
    }

    return data;
  } catch (err) {
    if (err.name === "TypeError") {
      throw new Error("Não foi possível conectar ao servidor. Verifique se o backend está rodando.");
    }
    throw err;
  }
}

// ============================================================
// AUTH
// ============================================================
const Auth = {
  login: (email, senha) =>
    apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, senha }),
    }),

  register: (nome, email, senha) =>
    apiRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify({ nome, email, senha }),
    }),

  me: () => apiRequest("/auth/me"),

  alterarSenha: (senha_atual, nova_senha) =>
    apiRequest("/auth/me/senha", {
      method: "PATCH",
      body: JSON.stringify({ senha_atual, nova_senha }),
    }),
};

// ============================================================
// TICKETS
// ============================================================
const Tickets = {
  list: (params = {}) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params).filter(([, v]) => v != null && v !== ""))
    ).toString();
    return apiRequest(`/tickets${qs ? "?" + qs : ""}`);
  },

  get: (id) => apiRequest(`/tickets/${id}`),

  create: (data) =>
    apiRequest("/tickets", { method: "POST", body: JSON.stringify(data) }),

  update: (id, data) =>
    apiRequest(`/tickets/${id}`, { method: "PUT", body: JSON.stringify(data) }),

  updateStatus: (id, data) =>
    apiRequest(`/tickets/${id}/status`, { method: "PATCH", body: JSON.stringify(data) }),

  encaminhar: (id, data) =>
    apiRequest(`/tickets/${id}/encaminhar`, { method: "POST", body: JSON.stringify(data) }),

  comentar: (id, comentario) =>
    apiRequest(`/tickets/${id}/comentarios`, {
      method: "POST",
      body: JSON.stringify({ comentario }),
    }),

  uploadAnexo: (id, file) => {
    const form = new FormData();
    form.append("file", file);
    return apiRequest(`/tickets/${id}/anexos`, { method: "POST", body: form });
  },
  aceitar: (id) =>
    apiRequest(`/tickets/${id}/aceitar`, { method: "PATCH" }),
  avaliar: (id, nota) =>
    apiRequest(`/tickets/${id}/avaliar?nota=${nota}`, { method: "PATCH" }),
};

// ============================================================
// USUÁRIOS
// ============================================================
const Users = {
  list: () => apiRequest("/users"),
  get: (id) => apiRequest(`/users/${id}`),
  create: (data) =>
    apiRequest("/users", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) =>
    apiRequest(`/users/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id) =>
    apiRequest(`/users/${id}`, { method: "DELETE" }),
};

// ============================================================
// EMPRESAS
// ============================================================
const Companies = {
  list: () => apiRequest("/companies"),
  get: (id) => apiRequest(`/companies/${id}`),
  create: (data) =>
    apiRequest("/companies", { method: "POST", body: JSON.stringify(data) }),
  delete: (id) =>
    apiRequest(`/companies/${id}`, { method: "DELETE" }),
};

// ============================================================
// EQUIPAMENTOS
// ============================================================
const Equipments = {
  list: () => apiRequest("/equipments"),
  get: (id) => apiRequest(`/equipments/${id}`),
  create: (data) =>
    apiRequest("/equipments", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) =>
    apiRequest(`/equipments/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id) =>
    apiRequest(`/equipments/${id}`, { method: "DELETE" }),
};

// ============================================================
// DASHBOARD
// ============================================================
const Dashboard = {
  resumo: () => apiRequest("/dashboard/resumo"),
};
