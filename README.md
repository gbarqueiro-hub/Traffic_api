# 🚦 Traffic API

API REST para monitoramento de tráfego rodoviário, desenvolvida com **Django Rest Framework** e suporte a dados **geoespaciais (PostGIS)**.

## 📋 Funcionalidades
- **CRUD** de segmentos de estrada (com geometria e velocidade média).
- **CRUD** de leituras de velocidade média por segmento.
- **Cálculo dinâmico** da intensidade de tráfego (Baixa, Média, Elevada).
- **Contagem de leituras** por segmento.
- **Passagens**:
  - Upload em lote (`bulk_upload`) via API Key.
  - Consulta de passagens por matrícula nas últimas 24h (`/api/passages/car/`).
- **Permissões**:
  - **Administrador**: criar, ler, atualizar, excluir.
  - **Manager**: criar, ler, atualizar (sem excluir).
  - **Anônimo**: somente leitura.
- **Documentação interativa** com Swagger UI e ReDoc.

---

## 📦 Requisitos
- Python 3.10+
- PostgreSQL + PostGIS
- `pipenv` ou `virtualenv` para gerenciamento de dependências
- Docker e Docker Compose (opcional, mas recomendado)

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clonar o repositório
```bash
cd c:/
git clone https://github.com/gbarqueiro-hub/Traffic_api.git
cd Traffic_api
```

### 2️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 3️⃣ Subir containers
```bash
docker-compose up 
```

### 4️⃣  Popular base inicial
```bash
docker-compose exec web python manage.py importstartdb
```

### 6️⃣ Reiniciar
```bash
docker-compose down
docker-compose up
```

---

## 🔑 Credenciais Padrão (dev)
- **manager / ubi12345**
- **SuperUser / ubi12345**
- **admin1 / 1234** (usuário PostgreSQL)

---

## 🗄️ Comandos úteis (Admin / SQL)

Acessar banco:
```bash
docker-compose exec db psql -U admin1 -d traffic
```
Listar tabelas:
```sql
\d traffic_api_roadsegment;
SELECT * FROM traffic_api_passage;
```

---

## 🖥️ Desenvolvimento (VS Code / Django)

Coletar arquivos estáticos:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

Criar novas migrações:
```bash
python manage.py makemigrations traffic_api
```

Reconstruir containers:
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

Apagar volumes (reset DB):
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

Rodar testes:
```bash
docker compose exec web python manage.py test traffic_api
```

---

## 🌐 Endpoints Principais

### CRUD via Router DRF
- `/api/roadsegments/` → **RoadSegmentViewSet** (CRUD + filtros)
- `/api/trafficreadings/` → **TrafficReadingViewSet** (CRUD)
- `/api/sensors/` → **SensorViewSet** (CRUD)

### Endpoints Extras
- `/passages/bulk_upload/` → Upload em lote das passagens (**API Key**)
- `/api/passages/car/` → Consulta passagens de carro nas últimas 24h (**IsAdminUser + parâmetro obrigatório `license_plate`**)

### Documentação Automática
- `/api/schema/`
- `/api/docs/` (Swagger UI)
- `/api/redoc/`

---

## 🧪 Testes via cURL

Listar passagens (últimas 24h, por matrícula):
```bash
curl -u manager:ubi12345 "http://localhost:8000/api/passages/car/?license_plate=ABC1234"
```

Enviar passagens em lote (API Key):
```bash
curl -X POST http://localhost:8000/passages/bulk_upload/ \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: 23231c7a-80a7-4810-93b3-98a18ecfbc42" \
  -d '[{"road_segment":1,"car_license_plate":"ABC1234","timestamp":"2025-08-12T14:30:00Z","sensor_uuid":"270e4cc0-d454-4b42-8682-80e87c3d163c"}]'
```

Listar segmentos de estrada:
```bash
curl -X GET http://localhost:8000/api/roadsegments/
```

Listar leituras de tráfego:
```bash
curl -X GET http://localhost:8000/api/trafficreadings/
```

Listar sensores:
```bash
curl -X GET http://localhost:8000/api/sensors/
```

---

## 📌 Observações
- O endpoint `/api/passages/car/` **sempre requer** `license_plate` e filtra pelas últimas 24 horas.
- O `bulk_upload` insere diretamente no modelo `Passage`, mas o que cada usuário vê depende do **escopo/tenant** e da autenticação usada.
- Para evitar **duplicados**, recomenda-se adicionar constraint única `(car, sensor, timestamp)` ou deduplicar no upload.
