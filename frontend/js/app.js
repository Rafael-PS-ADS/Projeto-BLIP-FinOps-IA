document.addEventListener('DOMContentLoaded', () => {
    loadResources();
});

async function loadResources() {
    try {
        const response = await fetch('/api/resources');
        const data = await response.json();
        
        updateMetrics(data.metrics);
        renderResources(data.resources);
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        document.getElementById('resources-container').innerHTML = '<p class="problem-tag">Erro ao carregar recursos do backend.</p>';
    }
}

function updateMetrics(metrics) {
    document.getElementById('metric-total').innerText = `R$ ${metrics.total_desperdicio.toLocaleString('pt-BR')}`;
    document.getElementById('metric-savings').innerText = `R$ ${metrics.economia_potencial.toLocaleString('pt-BR')}`;
    document.getElementById('metric-vms').innerText = metrics.n_vms;
    document.getElementById('metric-count').innerText = metrics.n_recursos;
}

function renderResources(resources) {
    const container = document.getElementById('resources-container');
    container.innerHTML = '';

    resources.forEach(res => {
        const badgeClass = res.tipo.includes('Disk') ? 'badge-Managed' : (res.tipo === 'Snapshot' ? 'badge-Snapshot' : 'badge-VM');
        
        const card = document.createElement('div');
        card.className = 'resource-card';
        card.innerHTML = `
            <div class="res-info">
                <span class="res-name">${res.recurso}</span>
                <span class="res-badge ${badgeClass}">${res.tipo}</span>
                <br/>
                <span class="problem-tag">⚠ ${res.problema}</span>
            </div>
            <div class="res-stat">
                <div class="stat-label">CPU Média</div>
                <div class="stat-val">${res.cpu_media}</div>
            </div>
            <div class="res-stat">
                <div class="stat-label">Custo/Mês</div>
                <div class="stat-cost">R$ ${res.custo_mensal.toLocaleString('pt-BR')}</div>
            </div>
            <div class="res-action">
                <button class="btn-remediate" onclick="remediate('${res.id}', this)">⚙️ Gerar Script</button>
            </div>
            <div class="ai-response" id="ai-res-${res.id}"></div>
        `;
        container.appendChild(card);
    });
}

async function remediate(id, btnElement) {
    const originalText = btnElement.innerHTML;
    btnElement.innerHTML = '<span class="spinner"></span> Analisando...';
    btnElement.disabled = true;

    const aiContainer = document.getElementById(`ai-res-${id}`);
    
    try {
        const response = await fetch('/api/remediate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: id })
        });
        
        const data = await response.json();
        
        // Parse da resposta do Gemini
        let code = data.script;
        let explanation = "";
        
        const codeMatch = data.script.match(/```(?:bash|azurecli|shell|cli|az)?\s*([\s\S]*?)```/);
        if (codeMatch) {
            code = codeMatch[1].trim();
            explanation = data.script.replace(/```[\s\S]*?```/g, '').trim();
        }

        aiContainer.innerHTML = `
            <div class="ai-header">🤖 Script Gerado pelo Copilot (Gemini)</div>
            <div class="ai-code-wrapper">
                <div class="ai-code">${code.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
            </div>
            ${explanation ? `<div class="ai-explanation">💡 ${explanation}</div>` : ''}
        `;
        aiContainer.style.display = 'block';

    } catch (error) {
        console.error('Erro na remediação:', error);
        aiContainer.innerHTML = `<span class="problem-tag">Erro ao gerar script com a IA.</span>`;
        aiContainer.style.display = 'block';
    } finally {
        btnElement.innerHTML = '✅ Script Gerado';
        // Não reabilito o botão para evitar re-geração desnecessária
    }
}
