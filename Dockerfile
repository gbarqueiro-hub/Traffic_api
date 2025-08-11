FROM python:3.11-slim

# Configurações para Python não criar .pyc e fazer flush de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema (incluindo PostGIS libs)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    binutils libproj-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório do app
WORKDIR /app

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código
COPY . .

# Porta para Django
EXPOSE 8000

CMD ["gunicorn", "traffic_api.wsgi:application", "--bind", "0.0.0.0:8000"]
