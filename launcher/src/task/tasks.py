__author__ = 'davidl'

from celery import Celery

app = Celery('tasks', broker='amqp://guest@localhost//')


@app.task
def run_sequence(sequence, device):
    pass


def run_execution(sequence, devices):
    for device in devices:
        run_sequence.delay((sequence, device))
