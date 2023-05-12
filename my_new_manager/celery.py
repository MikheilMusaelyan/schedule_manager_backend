import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_new_manager.settings')


app = Celery('my_new_manager')

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()