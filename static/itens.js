// Carrega lista de itens e renderiza com filtros

let allItens = [];
let filteredItens = [];

async function loadItens() {
    try {
        const response = await fetch('/api/itens');
        const data = await response.json();
        
        // Remove itens duplicados (mesma descrição e nomeUnidade)
        const uniqueMap = new Map();
        (data.itens || []).forEach(item => {
            const key = `${item.descricao_item}|${item.nomeUnidade}`;
            if (!uniqueMap.has(key)) {
                uniqueMap.set(key, item);
            }
        });
        
        allItens = Array.from(uniqueMap.values());
        filteredItens = [...allItens];
        
        populateOrgaoFilter();
        renderItens();
        updateStats();
    } catch (error) {
        console.error('Erro ao carregar itens:', error);
        document.getElementById('itens-container').innerHTML = 
            '<p style="text-align: center; padding: 40px;">Erro ao carregar itens.</p>';
    }
}

function populateOrgaoFilter() {
    const orgaos = [...new Set(allItens.map(item => item.nomeUnidade).filter(Boolean))].sort();
    const select = document.getElementById('filterOrg');
    
    orgaos.forEach(orgao => {
        const option = document.createElement('option');
        option.value = orgao;
        option.textContent = orgao;
        select.appendChild(option);
    });
}

function renderItens() {
    const container = document.getElementById('itens-container');
    container.innerHTML = '';
    
    if (filteredItens.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 40px;">Nenhum item encontrado.</p>';
        return;
    }
    
    filteredItens.forEach(item => {
        const card = document.createElement('div');
        card.className = 'item-card';
        
        const titulo = item.descricao_item || 'Sem descrição';
        const orgao = item.nomeUnidade || 'Sem órgão';
        const quantidade = item.quantidade_estimada || 0;
        const valor = item.valor_total || 0;
        const data = item.data_desejada ? new Date(item.data_desejada).toLocaleDateString('pt-BR') : 'Sem data';
        
        card.innerHTML = `
            <h4>${truncate(titulo, 50)}</h4>
            <p><strong>Órgão:</strong> ${orgao}</p>
            <p><strong>Quantidade:</strong> ${quantidade}</p>
            <p><strong>Valor Total:</strong> R$ ${valor.toFixed(2)}</p>
            <p><strong>Data Desejada:</strong> ${data}</p>
            <div>
                <span class="item-badge">${item.categoria_item_pca_nome || 'Geral'}</span>
                <span class="item-badge">${item.unidade_fornecimento || 'Un.'}</span>
            </div>
        `;
        
        container.appendChild(card);
    });
}

function truncate(text, length) {
    if (text.length > length) {
        return text.substring(0, length) + '...';
    }
    return text;
}

function updateStats() {
    document.getElementById('totalItens').textContent = filteredItens.length;
}

function filterItens() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const orgaoFilter = document.getElementById('filterOrg').value;
    
    filteredItens = allItens.filter(item => {
        const matchSearch = item.descricao_item && 
                          item.descricao_item.toLowerCase().includes(searchTerm);
        const matchOrgao = !orgaoFilter || item.nomeUnidade === orgaoFilter;
        
        return matchSearch && matchOrgao;
    });
    
    renderItens();
    updateStats();
}

// Event listeners
document.getElementById('searchInput').addEventListener('input', filterItens);
document.getElementById('filterOrg').addEventListener('change', filterItens);

document.getElementById('resetFilters').addEventListener('click', () => {
    document.getElementById('searchInput').value = '';
    document.getElementById('filterOrg').value = '';
    filteredItens = [...allItens];
    renderItens();
    updateStats();
});

// Carrega itens ao abrir página
window.addEventListener('DOMContentLoaded', loadItens);
