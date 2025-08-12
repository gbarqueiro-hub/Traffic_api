# Traffic API

API REST para monitoramento de tráfego rodoviário, desenvolvida com Django Rest Framework e suporte a dados geoespaciais.

## 🚀 Funcionalidades
- CRUD de segmentos de estrada (com geometria e velocidade média).
- CRUD de leituras de velocidade média por segmento.
- Cálculo dinâmico da intensidade de tráfego (Baixa, Média, Elevada).
- Contagem total de leituras por segmento.
- Permissões:
  - **Administrador**: criar, ler, atualizar, excluir.
  - **Manager**: criar, ler, atualizar, sem excluir.
  - **Anônimo**: somente leitura.
- Documentação interativa da API com Swagger e ReDoc.

## 📦 Requisitos
- Python 3.10+
- PostgreSQL + PostGIS
- pipenv ou virtualenv

## ⚙️ Instalação

```bash
# 1. Clonar repositório
git clone https://github.com/SEU_USUARIO/Traffic_api.git
cd Traffic_api

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com dados do banco

# 5. Criar tabelas no banco
python manage.py migrate

# 6. (Opcional) Importar dados iniciais
# Se necessário, execute o script de importação
python manage.py import_data
