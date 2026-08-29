FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home --uid 10001 appuser && mkdir -p /app/uploads && chown -R appuser:appuser /app
USER appuser
EXPOSE 8001
CMD ["python","-c","from studycheck.app import run; run(host='0.0.0.0',port=8001)"]
