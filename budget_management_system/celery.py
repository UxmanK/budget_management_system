import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_management_system.settings')

app = Celery('budget_management_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'daily-reset': {
        'task': 'budget.tasks.daily_reset',
        'schedule': crontab(hour=0, minute=0),  # Midnight
    },
    'monthly-reset': {
        'task': 'budget.tasks.monthly_reset',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
    'check-dayparting-hourly': {
        'task': 'budget.tasks.check_dayparting',
        'schedule': crontab(minute=0),
    },
    'check-budgets-every-5-min': {
        'task': 'budget.tasks.check_all_campaign_budgets',
        'schedule': crontab(minute='*/5'),
    },
}