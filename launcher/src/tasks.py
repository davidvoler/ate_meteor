from celery import Celery
import time
from random import randrange
from redlock import RedLock
import uuid
from api.python.locks import ExecutionStatusLock, SharedWaitResource
from tornado.options import options
import pymongo

app = Celery('hello', broker='amqp://localhost//', backend='redis://localhost')
import config

mongo_client = pymongo.MongoClient(options.mongo_db_host)
db = mongo_client[options.mongo_db_name]


def report_execution_status(fixture_id, status):
    fixture = db['fixture'].find_one(fixture_id)
    fixture['status'] = status
    db['fixture'].update({'_id': fixture_id}, {"$set": fixture}, upsert=False, manipulate=True, safe=True)



def report_sequence_status(fixture_id, cavity, status):
    fixture = db['fixture'].find_one(fixture_id)
    fixture['status'] = status
    for i in range(len(fixture['cavities'])):
        # print (i, cavity['id'])
        if fixture['cavities'][i]['id'] == cavity['id']:
            fixture['cavities'][i]['status'] = status
    db['fixture'].update({'_id': fixture_id}, {"$set": fixture}, upsert=False, manipulate=True, safe=True)


def report_lock_status():
    pass


def rand_verdict():
    return True
    r = randrange(0, 35)
    if r % 17 == 0:
        return False
    else:
        return True


def run_test(fixture_id, exc_lock, uut, test, unique_res=None, wait_res=None):
    """
    Temporary test runner
    :param uut:
    :param test:
    :return:
    """
    print (test)
    report_sequence_status(fixture_id, uut, test)
    if wait_res:
        exc_lock.wait_for_all(wait_res)

    lock = None
    if unique_res:
        res_lock = RedLock(unique_res)
        lock = res_lock.acquire()
        while not lock:
            time.sleep(0.02)
            lock = res_lock.acquire()
        print ('locking {}'.format(unique_res))
    time.sleep(randrange(1000, 3500) / 1000.0)
    # todo use REST api to set function status
    verdict = rand_verdict()
    payload = {'verdict': verdict, 'test': test, 'uut': uut}  # ,'execution_id':execution_id, 'process_id':process_id}
    print (payload)
    if lock:
        print ('releasing {}'.format(unique_res))
        res_lock.release()
    return verdict


@app.task
def run_sequence(fixture_id, execution_id, uut, sequence):
    process_id = str(uuid.uuid4())
    report_sequence_status(fixture_id, uut , 'started')
    exc_lock = ExecutionStatusLock(execution_id, process_id)
    print ('Starting Sequence uut:{} cavity:{}'.format(uut['serial'], uut['id']))
    # return True
    # print (sequence)
    for test in sequence:
        if not run_test(fixture_id, exc_lock, uut, test['name'], test['unique_lock'], test['wait_lock']):
            print ('UUT Serial:{} Failed'.format(uut['serial']))
            exc_lock.end_process()
            report_sequence_status(fixture_id, uut, 'fail')
            return False
    print ('UUT Serial:{} Success'.format(uut['serial']))
    exc_lock.end_process()
    report_sequence_status(fixture_id, uut, 'success')
    return True
