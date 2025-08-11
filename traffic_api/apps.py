from django.apps import AppConfig

class TrafficApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'traffic_api'

    def ready(self):
        import traffic_api.signals  # importa signals para registar os handlers
