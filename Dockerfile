FROM python:3.11-slim
WORKDIR /app

# Install minimal build deps (if any wheels need building)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501
ENV PORT=8501

CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]
