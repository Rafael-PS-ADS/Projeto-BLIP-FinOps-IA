import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

print(f"DEBUG: API KEY carregada: {os.getenv('GEMINI_API_KEY')[:10]}...")

from core.ai_engine import gerar_script_remediacao
from data.mocks import get_mock_resources

app = FastAPI(title="Active FinOps API")

class RemediateRequest(BaseModel):
    id: str

@app.get("/api/resources")
def get_resources():
    resources = get_mock_resources()
    total_desperdicio = sum(r["custo_mensal"] for r in resources)
    n_vms = sum(1 for r in resources if r["tipo"] == "VM")
    economia_potencial = int(total_desperdicio * 0.65)
    
    return {
        "resources": resources,
        "metrics": {
            "total_desperdicio": total_desperdicio,
            "economia_potencial": economia_potencial,
            "n_vms": n_vms,
            "n_recursos": len(resources)
        }
    }

@app.post("/api/remediate")
def remediate_resource(req: RemediateRequest):
    resources = get_mock_resources()
    # Busca o recurso pelo ID
    recurso = next((r for r in resources if r["id"] == req.id), None)
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    
    # Gera script via Gemini
    script = gerar_script_remediacao(recurso)
    return {"script": script}

# Serve o frontend de forma estática
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

@app.get("/")
def read_index():
    return FileResponse("frontend/index.html")
