import os
import pandas as pd
from google import genai

SYSTEM_PROMPT = """Você é um engenheiro de Cloud FinOps especialista em Azure.
O recurso Azure abaixo está gerando desperdício.
Baseado no problema descrito, escreva APENAS o comando de terminal do Azure CLI (az cli) necessário para consertar isso (ex: az vm resize, az disk delete, az resource tag).
Adicione uma breve explicação técnica de 1 linha embaixo do código.
Responda em português (pt-BR).
Dados do recurso:
{dados}"""

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada no ambiente (.env).")
    return genai.Client(api_key=api_key)

def gerar_script_remediacao(row: pd.Series) -> str:
    """Aciona a API do Gemini para gerar o script az cli."""
    dados_formatados = (
        f"Recurso: {row['Recurso']}\n"
        f"Tipo: {row['Tipo']}\n"
        f"CPU Média: {row['CPU Média (%)']}\n"
        f"Custo Mensal: R$ {row['Custo Mensal (R$)']}\n"
        f"Problema: {row['Problema']}"
    )
    prompt = SYSTEM_PROMPT.format(dados=dados_formatados)
    
    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"# ⚠️ Erro ao contatar a API Gemini\n# {str(e)}"

AI_FINOPS_SYSTEM_PROMPT = """Você é um Engenheiro de AI FinOps sênior.
Analise esta tabela de consumo de tokens e custos dos nossos modelos LLM.
Identifique ineficiências (como uso de modelos caros para tarefas simples) e gere exatamente 3 insights de otimização acionáveis.
Exemplos de insight: melhoria de prompt, roteamento de modelo, cache de contexto, compressão de histórico.
Retorne a resposta em Markdown limpo e executivo — use títulos ## para cada insight, negrito para valores de impacto e listas para ações concretas.
Responda em português (pt-BR).

Dados da tabela de consumo:
{dados}"""

def gerar_insights_ai_finops(dados_tabela) -> str:
    """Aciona a API do Gemini para gerar insights de otimização de IA FinOps."""
    dados_formatados = dados_tabela.to_string(index=False)
    prompt = AI_FINOPS_SYSTEM_PROMPT.format(dados=dados_formatados)

    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"**⚠️ Erro ao contatar a API Gemini:** {str(e)}"
