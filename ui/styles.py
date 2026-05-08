import streamlit as st

def apply_custom_css():
    st.markdown(
        """
        <style>
        /* ── Importar fonte ── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Reset global ── */
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        /* ── Background principal ── */
        .stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2e 50%, #0a0f1e 100%); color: #e2e8f0; }

        /* ── Header hero ── */
        .hero-section {
            background: linear-gradient(135deg, #1e3a5f 0%, #0f2744 40%, #1a1f3a 100%);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 20px;
            padding: 2.5rem 3rem;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 60px rgba(56, 189, 248, 0.08), 0 20px 60px rgba(0,0,0,0.4);
        }
        .hero-badge {
            display: inline-block;
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #38bdf8;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            padding: 0.3rem 0.9rem;
            border-radius: 50px;
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff 0%, #38bdf8 60%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.2rem 0 0.6rem 0;
            line-height: 1.15;
        }
        .hero-subtitle { font-size: 1rem; color: #94a3b8; margin: 0; }

        /* ── Metric cards ── */
        .metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; margin-bottom: 2.2rem; }
        .metric-card {
            background: linear-gradient(145deg, rgba(30,58,95,0.6) 0%, rgba(15,39,68,0.8) 100%);
            border: 1px solid rgba(56,189,248,0.18);
            border-radius: 16px;
            padding: 1.6rem 1.8rem;
            backdrop-filter: blur(10px);
            transition: transform 0.25s ease;
        }
        .metric-card:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(56,189,248,0.12); }
        .metric-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #64748b; font-weight: 600; margin-bottom: 0.5rem; }
        .metric-value { font-size: 2rem; font-weight: 800; color: #f8fafc; line-height: 1; }
        .metric-value.danger { color: #f87171; }
        .metric-value.warning { color: #fb923c; }
        .metric-value.info { color: #38bdf8; }
        .metric-delta { font-size: 0.8rem; color: #94a3b8; margin-top: 0.4rem; }

        /* ── Resources ── */
        .section-title { font-size: 1.15rem; font-weight: 700; color: #e2e8f0; margin: 2rem 0 1rem 0; }
        .section-divider { height: 1px; background: linear-gradient(90deg, rgba(56,189,248,0.3) 0%, transparent 80%); margin-bottom: 1.5rem; }
        
        .resource-name { font-size: 1.05rem; font-weight: 700; color: #e2e8f0; font-family: 'Courier New', monospace; }
        .resource-type-badge { display: inline-block; padding: 0.2rem 0.65rem; border-radius: 6px; font-size: 0.72rem; font-weight: 600; margin-left: 0.5rem; }
        .badge-vm { background: rgba(129,140,248,0.18); color: #818cf8; border: 1px solid rgba(129,140,248,0.3); }
        .badge-disk { background: rgba(251,146,60,0.15); color: #fb923c; border: 1px solid rgba(251,146,60,0.3); }
        .badge-snapshot { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
        
        .problem-tag { display: inline-block; background: rgba(248,113,113,0.12); border: 1px solid rgba(248,113,113,0.28); color: #fca5a5; border-radius: 8px; padding: 0.2rem 0.7rem; font-size: 0.78rem; font-weight: 500; margin-top: 0.4rem; }
        .resource-cost { font-size: 1.4rem; font-weight: 800; color: #f87171; }

        /* ── Botões e Code ── */
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important; color: white !important; border: none !important;
            border-radius: 10px !important; font-weight: 600 !important; font-size: 0.85rem !important; padding: 0.55rem 1.2rem !important;
            width: 100% !important;
        }
        .stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
        .stCode { border-radius: 12px !important; border: 1px solid rgba(56,189,248,0.2) !important; }
        
        .footer { text-align: center; color: #334155; font-size: 0.78rem; margin-top: 3rem; padding: 1.5rem 0; border-top: 1px solid rgba(56,189,248,0.08); }
        </style>
        """,
        unsafe_allow_html=True,
    )
