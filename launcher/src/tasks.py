from celery import Celery
import time
from random import randrange
from redlock import RedLock
import uuid
from api.python.locks import ExecutionStatusLock, SharedWaitResource
from tornado.options import options
import pymongo

app = Celery('proj', broker='amqp://localhost//', backend='redis://localhost')
import config

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)

mongo_client = pymongo.MongoClient(options.mongo_db_host)
db = mongo_client[options.mongo_db_name]

from MeteorClient import MeteorClient

client = MeteorClient('ws://127.0.0.1:3000/websocket', auto_reconnect=False)
client.connect()


def callback_function(error, result):
    if error:
        print(error)
        return
    print(result)


def report_execution_status(fixture_id, status):
    return True
    fixture = db['fixture'].find_one(fixture_id)
    fixture['status'] = status
    db['fixture'].update({'_id': fixture_id}, {"$set": fixture}, upsert=False, manipulate=True, safe=True)


def report_sequence_status_old(fixture_id, cavity, status):
    fixture = db['fixture'].find_one(fixture_id)
    fixture['status'] = status
    for i in range(len(fixture['cavities'])):
        # print (i, cavity['id'])
        if fixture['cavities'][i]['id'] == cavity['id']:
            fixture['cavities'][i]['status'] = status
    db['fixture'].update({'_id': fixture_id}, {"$set": fixture}, upsert=False, manipulate=True, safe=True)


def report_sequence_status(fixture_id, cavity, status, progress):
    try:
        client.call('setCavityStatus', [fixture_id, cavity['id'], status, progress], callback_function)
    except Exception as e:
        print(e)
        # if the exception is broken pipe - with server write directly to mongo
        try:
            fixture = db['fixture'].find_one(fixture_id)
            fixture['cavities'][cavity['id']]['status'] = status
            fixture['cavities'][cavity['id']]['progress'] = progress

            fprogress = 0
            for c in fixture['cavities']:
                if c['status'] == 'fail':
                    fprogress += 100
                else:
                    fprogress += c['progress']
            fixture['progress'] = fprogress / len(fixture['cavities'])
            db['fixture'].update({'_id': fixture_id}, fixture)
        except Exception as e:
            print (e)


def report_lock_status(fixture_id, lock, status):
    try:
        client.call('setLockStatus', [fixture_id, lock,status], callback_function)
    except Exception as e:
        print(e)


def rand_verdict():
    # return True
    r = randrange(0, 35)
    if r % 34 == 0:
        return False
    else:
        return True


def run_test(fixture_id, exc_lock, uut, test, progress, unique_res=None, wait_res=None):
    """
    Temporary test runner
    :param uut:
    :param test:
    :return:
    """
    print (test)
    report_sequence_status(fixture_id, uut, test, progress)
    if wait_res:
        exc_lock.wait_for_all(wait_res)

    lock = None
    if unique_res:
        res_lock = RedLock(unique_res)
        report_lock_status(fixture_id, unique_res,True)
        lock = res_lock.acquire()
        while not lock:
            time.sleep(0.02)
            lock = res_lock.acquire()
        print ('locking {}'.format(unique_res))
    time.sleep(randrange(10, 3500) / 1000.0)
    # todo use REST api to set function status
    verdict = rand_verdict()
    payload = {'verdict': verdict, 'test': test, 'uut': uut}  # ,'execution_id':execution_id, 'process_id':process_id}
    print (payload)
    if lock:
        print ('releasing {}'.format(unique_res))
        res_lock.release()
        report_lock_status(fixture_id, unique_res,False)
    return verdict


@app.task
def run_sequence(fixture_id, execution_id, uut, sequence):
    process_id = str(uuid.uuid4())
    report_sequence_status(fixture_id, uut, 'started', 0)
    exc_lock = ExecutionStatusLock(execution_id, process_id)
    print ('Starting Sequence uut:{} cavity:{}'.format(uut['serial'], uut['id']))
    # return True
    # print (sequence)
    for test in sequence:
        if not run_test(fixture_id, exc_lock, uut, test['name'], test['progress'], test['unique_lock'],
                        test['wait_lock']):
            print ('UUT Serial:{} Failed'.format(uut['serial']))
            exc_lock.end_process()
            report_sequence_status(fixture_id, uut, 'fail', test['progress'])
            return False
    print ('UUT Serial:{} Success'.format(uut['serial']))
    exc_lock.end_process()
    report_sequence_status(fixture_id, uut, 'success', 100)
    # client.close()
    return True
