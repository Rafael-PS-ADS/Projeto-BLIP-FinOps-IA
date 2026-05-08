import os
from google import genai
from pydantic import BaseModel

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

def gerar_script_remediacao(recurso_data: dict) -> str:
    """Aciona a API do Gemini para gerar o script az cli."""
    dados_formatados = (
        f"Recurso: {recurso_data.get('recurso')}\n"
        f"Tipo: {recurso_data.get('tipo')}\n"
        f"CPU Média: {recurso_data.get('cpu_media')}\n"
        f"Custo Mensal: R$ {recurso_data.get('custo_mensal')}\n"
        f"Problema: {recurso_data.get('problema')}"
    )
    prompt = SYSTEM_PROMPT.format(dados=dados_formatados)
    
    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR GEMINI: {error_msg}")  # Log para debug no servidor
        
        if "429" in error_msg or "quota" in error_msg.lower() or "RESOURCE_EXHAUSTED" in error_msg:
            fallback = f"# ⚠️ Limite de cota da API atingido (Fallback Ativado)\n"
            tipo = recurso_data.get("tipo", "")
            recurso = recurso_data.get("recurso", "recurso-desconhecido")
            
            if "VM" in tipo:
                fallback += f"az vm resize --resource-group rg-finops --name {recurso} --size Standard_B2s\n"
                fallback += f"# Sugestão: Reduzir o tamanho da VM para adequar ao baixo uso (CPU: {recurso_data.get('cpu_media')})."
            elif "Disk" in tipo:
                fallback += f"az disk delete --resource-group rg-finops --name {recurso} --yes\n"
                fallback += f"# Sugestão: Deletar disco órfão para evitar cobranças inativas."
            elif "SQL" in tipo or "Database" in tipo:
                fallback += f"az sql db update --resource-group rg-finops --server server-name --name {recurso} --tier GeneralPurpose --family Gen5 --capacity 2\n"
                fallback += f"# Sugestão: Escalonar o banco de dados para um tier menor de acordo com o consumo."
            else:
                fallback += f"az resource tag --tags RevisaoFinOps=Pendente --name {recurso}\n"
                fallback += f"# Sugestão: Recurso marcado para revisão manual pela equipe."
            
            return fallback

        # Limitar o tamanho da string de erro para não quebrar a UI
        return f"# ⚠️ Erro ao contatar a API Gemini\n# Detalhe técnico: {error_msg[:150]}..."
