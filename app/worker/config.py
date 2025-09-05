import os
from datetime import timedelta

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Celery configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# SSL certificate warning threshold (days)
SSL_WARNING_THRESHOLD = 14

# Default timeout for HTTP requests (seconds)
DEFAULT_TIMEOUT = 10

# Beat schedule configuration
CELERY_BEAT_SCHEDULE = {
    'check-google': {
        'task': 'tasks.check_website',
        'schedule': timedelta(minutes=5),
        'args': ('https://google.com',),
        'kwargs': {'timeout': 10}
    },
    'check-github': {
        'task': 'tasks.check_website',
        'schedule': timedelta(minutes=10),
        'args': ('https://github.com',),
        'kwargs': {'timeout': 15}
    },
    # Добавьте свои проверки здесь
}

CELERY_TIMEZONE = os.getenv("TZ")

