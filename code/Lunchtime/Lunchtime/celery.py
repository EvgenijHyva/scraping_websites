from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lunchtime.settings')

app = Celery('Lunchtime')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Helsinki')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')  #'django.conf:settings'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# database beat
# celery -A Lunchtime beat -l INFO
# +
# celery -A Lunchtime worker --pool=solo -l INFO

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    "run-scrapy-every-monday": {
        "task": "parsers_app.tasks.run_scrapy_task",
        "schedule": crontab(day_of_week=1, hour=1)
    },
    "run-scrapy-demo": {
        "task": "parsers_app.tasks.run_scrapy_task",
        "schedule": crontab(minute="*/5")
    },

}

