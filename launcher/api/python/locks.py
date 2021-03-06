__author__ = 'davidl'
import time
from redlock import RedLock
from redis import Redis
import pickle

"""
dlm = RedLock('example')
my_lock = dlm.acquire()
print ('now example is locked')
dlm.release()
print ('now example it is free')
"""


class ExecutionStatusLock(object):
    def __init__(self, execution_id, process_id):
        self.redis = Redis()
        self.execution_id = execution_id
        self.process_id = process_id
        self.active_key = 'active:{}'.format(self.execution_id)
        self.redis.hset(self.active_key, self.process_id, 1)
        print ('process_id:{} - is now active'.format(self.process_id))

    def end_process(self):
        self.redis.hdel(self.active_key, self.process_id)
        print ('process_id:{} - exited'.format(self.process_id))

    def _are_all_ready(self, resource):
        pipe = self.redis.pipeline()
        pipe.hlen(self.active_key)
        pipe.hlen('{}:{}'.format(self.execution_id, resource))
        res = pipe.execute()
        # print(res)
        if res[0] <= res[1]:
            return True
        else:
            return False

    def wait_for_all(self, resource, retry=6000, interval=0.01):
        resource_key = '{}:{}'.format(self.execution_id, resource)
        self.redis.hset(resource_key, self.process_id, 1)
        print ('Waiting for all:{}'.format(resource))
        for i in range(retry):
            if self._are_all_ready(resource):
                print ('Resource :{} after {} retry'.format(resource, i))
                return True
            time.sleep(interval)
        print('Expired after {} seconds'.format(retry * interval))
        return False


class SharedWaitResource(object):
    """
    Process safe shared resource shared amongst few running process.
    Scenario:
    The first process may change the resource state (on/off)
    Then it should wait for other running process to get to the point where the resource is needed.
    When all Active process
    """

    def __init__(self, execution_id, process_id, resource):
        self.redis = Redis()
        self.execution_id = execution_id
        self.resource = resource
        self.process_id = process_id
        self.key = '{}:{}'.format(self.execution_id, self.resource)
        self.active_key = 'active:{}'.format(self.execution_id)

    def active_process(self):
        active = self.redis.get(self.active_key)
        print ('Active Process:{}'.format(active))
        print (active)
        return len(active)

    def get_state(self):
        resource_key = {
            'state': None,
            'waiting': []
        }
        self.redis.setnx(self.key, resource_key)
        resource_key = self.redis.get(self.key)
        return resource_key['state']

    def set_state(self, state):
        resource_key = {
            'state': state,
            'waiting': [self.process_id]
        }

        self.redis.setnx(self.key, resource_key)
        resource_key = self.redis.get(self.key)
        print (resource_key)
        print (resource_key)
        print (type(resource_key))

        if resource_key['state'] == state:
            return True
        else:
            return False

    def when_ready(self, retry=500, interval=0.02):
        print ('when_ready')
        # self.access_key.acquire()
        # What if lock
        resource_key = self.redis.get(self.key)
        print(resource_key)
        if not resource_key:
            # Someone deleted the resource or it was never created. Raise Exception
            print ('when_ready: no resource key')
            return False
        else:
            if self.process_id not in resource_key['waiting']:
                resource_key['waiting'].append(self.process_id)
            self.redis.set(self.key, resource_key)
        self.access_key.release()
        for i in range(0, retry):
            resource_key = self.redis.get(self.key)
            print (resource_key)

            if len(resource_key['waiting']) >= self.active_process():
                return True
            else:
                time.sleep(interval)
        # here we should raise timeout exception
        print ('when_ready: Exceeded wait time')
        return False

    def set_and_wait(self, state, retry=500, interval=0.02):
        if not self.set_state(state):
            print ('set_and_wait:Fail')
            return False
        return self.when_ready(retry, interval)
