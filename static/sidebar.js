// Controla a sidebar

const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebarClose = document.getElementById('sidebarClose');
const sidebarOverlay = document.getElementById('sidebarOverlay');

// Abre a sidebar
function openSidebar() {
    sidebar.classList.add('open');
    sidebarOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
}

// Fecha a sidebar
function closeSidebar() {
    sidebar.classList.remove('open');
    sidebarOverlay.classList.remove('open');
    document.body.style.overflow = 'auto';
}

// Event listeners
if (sidebarToggle) {
    sidebarToggle.addEventListener('click', openSidebar);
}

if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
}

if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
}

// Fecha sidebar ao clicar em um link
document.querySelectorAll('.sidebar-nav a').forEach(link => {
    link.addEventListener('click', closeSidebar);
});

// Fecha sidebar quando a janela é redimensionada para tamanho desktop
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        closeSidebar();
    }
});
