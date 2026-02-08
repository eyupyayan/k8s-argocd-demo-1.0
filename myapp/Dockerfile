FROM python:3.12-slim

WORKDIR /app

# Kopier requirements først
COPY app/requirements.txt /app/requirements.txt

# Installer som root
RUN pip install --no-cache-dir -r /app/requirements.txt

# Lag user etter install
RUN useradd -m appuser

# Kopier kode
COPY app /app/app
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
