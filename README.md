# Active FinOps Copilot — Deploy

Este repositório contém uma app Streamlit (`app.py`) pronta para deploy.

Passo a passo mínimo para subir (assumindo que o repo já está no GitHub):

1) Garanta que os novos arquivos estão commitados e enviados:

```bash
git add Dockerfile Procfile .dockerignore README.md
git commit -m "Add deploy files: Dockerfile, Procfile, dockerignore, README"
git push origin main
```

2) Variáveis de ambiente (necessárias em produção):
- `GEMINI_API_KEY` — token da API Gemini. Não comite `.env`.

Para testes locais você pode criar um `.env` a partir do exemplo:

```bash
cp .env.example .env
# then open .env and replace the placeholder with your real key
```

Onde configurar a variável no host:
- Streamlit Community Cloud: App Settings → Secrets → adicione `GEMINI_API_KEY`.
- Render: Dashboard do serviço → Environment → Add Environment Variable.
- Azure App Service: Configuration → Application settings.

3) Deploy rápido (recomendado para demo): Streamlit Community Cloud
- Vá para https://streamlit.io/cloud e crie um novo app ligado ao seu repositório GitHub.
- Selecione branch `main` e o path do repositório (root).
- Defina o secret `GEMINI_API_KEY` no painel de Secrets.

4) Deploy via Render (alternativa simples):
- New → Web Service → Connect GitHub repo → Branch `main`.
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Add `GEMINI_API_KEY` em Environment.

5) Deploy com Docker (VPS, Azure Container Instances, etc.):

Build & run localmente para testar:
```bash
docker build -t finops-copilot:latest .
docker run -p 8501:8501 --env GEMINI_API_KEY="$GEMINI_API_KEY" finops-copilot:latest
```

Enviar imagem para Docker Hub (exemplo):
```bash
docker tag finops-copilot:latest <your-dockerhub-username>/finops-copilot:latest
docker push <your-dockerhub-username>/finops-copilot:latest
```

6) Observações finais
- Nunca exponha `GEMINI_API_KEY` no repositório.
- Para ambientes corporativos, prefira Azure App Service + Managed Identity ou Container Registry.
