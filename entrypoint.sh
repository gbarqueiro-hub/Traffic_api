#!/bin/sh

echo "TrafficApiLogs : Aguardando base de dados..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.5
done
echo "TrafficApiLogs :Base de dados pronta!"

# Aplicar migrações
python manage.py migrate --noinput

# Carregar fixtures iniciais se existirem
if [ -f /app/initial_data.json ]; then
    python manage.py loaddata initial_data.json
fi

# Criar superuser automático (opcional)
if [ "$CREATE_SUPERUSER" = "1" ]; then
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin1234")
EOF
fi

exec "$@"
