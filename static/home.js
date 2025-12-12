// Mock data para simular 15 compras compartilhadas
const comprasCompartilhadas = [
    {
        id: 1,
        item: 'Papel A4 75g/m² - Resma com 500 folhas',
        nomeUnidade: 'Prefeitura de Campinas',
        quantidadeEstimada: 500,
        orgaosParticipantes: ['Prefeitura de Campinas', 'Secretaria de Educação', 'Secretaria de Saúde', 'DETRAN']
    },
    {
        id: 2,
        item: 'Toner para impressora HP LaserJet',
        nomeUnidade: 'Secretaria de Educação RR',
        quantidadeEstimada: 150,
        orgaosParticipantes: ['Secretaria de Educação RR', 'Prefeitura Municipal', 'Câmara Municipal']
    },
    {
        id: 3,
        item: 'Caneta azul esferográfica - Caixa com 50',
        nomeUnidade: 'DETRAN',
        quantidadeEstimada: 300,
        orgaosParticipantes: ['DETRAN', 'Prefeitura Municipal', 'Secretaria de Educação', 'Secretaria de Saúde', 'Câmara Municipal']
    },
    {
        id: 4,
        item: 'Cadernos 200 folhas - Lote com 100',
        nomeUnidade: 'Secretaria de Saúde',
        quantidadeEstimada: 200,
        orgaosParticipantes: ['Secretaria de Saúde', 'Secretaria de Educação', 'Prefeitura Municipal']
    },
    {
        id: 5,
        item: 'Pastas suspensas - Caixa com 50',
        nomeUnidade: 'Câmara Municipal',
        quantidadeEstimada: 100,
        orgaosParticipantes: ['Câmara Municipal', 'Prefeitura Municipal', 'Secretaria de Educação', 'DETRAN']
    },
    {
        id: 6,
        item: 'Clipes niquelados número 4/0 - Caixa com 1000',
        nomeUnidade: 'Prefeitura Municipal',
        quantidadeEstimada: 2000,
        orgaosParticipantes: ['Prefeitura Municipal', 'Secretaria de Saúde', 'Câmara Municipal']
    },
    {
        id: 7,
        item: 'Envelopes brancos 162x229mm - Caixa com 100',
        nomeUnidade: 'Secretaria de Educação',
        quantidadeEstimada: 500,
        orgaosParticipantes: ['Secretaria de Educação', 'DETRAN', 'Prefeitura Municipal', 'Secretaria de Saúde']
    },
    {
        id: 8,
        item: 'Lápis HB - Caixa com 72',
        nomeUnidade: 'DETRAN',
        quantidadeEstimada: 400,
        orgaosParticipantes: ['DETRAN', 'Secretaria de Educação', 'Prefeitura Municipal']
    },
    {
        id: 9,
        item: 'Borracha branca - Pacote com 50',
        nomeUnidade: 'Secretaria de Saúde',
        quantidadeEstimada: 250,
        orgaosParticipantes: ['Secretaria de Saúde', 'Prefeitura Municipal', 'Secretaria de Educação', 'DETRAN', 'Câmara Municipal']
    },
    {
        id: 10,
        item: 'Estojo organizador para mesa',
        nomeUnidade: 'Câmara Municipal',
        quantidadeEstimada: 150,
        orgaosParticipantes: ['Câmara Municipal', 'Secretaria de Educação', 'Prefeitura Municipal']
    },
    {
        id: 11,
        item: 'Fita adesiva 50mm x 50m - Rolo',
        nomeUnidade: 'Prefeitura Municipal',
        quantidadeEstimada: 350,
        orgaosParticipantes: ['Prefeitura Municipal', 'DETRAN', 'Secretaria de Saúde', 'Câmara Municipal', 'Secretaria de Educação']
    },
    {
        id: 12,
        item: 'Tesoura de corte reto 21cm',
        nomeUnidade: 'Secretaria de Educação',
        quantidadeEstimada: 200,
        orgaosParticipantes: ['Secretaria de Educação', 'Prefeitura Municipal', 'DETRAN']
    },
    {
        id: 13,
        item: 'Apontador com depósito - Pacote com 30',
        nomeUnidade: 'DETRAN',
        quantidadeEstimada: 180,
        orgaosParticipantes: ['DETRAN', 'Secretaria de Educação', 'Secretaria de Saúde']
    },
    {
        id: 14,
        item: 'Marca-página - Caixa com 100',
        nomeUnidade: 'Secretaria de Saúde',
        quantidadeEstimada: 300,
        orgaosParticipantes: ['Secretaria de Saúde', 'Prefeitura Municipal', 'Câmara Municipal', 'Secretaria de Educação']
    },
    {
        id: 15,
        item: 'Luvas de nitrilo para serviços gerais - Caixa com 100',
        nomeUnidade: 'Câmara Municipal',
        quantidadeEstimada: 500,
        orgaosParticipantes: ['Câmara Municipal', 'Prefeitura Municipal', 'Secretaria de Saúde']
    }
];

// Função para carregar compras compartilhadas
function carregarComprasCompartilhadas() {
    const container = document.getElementById('active-purchases');
    container.innerHTML = '';

    comprasCompartilhadas.forEach(compra => {
        const numParticipantesExtras = compra.orgaosParticipantes.length - 1;
        
        const div = document.createElement('div');
        div.className = 'purchase-item';
        div.innerHTML = `
            <span class="purchase-icon">📦</span>
            <div class="purchase-info">
                <h4>${compra.item}</h4>
                <p><strong>Órgão Responsável:</strong> ${compra.nomeUnidade}</p>
            </div>
            <span class="count">+${numParticipantesExtras}</span>
        `;
        container.appendChild(div);
    });
}

// Carrega compras ao abrir página
window.addEventListener('DOMContentLoaded', carregarComprasCompartilhadas);
