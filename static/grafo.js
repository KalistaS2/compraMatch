// Carrega dados do grafo e renderiza com D3.js

let svg, g, simulation;
let zoomLevel = 1;
let nodes = [];
let links = [];
let showDescription = false;
let labels;

async function loadGraphData() {
    try {
        const response = await fetch('/api/grafo');
        const data = await response.json();
        
        nodes = data.nodes || [];
        links = data.edges || [];
        
        renderGraph();
    } catch (error) {
        console.error('Erro ao carregar grafo:', error);
        document.getElementById('grafo-container').innerHTML = 
            '<p style="text-align: center; padding: 40px;">Erro ao carregar o grafo. Certifique-se de que o arquivo existe.</p>';
    }
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
            
            // Mostra tooltip
            const tooltip = svg.append('text')
                .attr('id', 'tooltip')
                .attr('x', event.pageX - container.getBoundingClientRect().left)
                .attr('y', event.pageY - container.getBoundingClientRect().top - 10)
                .attr('text-anchor', 'middle')
                .attr('font-size', '12px')
                .attr('fill', '#000')
                .attr('background', '#fff')
                .text(d.orgao);
        })
        .on('mouseout', function() {
            d3.select(this)
                .attr('r', 25)
                .attr('stroke-width', 2);
            
            svg.select('#tooltip').remove();
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

// Carrega grafo ao abrir página
window.addEventListener('DOMContentLoaded', loadGraphData);
