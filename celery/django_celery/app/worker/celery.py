import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from django.conf import settings

# Reference: https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('worker') # type: ignore

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.update(
#     task_routes = {
#         'worker.tasks.fetch_data_for_location': {
#             'queue': 'queue1'
#         },
#         'worker.tasks.send_weather_data_to_server': {
#             'queue': 'queue2'
#         }
#     },
# )

# Rate limiting
# app.conf.task_default_rate_limit = '5/m'  # 5 tasks per minute

# Redis specific
# https://docs.celeryq.dev/en/stable/userguide/routing.html#redis-message-priorities
# app.conf.broker_transport_options = {
#     'priority_steps': list(range(10)), # default is 4
#     # 'sep': ':',
#     'queue_order_strategy': 'priority',
# }
# """
# ['celery', 'celery:1', 'celery:2', 'celery:3', 'celery:4', 'celery:5', 'celery:6', 'celery:7', 'celery:8', 'celery:9']
# """

# app.conf.task_routes = {
#     'worker.tasks.dumb': {
#         'queue': 'queue1'
#     },
#     'worker.tasks.send_weather_data_to_server': {
#         'queue': 'queue2'
#     }
# }

# Load task modules from all registered Django apps.
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
"""
looking for all the tasks like below:
- app1/
    - tasks.py
    - models.py
- app2/
    - tasks.py
    - models.py
"""

# Periodic task & Cron Table

app.conf.beat_schedule = {
    # 'fct_land_forecast_5_11_17': {
    #     'task': 'worker.tasks.fct_land_forecast',
    #     'schedule': crontab(hour='5,11,17'),
    #     'args': (),
    # },
    # 'fct_ocean_forecast_5_11_17': {
    #     'task': 'worker.tasks.fct_ocean_forecast',
    #     'schedule': crontab(hour='5,11,17'),
    #     'args': (),
    # },
    # 'fct_mid_land_temp_forecast_6_18': {
    #     'task': 'worker.tasks.fct_mid_land_temp_forecast',
    #     'schedule': crontab(hour='6,18'),
    #     'args': (),
    # },
    # 'fct_mid_land_status_forecast_6_18': {
    #     'task': 'worker.tasks.fct_mid_land_status_forecast',
    #     'schedule': crontab(hour='6,18'),
    #     'args': (),
    # }
    # ,
    #     'sunrise_sunset_data': {
    #     'task': 'worker.tasks.sunrise_sunset_data',
    #     'schedule': crontab(minute=10)

    # },
    'data_by_shot_forecast-초단기실황조회': {
        'task': 'worker.tasks.data_by_shot_forecast',
        'schedule': crontab(minute=30, hour='*'),
        'args': ('초단기실황조회',),
    },
    'data_by_shot_forecast-초단기예보조회': {
        'task': 'worker.tasks.data_by_shot_forecast',
        'schedule': crontab(minute=30, hour='*'),
        'args': ('초단기예보조회',),
    },
    'data_by_shot_forecast-단기예보 조회': {
        'task': 'worker.tasks.data_by_shot_forecast',
        'schedule': crontab(minute=0, hour=5),
        'args': ('단기예보조회',),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

