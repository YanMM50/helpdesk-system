/**
 * utils.js — Funções utilitárias reutilizáveis
 */

// ============================================================
// TOAST NOTIFICATIONS
// ============================================================

function showToast(message, type = "info") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all .3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ============================================================
// FORMATAÇÃO
// ============================================================

function formatDate(dateStr) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleString("pt-BR", {
    day: "2-digit", month: "2-digit", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

function formatDateOnly(dateStr) {
  if (!dateStr) return "—";
  const d = new Date(dateStr);
  return d.toLocaleDateString("pt-BR");
}

function formatFileSize(bytes) {
  if (!bytes) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

// ============================================================
// BADGES HTML
// ============================================================

const LABELS = {
  status: {
    ABERTO: "Aberto",
    EM_ANALISE: "Em Análise",
    EM_ATENDIMENTO: "Em Atendimento",
    AGUARDANDO_CLIENTE: "Aguardando",
    RESOLVIDO: "Resolvido",
    FECHADO: "Fechado",
  },
  prioridade: {
    BAIXA: "Baixa",
    MEDIA: "Média",
    ALTA: "Alta",
    CRITICA: "Crítica",
  },
  nivel: {
    N1: "N1",
    N2: "N2",
    N3: "N3",
    ADMIN: "Admin",
  },
  acao: {
    ABERTURA: "Abriu o chamado",
    COMENTARIO: "Comentou",
    MUDANCA_STATUS: "Alterou status",
    ENCAMINHAMENTO: "Encaminhou",
    RESOLUCAO: "Resolveu",
    FECHAMENTO: "Fechou",
    EDICAO: "Editou",
  }
};

function badgeStatus(status) {
  const cls = status.toLowerCase();
  return `<span class="badge badge-${cls}">${LABELS.status[status] || status}</span>`;
}

function badgePrioridade(prioridade) {
  const cls = prioridade.toLowerCase();
  return `<span class="badge badge-${cls}">${LABELS.prioridade[prioridade] || prioridade}</span>`;
}

function badgeNivel(nivel) {
  const cls = nivel.toLowerCase();
  return `<span class="badge badge-${cls}">${LABELS.nivel[nivel] || nivel}</span>`;
}

// ============================================================
// AUTENTICAÇÃO LOCAL
// ============================================================

function getUser() {
  const raw = localStorage.getItem("user");
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

function getToken() {
  return localStorage.getItem("token");
}

function requireAuth() {
  if (!getToken()) {
    window.location.href = "/frontend/index.html";
    return false;
  }
  return true;
}

function logout() {
  localStorage.clear();
  window.location.href = "/frontend/index.html";
}

// ============================================================
// INICIALIZAÇÃO DA SIDEBAR (presente em todas as páginas)
// ============================================================

function initSidebar(activePage) {
  const user = getUser();
  if (!user) return;

  // Preenche dados do usuário na sidebar
  const el = document.getElementById("sidebar-user-name");
  if (el) el.textContent = user.nome.split(" ")[0];

  const elNivel = document.getElementById("sidebar-user-nivel");
  if (elNivel) elNivel.textContent = user.nivel_suporte;

  const avatar = document.getElementById("sidebar-avatar");
  if (avatar) avatar.textContent = user.nome.charAt(0).toUpperCase();

  // Marca o item ativo no menu
  const navItems = document.querySelectorAll(".nav-item[data-page]");
  navItems.forEach((item) => {
    if (item.dataset.page === activePage) item.classList.add("active");
    item.addEventListener("click", () => {
      window.location.href = item.dataset.href;
    });
  });

  // Logout
  const btnLogout = document.getElementById("btn-logout");
  if (btnLogout) btnLogout.addEventListener("click", logout);

  // Oculta itens de admin se não for admin
  if (user.nivel_suporte !== "ADMIN") {
    document.querySelectorAll("[data-admin-only]").forEach((el) => {
      el.style.display = "none";
    });
  }
}

// ============================================================
// MODAL HELPERS
// ============================================================

function openModal(id) {
  document.getElementById(id).classList.remove("hidden");
}

function closeModal(id) {
  document.getElementById(id).classList.add("hidden");
}
