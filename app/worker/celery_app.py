from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND, CELERY_BEAT_SCHEDULE, CELERY_TIMEZONE

app = Celery('website_cheker',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['tasks'])

app.conf.update(
    timezone=CELERY_TIMEZONE,
    beat_schedule=CELERY_BEAT_SCHEDULE,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

if __name__ == "__main__":
    app.start()