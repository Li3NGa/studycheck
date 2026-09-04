FROM python:3.12-slim
WORKDIR /app
ENV PYTHONPATH=/app PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 STUDYCHECK_HOST=0.0.0.0 STUDYCHECK_PORT=8001 STUDYCHECK_DB=/data/studycheck.db
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home --uid 10001 appuser && mkdir -p /app/uploads /data && chown -R appuser:appuser /app /data
USER appuser
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8001/health',timeout=3)"
CMD ["python","-c","from studycheck.app import run; run()"]
