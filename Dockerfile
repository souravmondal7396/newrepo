FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 AEGIS_DATA_DIR=/var/lib/aegis
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
RUN useradd --create-home --uid 10001 aegis && mkdir -p /var/lib/aegis && chown -R aegis:aegis /app /var/lib/aegis
USER aegis
EXPOSE 8080
HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')"
CMD ["uvicorn", "aegis.api:app", "--host", "0.0.0.0", "--port", "8080"]
