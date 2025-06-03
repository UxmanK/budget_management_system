import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_management_system.settings')
django.setup()

from django.db import connection
from celery import current_app

print("=== System Check ===")
# Test DB connection
try:
    connection.ensure_connection()
    print("✅ Database connection working")
except Exception as e:
    print(f"❌ Database error: {e}")

# Test Redis connection
try:
    current_app.connection().connect()
    print("✅ Redis connection working")
except Exception as e:
    print(f"❌ Redis error: {e}")

# Test Celery
try:
    from budget.tasks import check_dayparting
    result = check_dayparting.delay()
    if result.ready():
        print("✅ Celery task execution working")
    else:
        print("⚠️ Celery task queued but not processed")
except Exception as e:
    print(f"❌ Celery error: {e}")