from __future__ import absolute_import, unicode_literals

import logging
import os

from celery import Celery

# setting the Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    logging.info(f"Request: {self.request!r}")


@app.task(bind=True)
def query_scheduler_task(self, query_scheduler_id):
    logging.info(f"Request: {self.request!r}")
    logging.info(f"query_scheduler_id: {query_scheduler_id}")
