import pandas as pd

mock_data = {
    "Recurso": [
        "vm-blip-prd-01",
        "disk-orphan-bkp",
        "vm-teste-dev-04",
        "vm-data-worker",
        "snap-old-2025",
    ],
    "Tipo": ["VM", "Managed Disk", "VM", "VM", "Snapshot"],
    "CPU Média (%)": ["8%", "N/A", "2%", "15%", "N/A"],
    "Custo Mensal (R$)": [1200, 350, 400, 800, 150],
    "Problema": [
        "Oversized (Muito grande para o uso)",
        "Unattached (Disco solto cobrando)",
        "Missing Tags (Sem tag de centro de custo)",
        "Oversized",
        "Obsoleto (> 90 dias)",
    ],
}

def get_mock_dataframe() -> pd.DataFrame:
    """Retorna o DataFrame de dados mockados simulando recursos do Azure."""
    return pd.DataFrame(mock_data)

def get_mock_resources() -> list:
    """Retorna uma lista de dicionários para consumo via API FastAPI."""
    return [
        {
            "id": f"res-{i}",
            "recurso": mock_data["Recurso"][i],
            "tipo": mock_data["Tipo"][i],
            "cpu_media": mock_data["CPU Média (%)"][i],
            "custo_mensal": mock_data["Custo Mensal (R$)"][i],
            "problema": mock_data["Problema"][i],
            # Chaves extras para o motor de IA que espera o formato original do DataFrame
            "Recurso": mock_data["Recurso"][i],
            "Tipo": mock_data["Tipo"][i],
            "CPU Média (%)": mock_data["CPU Média (%)"][i],
            "Custo Mensal (R$)": mock_data["Custo Mensal (R$)"][i],
            "Problema": mock_data["Problema"][i]
        }
        for i in range(len(mock_data["Recurso"]))
    ]

ai_agents_data = {
    "Modelo de IA": [
        "GPT-4o",
        "GPT-4o",
        "GPT-4o mini",
        "Gemini 1.5 Pro",
        "GPT-4o mini",
        "Gemini 1.5 Flash",
    ],
    "Área/Squad": [
        "Atendimento",
        "Dev – Code Review",
        "Suporte N1",
        "Análise de Dados",
        "Marketing",
        "Automação Interna",
    ],
    "Input Tokens (M)": [18.4, 12.1, 35.6, 9.2, 41.0, 6.7],
    "Output Tokens (M)": [1.2, 0.9, 3.1, 4.8, 2.9, 0.4],
    "Custo Total (R$)": [9_200, 6_050, 2_100, 5_800, 2_460, 310],
    "Eficiência": [
        "Baixa – Alto uso de prompt para saída curta",
        "Baixa – Modelo caro para tarefa de revisão simples",
        "Média – Boa relação custo/output",
        "Alta – Modelo adequado para análise de longa duração",
        "Baixa – Volume de input excessivo, cache não utilizado",
        "Alta – Modelo leve e eficiente para automações",
    ],
}

def get_ai_agents_dataframe() -> pd.DataFrame:
    """Retorna DataFrame simulado com consumo de tokens e custos dos agentes de IA."""
    return pd.DataFrame(ai_agents_data)
