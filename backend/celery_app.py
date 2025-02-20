from celery import Celery
import redis
import os
from cs50 import SQL

db_path = os.path.join(os.path.dirname(__file__), "cozen.db")

db=SQL(f"sqlite:///{db_path}")



from celery import Celery

def make_celery(app_name=__name__):
    celery = Celery(app_name, broker='redis://localhost:6380/0')
    celery.conf.update(
        result_backend='redis://localhost:6380/0',
        task_track_started=True,  # Track task start times
        worker_concurrency=10,  # The number of greenlets (lightweight threads) to use
        pool='gevent',  # Use gevent pool
    )
    return celery

celery = make_celery()

@celery.task
def cleanup_expired_codes():
    print("Cleaning up expired verification codes...")
    res = db.execute("DELETE FROM VerificationCodes WHERE expires_at < CURRENT_TIMESTAMP")
    print(f'{res.rowcount} expired verification codes deleted')
    if res.rowcount:
        print(f"Deleted expired verification codes")
    else:
        print("No expired verification codes found")
