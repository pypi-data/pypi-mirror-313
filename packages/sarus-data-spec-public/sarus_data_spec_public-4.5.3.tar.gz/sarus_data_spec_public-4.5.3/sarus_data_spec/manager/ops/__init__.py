try:
    from celery import Celery

    runner = Celery(
        "tasks", broker="redis://localhost", backend="redis://localhost"
    )
except ModuleNotFoundError:
    pass
