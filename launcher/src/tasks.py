from celery import Celery
import time
from random import randrange
from redlock import RedLock

app = Celery('hello', broker='amqp://localhost//', backend='redis://localhost')


def rand_verdict():
    return True
    """
    r = randrange(0, 25)
    if r % 15 == 0:
        return False
    else:
        return True
    """


def run_test(uut, test, unique_res=None, wait_res=None):
    """
    Temporary test runner
    :param uut:
    :param test:
    :return:
    """

    lock = None
    if unique_res:
        res_lock = RedLock(unique_res)
        lock = res_lock.acquire()
        while not lock:
            time.sleep(0.02)
            lock = res_lock.acquire()
        print ('locking {}'.format(unique_res))
    time.sleep(randrange(1, 1500) / 1000.0)
    # todo use REST api to set function status
    verdict = rand_verdict()
    payload = {'verdict': verdict, 'test': test, 'uut': uut}
    print (payload)
    if lock:
        print ('releasing {}'.format(unique_res))
        res_lock.release()
    return verdict


@app.task
def run_sequence(uut, sequence):
    print ('Starting Sequence uut:{}'.format(uut['serial']))
    # print (sequence)
    for test in sequence:
        if not run_test(uut, test['name'], test['unique_lock']):
            print ('UUT Serial:{} Failed'.format(uut['serial']))
            return False
    print ('UUT Serial:{} Success'.format(uut['serial']))
    return True
