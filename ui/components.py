import streamlit as st
import re

def render_hero():
    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-badge">⚡ AI-Powered · Azure FinOps</div>
            <div class="hero-title">Copilot CLI – Active FinOps</div>
            <p class="hero-subtitle">
                Identificação e Remediação Automática de Desperdícios no Azure
                &nbsp;·&nbsp; Powered by Gemini 1.5 Flash
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_metrics(total_desperdicio: float, n_recursos: int, n_vms: int):
    economia_potencial = int(total_desperdicio * 0.65)
    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">💸 Desperdício Total Identificado</div>
                <div class="metric-value danger">R$ {total_desperdicio:,.0f}</div>
                <div class="metric-delta">/ mês · {n_recursos} recursos analisados</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">🎯 Economia Potencial Estimada</div>
                <div class="metric-value warning">R$ {economia_potencial:,.0f}</div>
                <div class="metric-delta">após remediações sugeridas</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">🖥️ VMs com Baixo Consumo</div>
                <div class="metric-value info">{n_vms}</div>
                <div class="metric-delta">candidatas a resize ou desligamento</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_ai_response(script_text: str):
    """Extrai o bloco de código markdown e exibe lindamente."""
    code_match = re.search(r"```(?:bash|azurecli|shell|cli|az)?\s*([\s\S]*?)```", script_text)
    
    if code_match:
        code_part = code_match.group(1).strip()
        explanation = re.sub(r"```(?:bash|azurecli|shell|cli|az)?[\s\S]*?```", "", script_text).strip()
    else:
        lines = script_text.strip().split("\n")
        code_lines = []
        exp_lines = []
        in_code = True
        for line in lines:
            if in_code and (line.startswith("az ") or line.startswith("#") or line.strip() == ""):
                code_lines.append(line)
            else:
                in_code = False
                exp_lines.append(line)
        code_part = "\n".join(code_lines).strip()
        explanation = "\n".join(exp_lines).strip()

    with st.container():
        st.markdown(
            """
            <div style="background:rgba(14,165,233,0.06); border-left:3px solid #0ea5e9;
                 border-radius:0 12px 12px 0; padding:1.2rem 1.5rem; margin: 0.5rem 0 1.5rem 0;">
                <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;
                     color:#38bdf8;font-weight:700;margin-bottom:0.8rem;">
                    🤖 Script Gerado pelo Copilot (Gemini 1.5 Flash)
                </div>
            """,
            unsafe_allow_html=True,
        )
        if code_part:
            st.code(code_part, language="bash")
        if explanation:
            st.markdown(
                f"""<p style="font-size:0.85rem;color:#94a3b8;margin-top:0.6rem;margin-bottom:0;">
                    💡 <em>{explanation}</em></p>""",
                unsafe_allow_html=True,
            )
        elif not code_part:
            st.code(script_text, language="bash")
        st.markdown("</div>", unsafe_allow_html=True)

def render_footer():
    st.markdown(
        """
        <div class="footer">
            Active FinOps Copilot – Azure &nbsp;·&nbsp; Powered by Google Gemini 1.5 Flash &nbsp;·&nbsp;
            Arquitetura Modular Refatorada · 2025
        </div>
        """,
        unsafe_allow_html=True,
    )
