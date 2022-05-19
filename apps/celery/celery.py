from celery import current_app as current_celery_app
from db_config.config import setting

def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(setting, namespace="CELERY")

    return celery_app