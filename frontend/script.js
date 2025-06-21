document.addEventListener('DOMContentLoaded', () => {
    const mindmapContainer = document.getElementById('mindmap');
    const detailsContainer = document.getElementById('details');
    let network = null;
    let allTerms = [];

    const drawMindMap = (terms) => {
        const nodes = new vis.DataSet(terms.map(term => ({
            id: term.id,
            label: term.term
        })));

        const edges = new vis.DataSet();
        terms.forEach(term => {
            if (term.related_term_ids) {
                term.related_term_ids.forEach(relatedId => {
                    edges.add({ from: term.id, to: relatedId, arrows: 'to' });
                });
            }
        });

        const data = { nodes, edges };
        const options = {
            nodes: {
                shape: 'box',
                font: {
                    size: 16,
                    color: '#ffffff'
                },
                color: {
                    border: '#2B7CE9',
                    background: '#97C2FC',
                    highlight: {
                        border: '#2B7CE9',
                        background: '#D2E5FF'
                    }
                }
            },
            edges: {
                width: 2
            },
            physics: {
                barnesHut: {
                    gravitationalConstant: -3000
                }
            }
        };

        network = new vis.Network(mindmapContainer, data, options);
        network.on("click", handleNodeClick);
    };

    const handleNodeClick = (params) => {
        const { nodes } = params;
        if (nodes.length > 0) {
            const nodeId = nodes[0];
            const term = allTerms.find(t => t.id === nodeId);
            if (term) {
                displayTermDetails(term);
            }
        }
    };

    const displayTermDetails = (term) => {
        let linksHtml = term.source_links.map(link => 
            `<a href="${link}" target="_blank">${link}</a>`
        ).join('<br>');

        detailsContainer.innerHTML = `
            <h2>${term.term}</h2>
            <p><strong>Definition:</strong> ${term.definition}</p>
            <p><strong>Sources:</strong><br>${linksHtml}</p>
        `;
    };

    fetch('/api/terms')
        .then(response => response.json())
        .then(data => {
            allTerms = data;
            drawMindMap(allTerms);
        })
        .catch(error => {
            console.error('Error fetching terms:', error);
            mindmapContainer.innerHTML = 'Failed to load glossary data.';
        });
});
