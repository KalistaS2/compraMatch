// Lista de prefeituras e secretarias brasileiras para mock data
const orgaosBrasileiros = [
    'Prefeitura de São Paulo', 'Prefeitura de Rio de Janeiro', 'Prefeitura de Belo Horizonte', 'Prefeitura de Brasília', 'Prefeitura de Salvador',
    'Prefeitura de Fortaleza', 'Prefeitura de Manaus', 'Prefeitura de Curitiba', 'Prefeitura de Recife', 'Prefeitura de Porto Alegre',
    'Prefeitura de Belém', 'Prefeitura de Goiânia', 'Prefeitura de Guarulhos', 'Prefeitura de Campinas', 'Prefeitura de São Bernardo do Campo',
    'Prefeitura de Santo André', 'Prefeitura de Osasco', 'Prefeitura de Sorocaba', 'Prefeitura de Ribeirão Preto', 'Prefeitura de Piracicaba',
    'Prefeitura de Caruaru', 'Prefeitura de Petrolina', 'Prefeitura de Maceió', 'Prefeitura de Teresina', 'Prefeitura de São Luís',
    'Prefeitura de Natal', 'Prefeitura de João Pessoa', 'Prefeitura de Aracaju', 'Prefeitura de Macapá', 'Prefeitura de Boa Vista',
    'Secretaria de Educação SP', 'Secretaria de Saúde SP', 'Secretaria de Educação RJ', 'Secretaria de Saúde RJ', 'Secretaria de Educação MG',
    'Secretaria de Saúde MG', 'DETRAN SP', 'DETRAN RJ', 'DETRAN MG', 'Câmara Municipal SP',
    'Câmara Municipal RJ', 'Câmara Municipal MG', 'Delegacia Regional São Paulo', 'Delegacia Regional Rio de Janeiro', 'Delegacia Regional Minas Gerais',
    'Secretaria de Infraestrutura SP', 'Secretaria de Transportes SP', 'DAEE SP', 'SABESP SP', 'Polícia Militar SP',
    'Polícia Civil SP', 'Bombeiros SP', 'CEAGESP', 'Companhia de Iluminação Pública SP', 'Secretaria de Bem Estar Social SP',
    'Secretaria de Cultura SP', 'Secretaria de Turismo SP', 'SESC SP', 'SENAC SP', 'Fundação para o Bem Estar do Idoso',
    'Instituto da Criança SP', 'EMAE SP', 'CDHU SP', 'Desenvolve SP', 'Agência de Fomento São Paulo',
    'Casa da Moeda', 'Banco do Brasil', 'Caixa Econômica Federal', 'Banco do Nordeste', 'Sudene',
    'Sudam', 'Codevasf', 'Incra', 'Funai', 'Anvisa',
    'Inmetro', 'Instituto Butantan', 'Fundação Oswaldo Cruz', 'Unifesp', 'UFRJ',
    'UFMG', 'USP', 'Unicamp', 'Unesp', 'ITA',
    'INPE', 'Embrapa', 'CNPq', 'Capes', 'Fapesp',
    'Instituto Nacional de Pesquisas da Amazônia', 'INPA', 'Museu Goeldi', 'Museu Nacional', 'Museu de Arte de São Paulo',
    'Museu de Arte do Rio', 'Instituto Moreira Salles', 'Pinacoteca do Estado', 'MASP', 'Memorial da América Latina',
    'Sesc Pompéia', 'Sesc 25 de Março', 'Sesc Ribeirão Preto', 'Sesc Guarulhos', 'Sesc Itanhaém',
    'ETEC São Paulo', 'FATEC São Paulo', 'Instituto Federal de São Paulo', 'Instituto Federal do Rio de Janeiro', 'Instituto Federal de Minas Gerais',
    'Instituto Federal de Brasília', 'Instituto Federal de Salvador', 'Instituto Federal de Fortaleza', 'Instituto Federal de Manaus', 'Instituto Federal de Curitiba',
    'Instituto Federal de Recife', 'Instituto Federal de Porto Alegre', 'Instituto Federal de Belém', 'Instituto Federal de Goiânia', 'Instituto Federal de Guarulhos',
    'Corpo de Bombeiros SP', 'Corpo de Bombeiros RJ', 'Corpo de Bombeiros MG', 'Defesa Civil SP', 'Defesa Civil RJ',
    'Defesa Civil MG', 'Polícia Rodoviária Federal', 'Polícia Federal', 'Receita Federal', 'Alfândega de São Paulo',
    'Serviço Florestal Brasileiro', 'ICMBio', 'Ibama', 'Instituto Chico Mendes', 'Parque Nacional da Tijuca',
    'Parque Nacional de Brasília', 'Parque Nacional da Serra da Capivara', 'ANA', 'Agência Nacional de Energia', 'Anatel',
    'Agência Nacional de Aviação Civil', 'Agência Nacional de Transportes Terrestres', 'Agência Nacional de Transportes Aquaviários', 'Marinha do Brasil', 'Aeronáutica',
    'Exército Brasileiro', 'Força Aérea Brasileira', 'Ministério da Justiça', 'Ministério das Cidades', 'Ministério da Fazenda',
    'Ministério da Agricultura', 'Ministério da Saúde', 'Ministério da Educação', 'Ministério do Trabalho', 'Ministério da Integração',
    'Ministério do Meio Ambiente', 'Ministério da Ciência e Tecnologia', 'Ministério da Cultura', 'Ministério do Turismo', 'Ministério do Esporte',
    'Ministério das Mulheres', 'Ministério da Igualdade Racial', 'Ministério dos Direitos Humanos', 'Ministério da Communicação', 'Ministério da Governança',
    'Tribunal de Justiça SP', 'Tribunal de Justiça RJ', 'Tribunal de Justiça MG', 'Tribunal Federal', 'Tribunal Superior do Trabalho',
    'Tribunal de Contas da União', 'Tribunal de Contas de SP', 'Tribunal de Contas de RJ', 'Tribunal de Contas de MG', 'Superior Tribunal de Justiça'
];

// Função para gerar órgãos participantes aleatórios
function gerarOrgaosParticipantes(orgaoResponsavel) {
    const quantidade = Math.floor(Math.random() * (300 - 50 + 1)) + 50; // Entre 50-300
    const orgaosUnicos = new Set([orgaoResponsavel]);
    const orgaosDisponiveis = orgaosBrasileiros.filter(o => o !== orgaoResponsavel);
    
    while (orgaosUnicos.size < quantidade && orgaosDisponiveis.length > 0) {
        const indice = Math.floor(Math.random() * orgaosDisponiveis.length);
        orgaosUnicos.add(orgaosDisponiveis[indice]);
        orgaosDisponiveis.splice(indice, 1);
    }
    
    return Array.from(orgaosUnicos);
}

// Mock data para simular 15 compras compartilhadas
const comprasCompartilhadas = [
    {
        id: 1,
        item: 'Papel A4 75g/m² - Resma com 500 folhas',
        nomeUnidade: 'Prefeitura de São Paulo',
        quantidadeEstimada: 5000,
        orgaosParticipantes: gerarOrgaosParticipantes('Prefeitura de São Paulo')
    },
    {
        id: 2,
        item: 'Toner para impressora HP LaserJet',
        nomeUnidade: 'Secretaria de Educação SP',
        quantidadeEstimada: 1500,
        orgaosParticipantes: gerarOrgaosParticipantes('Secretaria de Educação SP')
    },
    {
        id: 3,
        item: 'Caneta azul esferográfica - Caixa com 50',
        nomeUnidade: 'Prefeitura de Rio de Janeiro',
        quantidadeEstimada: 3000,
        orgaosParticipantes: gerarOrgaosParticipantes('Prefeitura de Rio de Janeiro')
    },
    {
        id: 4,
        item: 'Cadernos 200 folhas - Lote com 100',
        nomeUnidade: 'Secretaria de Educação RJ',
        quantidadeEstimada: 2000,
        orgaosParticipantes: gerarOrgaosParticipantes('Secretaria de Educação RJ')
    },
    {
        id: 5,
        item: 'Pastas suspensas - Caixa com 50',
        nomeUnidade: 'Prefeitura de Belo Horizonte',
        quantidadeEstimada: 1000,
        orgaosParticipantes: gerarOrgaosParticipantes('Prefeitura de Belo Horizonte')
    },
    {
        id: 6,
        item: 'Clipes niquelados número 4/0 - Caixa com 1000',
        nomeUnidade: 'Secretaria de Saúde MG',
        quantidadeEstimada: 2000,
        orgaosParticipantes: gerarOrgaosParticipantes('Secretaria de Saúde MG')
    },
    {
        id: 7,
        item: 'Envelopes brancos 162x229mm - Caixa com 100',
        nomeUnidade: 'Prefeitura de Brasília',
        quantidadeEstimada: 5000,
        orgaosParticipantes: gerarOrgaosParticipantes('Prefeitura de Brasília')
    },
    {
        id: 8,
        item: 'Lápis HB - Caixa com 72',
        nomeUnidade: 'DETRAN SP',
        quantidadeEstimada: 4000,
        orgaosParticipantes: gerarOrgaosParticipantes('DETRAN SP')
    },
    {
        id: 9,
        item: 'Borracha branca - Pacote com 50',
        nomeUnidade: 'Secretaria de Saúde SP',
        quantidadeEstimada: 2500,
        orgaosParticipantes: gerarOrgaosParticipantes('Secretaria de Saúde SP')
    },
    {
        id: 10,
        item: 'Estojo organizador para mesa',
        nomeUnidade: 'Câmara Municipal SP',
        quantidadeEstimada: 1500,
        orgaosParticipantes: gerarOrgaosParticipantes('Câmara Municipal SP')
    },
    {
        id: 11,
        item: 'Fita adesiva 50mm x 50m - Rolo',
        nomeUnidade: 'Prefeitura de Fortaleza',
        quantidadeEstimada: 3500,
        orgaosParticipantes: gerarOrgaosParticipantes('Prefeitura de Fortaleza')
    },
    {
        id: 12,
        item: 'Tesoura de corte reto 21cm',
        nomeUnidade: 'Prefeitura de Salvador',
        quantidadeEstimada: 2000,
        orgaosParticipantes: gerarOrgaosParticipantes('Prefeitura de Salvador')
    },
    {
        id: 13,
        item: 'Apontador com depósito - Pacote com 30',
        nomeUnidade: 'DETRAN RJ',
        quantidadeEstimada: 1800,
        orgaosParticipantes: gerarOrgaosParticipantes('DETRAN RJ')
    },
    {
        id: 14,
        item: 'Marca-página - Caixa com 100',
        nomeUnidade: 'Secretaria de Saúde RJ',
        quantidadeEstimada: 3000,
        orgaosParticipantes: gerarOrgaosParticipantes('Secretaria de Saúde RJ')
    },
    {
        id: 15,
        item: 'Luvas de nitrilo para serviços gerais - Caixa com 100',
        nomeUnidade: 'Prefeitura de Curitiba',
        quantidadeEstimada: 5000,
        orgaosParticipantes: gerarOrgaosParticipantes('Prefeitura de Curitiba')
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
        div.style.cursor = 'pointer';
        div.onclick = () => abrirModal(compra);
        container.appendChild(div);
    });
}

// Função para abrir modal com detalhes da compra
function abrirModal(compra) {
    document.getElementById('modal-title').textContent = 'Detalhes da Compra';
    document.getElementById('modal-item').textContent = compra.item;
    document.getElementById('modal-unidade').textContent = compra.nomeUnidade;
    document.getElementById('modal-quantidade').textContent = compra.quantidadeEstimada + ' unidades';
    
    // Preenche lista de órgãos participantes
    const orgaosDiv = document.getElementById('modal-orgaos');
    orgaosDiv.innerHTML = '';
    compra.orgaosParticipantes.forEach(orgao => {
        const span = document.createElement('span');
        span.className = 'orgao-badge';
        span.textContent = orgao;
        orgaosDiv.appendChild(span);
    });
    
    // Abre o modal
    document.getElementById('purchaseModal').style.display = 'block';
}

// Função para fechar modal
function fecharModal() {
    document.getElementById('purchaseModal').style.display = 'none';
}

// Função para ingressar na compra
function ingressarCompra() {
    const item = document.getElementById('modal-item').textContent;
    const unidade = document.getElementById('modal-unidade').textContent;
    
    // Cria mensagem de sucesso
    alert(`✅ Você ingressou com sucesso na compra:\n\n"${item}"\n\nOrgão Responsável: ${unidade}`);
    
    // Aqui você pode adicionar lógica adicional, como:
    // - Enviar dados para o servidor
    // - Registrar em um banco de dados
    // - Atualizar interface do usuário
    
    fecharModal();
}

// Fecha modal ao clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('purchaseModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Carrega quantidade de conexões do grafo
async function carregarConexoes() {
    try {
        const response = await fetch('/api/grafo');
        const data = await response.json();
        const arestas = (data.edges || []).length;
        document.getElementById('conexoes-count').textContent = arestas;
    } catch (error) {
        console.error('Erro ao carregar conexões:', error);
        document.getElementById('conexoes-count').textContent = '0';
    }
}

// Carrega compras ao abrir página
window.addEventListener('DOMContentLoaded', () => {
    carregarComprasCompartilhadas();
    carregarConexoes();
});
