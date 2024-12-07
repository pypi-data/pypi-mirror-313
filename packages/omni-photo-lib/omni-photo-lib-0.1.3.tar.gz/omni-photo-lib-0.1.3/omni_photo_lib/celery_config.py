from celery import Celery

def make_celery(app_name, broker_url, backend_url):
    """
    Initialize and return a Celery instance.
    """
    celery = Celery(
        app_name,
        broker=broker_url,
        backend=backend_url,
    )
    return celery
