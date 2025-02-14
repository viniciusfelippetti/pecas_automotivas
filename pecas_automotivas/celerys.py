import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pecas_automotivas.settings')

app = Celery('pecas_automotivas')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['comum'])

# Configurações do broker (Redis neste exemplo)
app.conf.broker_url = 'redis://localhost:6379/0'