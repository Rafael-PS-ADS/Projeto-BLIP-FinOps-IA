import streamlit as st
from dotenv import load_dotenv

# Carrega a variável de ambiente (GEMINI_API_KEY) do arquivo .env
load_dotenv()

from data.mocks import get_mock_dataframe, get_ai_agents_dataframe
from core.ai_engine import gerar_script_remediacao, gerar_insights_ai_finops
from ui.styles import apply_custom_css
from ui.components import render_hero, render_metrics, render_ai_response, render_footer

# ─────────────────────────────────────────────
#  PAGE CONFIG & SETUP
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Active FinOps Copilot – Azure",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_css()

# ─────────────────────────────────────────────
#  CABEÇALHO GLOBAL
# ─────────────────────────────────────────────
render_hero()

# ─────────────────────────────────────────────
#  ABAS PRINCIPAIS
# ─────────────────────────────────────────────
tab_infra, tab_ai = st.tabs(["☁️ Cloud Infra (Azure)", "🧠 AI Agents FinOps"])

# ══════════════════════════════════════════════
#  ABA 1 – CLOUD INFRA (código original intacto)
# ══════════════════════════════════════════════
with tab_infra:
    df = get_mock_dataframe()
    total_desperdicio = df["Custo Mensal (R$)"].sum()
    n_recursos = len(df)
    n_vms = len(df[df["Tipo"] == "VM"])

    render_metrics(total_desperdicio, n_recursos, n_vms)

    # ── Tabela de ação ──
    st.markdown(
        '<div class="section-title">🔍 Recursos com Desperdício Detectado</div><div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    BADGE_MAP = {"VM": "badge-vm", "Managed Disk": "badge-disk", "Snapshot": "badge-snapshot"}

    if "scripts" not in st.session_state:
        st.session_state.scripts = {}

    for idx, row in df.iterrows():
        tipo = row["Tipo"]
        badge_class = BADGE_MAP.get(tipo, "badge-vm")

        col_info, col_cpu, col_cost, col_btn = st.columns([3.5, 1.2, 1.5, 2])

        with col_info:
            st.markdown(
                f"""
                <div style="padding: 0.5rem 0;">
                    <span class="resource-name">{row['Recurso']}</span>
                    <span class="resource-type-badge {badge_class}">{tipo}</span>
                    <br/>
                    <span class="problem-tag">⚠ {row['Problema']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_cpu:
            st.markdown(
                f"""
                <div style="padding:0.5rem 0; font-size:0.82rem; color:#64748b; font-weight:500;">
                    <span style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;">CPU Média</span><br/>
                    <span style="font-size:1.1rem; color:#94a3b8; font-weight:700;">{row['CPU Média (%)']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_cost:
            st.markdown(
                f"""
                <div style="padding:0.5rem 0;">
                    <span style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#64748b;">Custo/mês</span><br/>
                    <span class="resource-cost">R$ {row['Custo Mensal (R$)']:,}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_btn:
            st.write("")  # alinhamento vertical
            if st.button(f"⚙️ Gerar Script (Copilot)", key=f"btn_{idx}"):
                with st.spinner(f"🤖 Analisando `{row['Recurso']}`..."):
                    script = gerar_script_remediacao(row)
                    st.session_state.scripts[idx] = script

        if idx in st.session_state.scripts:
            render_ai_response(st.session_state.scripts[idx])

        st.markdown('<hr style="border:none;border-top:1px solid rgba(56,189,248,0.07);margin:0.3rem 0 0.8rem 0;">', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  ABA 2 – AI AGENTS FINOPS (novo módulo)
# ══════════════════════════════════════════════
with tab_ai:
    # ── Cabeçalho da seção ──
    st.markdown(
        """
        <div class="section-title">🧠 Monitoramento de Consumo – Agentes de IA</div>
        <div class="section-divider"></div>
        """,
        unsafe_allow_html=True,
    )

    df_ai = get_ai_agents_dataframe()

    # ── Métricas de resumo ──
    custo_total_ai = df_ai["Custo Total (R$)"].sum()
    input_total    = df_ai["Input Tokens (M)"].sum()
    output_total   = df_ai["Output Tokens (M)"].sum()
    razao_io       = input_total / output_total if output_total else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">💰 Custo Total com LLMs</div>
                <div class="metric-value danger">R$ {custo_total_ai:,.0f}</div>
                <div class="metric-delta">/ mês · {len(df_ai)} squads monitorados</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">📥 Input Tokens Totais</div>
                <div class="metric-value warning">{input_total:.1f} M</div>
                <div class="metric-delta">tokens de entrada processados</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">⚖️ Razão Input / Output</div>
                <div class="metric-value info">{razao_io:.1f}x</div>
                <div class="metric-delta">ideal: abaixo de 5x para prompts eficientes</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Tabela estilizada ──
    EFIC_COLORS = {
        "Alta":  ("#34d399", "rgba(52,211,153,0.12)", "rgba(52,211,153,0.3)"),
        "Média": ("#fb923c", "rgba(251,146,60,0.12)",  "rgba(251,146,60,0.3)"),
        "Baixa": ("#f87171", "rgba(248,113,113,0.12)", "rgba(248,113,113,0.3)"),
    }

    def efic_badge(texto: str) -> str:
        nivel = texto.split(" –")[0].strip()
        cor, bg, borda = EFIC_COLORS.get(nivel, ("#94a3b8", "rgba(148,163,184,0.1)", "rgba(148,163,184,0.3)"))
        return (
            f'<span style="background:{bg};border:1px solid {borda};color:{cor};'
            f'border-radius:8px;padding:0.18rem 0.65rem;font-size:0.76rem;font-weight:600;">'
            f'{texto}</span>'
        )

    header_cols = st.columns([2, 2, 1.5, 1.5, 1.8, 3.5])
    headers = ["Modelo de IA", "Área/Squad", "Input (M)", "Output (M)", "Custo (R$)", "Eficiência"]
    for col, h in zip(header_cols, headers):
        col.markdown(
            f'<div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.09em;'
            f'color:#64748b;font-weight:700;padding-bottom:0.4rem;border-bottom:1px solid rgba(56,189,248,0.12);">{h}</div>',
            unsafe_allow_html=True,
        )

    for _, row in df_ai.iterrows():
        row_cols = st.columns([2, 2, 1.5, 1.5, 1.8, 3.5])
        row_cols[0].markdown(
            f'<span style="font-weight:700;color:#e2e8f0;font-size:0.88rem;">{row["Modelo de IA"]}</span>',
            unsafe_allow_html=True,
        )
        row_cols[1].markdown(
            f'<span style="color:#94a3b8;font-size:0.88rem;">{row["Área/Squad"]}</span>',
            unsafe_allow_html=True,
        )
        row_cols[2].markdown(
            f'<span style="color:#38bdf8;font-weight:600;">{row["Input Tokens (M)"]}</span>',
            unsafe_allow_html=True,
        )
        row_cols[3].markdown(
            f'<span style="color:#818cf8;font-weight:600;">{row["Output Tokens (M)"]}</span>',
            unsafe_allow_html=True,
        )
        row_cols[4].markdown(
            f'<span style="color:#f87171;font-weight:700;">R$ {row["Custo Total (R$)"]:,}</span>',
            unsafe_allow_html=True,
        )
        row_cols[5].markdown(efic_badge(row["Eficiência"]), unsafe_allow_html=True)
        st.markdown(
            '<hr style="border:none;border-top:1px solid rgba(56,189,248,0.06);margin:0.35rem 0;">',
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Botão de Insights ──
    if "ai_insights" not in st.session_state:
        st.session_state.ai_insights = None

    if st.button("🪄 Gerar Insights de Otimização de IA", key="btn_ai_insights"):
        with st.spinner("🧠 Analisando padrões de consumo com Gemini..."):
            st.session_state.ai_insights = gerar_insights_ai_finops(df_ai)

    # ── Exibição dos insights ──
    if st.session_state.ai_insights:
        st.markdown(
            """
            <div style="background:rgba(129,140,248,0.06); border-left:3px solid #818cf8;
                 border-radius:0 12px 12px 0; padding:1.4rem 1.8rem; margin-top:1rem;">
                <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;
                     color:#818cf8;font-weight:700;margin-bottom:1rem;">
                    🤖 Insights Gerados pelo AI FinOps Copilot (Gemini 2.5 Flash)
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state.ai_insights)
        st.markdown("</div>", unsafe_allow_html=True)

render_footer()
