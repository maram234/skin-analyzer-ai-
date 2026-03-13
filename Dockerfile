# Skin Mirror AI — Backend for Hugging Face Spaces (port 7860)
FROM python:3.11-slim

WORKDIR /app

# Copy backend code and dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Hugging Face Spaces default port
EXPOSE 7860

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "7860"]
