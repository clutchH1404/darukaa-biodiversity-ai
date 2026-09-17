FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ingest initial scientific knowledge into ChromaDB and seed database
RUN python scripts/ingest_documents.py && python scripts/seed_database.py

EXPOSE 8000 8501

ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV FRONTEND_PORT=8501

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
