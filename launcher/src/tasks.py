from celery import Celery
import time
from random import randrange

app = Celery('hello', broker='amqp://localhost//', backend='redis://localhost')


def rand_verdict():
    r = randrange(0, 25)
    if r % 8 == 0:
        return False
    else:
        return True


def run_test(uut, test):
    """
    Temporary test runner
    :param uut:
    :param test:
    :return:
    """
    time.sleep(randrange(1, 1500) / 1000.0)
    # todo use REST api to set function status
    verdict = rand_verdict()
    payload = {'verdict': verdict, 'test': test, 'uut': uut}
    print (payload)
    return verdict


@app.task
def run_sequence(uut, sequence):
    print ('Starting Sequence uut:{}'.format(uut['serial']))
    # print (sequence)
    for test in sequence:
        if not run_test(uut, test):
            print ('UUT Serial:{} Failed'.format(uut['serial']))
            return False
    print ('UUT Serial:{} Success'.format(uut['serial']))
    return True
