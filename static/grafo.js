// Carrega dados do grafo e renderiza com D3.js

let svg, g, simulation;
let zoomLevel = 1;
let nodes = [];
let links = [];
let nodesOriginais = [];
let linksOriginais = [];
let showDescription = false;
let labels;
let filtroDataInicio = null;
let filtroDataFim = null;
let filtroOrgao = null;

async function loadGraphData() {
    try {
        const response = await fetch('/api/grafo');
        const data = await response.json();
        
        nodesOriginais = data.nodes || [];
        linksOriginais = data.edges || [];
        
        // Cria cópias para trabalhar com filtros
        nodes = JSON.parse(JSON.stringify(nodesOriginais));
        links = JSON.parse(JSON.stringify(linksOriginais));
        
        inicializarFiltroData();
        inicializarFiltroOrgao();
        renderGraph();
    } catch (error) {
        console.error('Erro ao carregar grafo:', error);
        document.getElementById('grafo-container').innerHTML = 
            '<p style="text-align: center; padding: 40px;">Erro ao carregar o grafo. Certifique-se de que o arquivo existe.</p>';
    }
}

function inicializarFiltroOrgao() {
    // Extrai órgãos únicos dos nós
    const orgaosUnicos = [...new Set(nodesOriginais.map(n => n.orgao).filter(o => o))];
    orgaosUnicos.sort();
    
    // Popula o select com os órgãos
    const select = document.getElementById('selectOrgao');
    orgaosUnicos.forEach(orgao => {
        const option = document.createElement('option');
        option.value = orgao;
        option.textContent = orgao;
        select.appendChild(option);
    });
}

function inicializarFiltroData() {
    // Obtém data atual
    const hoje = new Date();
    const dataInicio = new Date(hoje);
    dataInicio.setDate(dataInicio.getDate()); // Hoje
    
    // Data 6 meses à frente
    const dataFim = new Date(hoje);
    dataFim.setMonth(dataFim.getMonth() + 6);
    
    // Formata para yyyy-MM-dd
    const formatarData = (date) => {
        const ano = date.getFullYear();
        const mes = String(date.getMonth() + 1).padStart(2, '0');
        const dia = String(date.getDate()).padStart(2, '0');
        return `${ano}-${mes}-${dia}`;
    };
    
    // Define valores nos inputs
    document.getElementById('dataInicio').value = formatarData(dataInicio);
    document.getElementById('dataFim').value = formatarData(dataFim);
    
    // Armazena os valores
    filtroDataInicio = dataInicio;
    filtroDataFim = dataFim;
}

function getVibrantColor(index) {
    // Cores vibrantes em paleta moderna
    const colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
        '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8B88B', '#82E0AA',
        '#F1948A', '#AED6F1', '#F5B041', '#A9DFBF', '#D7BDE2',
        '#FADBD8', '#D5F4E6', '#FDEBD0', '#EBDEF0', '#EBF5FB'
    ];
    return colors[index % colors.length];
}

function renderGraph() {
    const container = document.getElementById('grafo-container');
    const width = container.clientWidth;
    const height = container.clientHeight || 600;

    // Limpa container anterior
    container.innerHTML = '';

    // Cria SVG
    svg = d3.select('#grafo-container')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // Define zoom
    const zoom = d3.zoom()
        .on('zoom', (event) => {
            g.attr('transform', event.transform);
            zoomLevel = event.transform.k;
        });

    svg.call(zoom);

    // Grupo para conteúdo
    g = svg.append('g');

    // Defini simulação de força
    simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links)
            .id(d => d.id)
            .distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(30));

    // Desenha links (arestas)
    const link = g.selectAll('line')
        .data(links)
        .enter()
        .append('line')
        .attr('stroke', '#ddd')
        .attr('stroke-width', d => Math.sqrt(d.weight) * 2)
        .attr('opacity', 0.6);

    // Desenha nós
    const node = g.selectAll('circle')
        .data(nodes)
        .enter()
        .append('circle')
        .attr('r', 25)
        .attr('fill', (d, i) => getVibrantColor(i))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .call(drag(simulation))
        .on('mouseover', function(event, d) {
            d3.select(this)
                .attr('r', 35)
                .attr('stroke-width', 3);
            
            // Criar grupo para o tooltip
            const tooltipGroup = g.append('g')
                .attr('id', 'tooltip-group')
                .attr('transform', `translate(${d.x}, ${d.y - 60})`);
            
            // Caixa de fundo do tooltip
            const rectWidth = 250;
            const rectHeight = 80;
            
            tooltipGroup.append('rect')
                .attr('x', -rectWidth / 2)
                .attr('y', 0)
                .attr('width', rectWidth)
                .attr('height', rectHeight)
                .attr('fill', '#fff')
                .attr('stroke', '#1abc9c')
                .attr('stroke-width', 2)
                .attr('rx', 6)
                .attr('box-shadow', '0 4px 12px rgba(0,0,0,0.15)');
            
            // Triângulo apontador para o nó
            tooltipGroup.append('polygon')
                .attr('points', `0,${rectHeight} -8,${rectHeight + 8} 8,${rectHeight + 8}`)
                .attr('fill', '#fff')
                .attr('stroke', '#1abc9c')
                .attr('stroke-width', 2);
            
            // Texto - Órgão (titulo)
            tooltipGroup.append('text')
                .attr('x', 0)
                .attr('y', 15)
                .attr('text-anchor', 'middle')
                .attr('font-weight', 'bold')
                .attr('font-size', '12px')
                .attr('fill', '#1abc9c')
                .text(d.orgao || 'Sem órgão');
            
            // Linha separadora
            tooltipGroup.append('line')
                .attr('x1', -rectWidth / 2 + 10)
                .attr('x2', rectWidth / 2 - 10)
                .attr('y1', 25)
                .attr('y2', 25)
                .attr('stroke', '#e9ecef')
                .attr('stroke-width', 1);
            
            // Texto - Descrição
            const descricao = d.descricao || 'Sem descrição';
            const descricaoTruncada = descricao.length > 35 ? descricao.substring(0, 35) + '-' : descricao;
            
            tooltipGroup.append('text')
                .attr('x', -rectWidth / 2 + 10)
                .attr('y', 45)
                .attr('font-size', '11px')
                .attr('fill', '#555')
                .attr('style', 'word-wrap: break-word;')
                .text(descricaoTruncada);
            
            tooltipGroup.append('text')
                .attr('x', -rectWidth / 2 + 10)
                .attr('y', 60)
                .attr('font-size', '11px')
                .attr('fill', '#555')
                .text(descricao.length > 35 ? descricao.substring(35, 70) : '');
        })
        .on('mouseout', function() {
            d3.select(this)
                .attr('r', 25)
                .attr('stroke-width', 2);
            
            svg.select('#tooltip-group').remove();
        });

    // Rótulos
    labels = g.selectAll('text.node-label')
        .data(nodes)
        .enter()
        .append('text')
        .attr('class', 'node-label')
        .attr('font-size', '10px')
        .attr('text-anchor', 'middle')
        .attr('dy', '0.3em')
        .attr('fill', '#000')
        .attr('pointer-events', 'none')
        .text(d => d.orgao ? d.orgao.substring(0, 10) : '');

    // Atualiza posições durante simulação
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);

        labels
            .attr('x', d => d.x)
            .attr('y', d => d.y);
    });
}

function drag(simulation) {
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    return d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended);
}

// Controles de zoom
document.getElementById('zoomIn').addEventListener('click', () => {
    svg.transition().duration(300).call(
        d3.zoom().transform,
        d3.zoomIdentity
            .translate(svg.attr('width') / 2, svg.attr('height') / 2)
            .scale(zoomLevel * 1.5)
            .translate(-svg.attr('width') / 2, -svg.attr('height') / 2)
    );
});

document.getElementById('zoomOut').addEventListener('click', () => {
    svg.transition().duration(300).call(
        d3.zoom().transform,
        d3.zoomIdentity
            .translate(svg.attr('width') / 2, svg.attr('height') / 2)
            .scale(zoomLevel / 1.5)
            .translate(-svg.attr('width') / 2, -svg.attr('height') / 2)
    );
});

document.getElementById('resetZoom').addEventListener('click', () => {
    svg.transition().duration(300).call(
        d3.zoom().transform,
        d3.zoomIdentity
            .translate(svg.attr('width') / 2, svg.attr('height') / 2)
    );
    zoomLevel = 1;
});

// Toggle para mostrar nome ou descrição
document.getElementById('toggleLabels').addEventListener('click', function() {
    showDescription = !showDescription;
    labels.text(d => {
        if (showDescription) {
            return d.label ? d.label.substring(0, 20) : '';
        } else {
            return d.orgao ? d.orgao.substring(0, 10) : '';
        }
    });
    this.textContent = showDescription ? '🏷️ Mostrar Órgão' : '🏷️ Mostrar Descrição';
});

// Fullscreen para o grafo
document.getElementById('fullscreenBtn').addEventListener('click', function() {
    const container = document.getElementById('grafo-container');
    
    if (!document.fullscreenElement) {
        // Entrar em tela cheia
        if (container.requestFullscreen) {
            container.requestFullscreen();
        } else if (container.webkitRequestFullscreen) {
            container.webkitRequestFullscreen();
        } else if (container.msRequestFullscreen) {
            container.msRequestFullscreen();
        }
        this.textContent = '👁️ Sair Tela Cheia';
    } else {
        // Sair de tela cheia
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
        this.textContent = '👁️ Tela Cheia';
    }
});

// Listener para quando sair de tela cheia (tecla ESC)
document.addEventListener('fullscreenchange', function() {
    const btn = document.getElementById('fullscreenBtn');
    if (!document.fullscreenElement) {
        btn.textContent = '👁️ Tela Cheia';
    }
});

// Filtro de data
document.getElementById('dataInicio').addEventListener('change', () => {
    const dataInicio = document.getElementById('dataInicio').value;
    filtroDataInicio = dataInicio ? new Date(dataInicio) : null;
});

document.getElementById('dataFim').addEventListener('change', () => {
    const dataFim = document.getElementById('dataFim').value;
    filtroDataFim = dataFim ? new Date(dataFim) : null;
});

document.getElementById('resetData').addEventListener('click', () => {
    inicializarFiltroData();
});

// Filtro de órgão
document.getElementById('selectOrgao').addEventListener('change', function() {
    filtroOrgao = this.value || null;
    aplicarFiltros();
    renderGraph();
});

function aplicarFiltros() {
    // Começa com todos os nós e links originais
    let nodesFiltered = JSON.parse(JSON.stringify(nodesOriginais));
    let linksFiltered = JSON.parse(JSON.stringify(linksOriginais));
    
    // Aplica filtro de órgão
    if (filtroOrgao) {
        const nodesDoOrgao = nodesFiltered.filter(n => n.orgao === filtroOrgao);
        const idsDoOrgao = new Set(nodesDoOrgao.map(n => n.id));
        
        // Nós: o próprio órgão + nós conectados a ele
        const nodesConectados = new Set(idsDoOrgao);
        linksFiltered.forEach(link => {
            if (idsDoOrgao.has(link.source.id) || idsDoOrgao.has(link.source)) {
                nodesConectados.add(link.target.id || link.target);
            }
            if (idsDoOrgao.has(link.target.id) || idsDoOrgao.has(link.target)) {
                nodesConectados.add(link.source.id || link.source);
            }
        });
        
        nodesFiltered = nodesFiltered.filter(n => nodesConectados.has(n.id));
        
        // Links: apenas aqueles que conectam nós do filtro
        linksFiltered = linksFiltered.filter(link => {
            const sourceId = link.source.id || link.source;
            const targetId = link.target.id || link.target;
            return nodesConectados.has(sourceId) && nodesConectados.has(targetId);
        });
    }
    
    nodes = nodesFiltered;
    links = linksFiltered;
}

// Carrega grafo ao abrir página
window.addEventListener('DOMContentLoaded', loadGraphData);
