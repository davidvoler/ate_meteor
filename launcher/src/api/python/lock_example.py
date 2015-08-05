__author__ = 'davidl'
import time
from redlock import RedLock
from redis import Redis

dlm = RedLock('example')
my_lock = dlm.acquire()
print ('now example is locked')
dlm.release()
print ('now example it is free')


def shared_resource_wait_lock(execution_id, resource, state, retry=100, delay=0.03):
    """
    A shared resource that requires to wait for all current running uuts
    Implement with redis
    :param resource:
    :param state:
    :param retry: Number of time to
    :param delay:
    :return:
    """
    redis_db = Redis()
    # if number of active execution == 1, no need for a lock, just return True:
    if redis_db.get("active:{}".format(execution_id)) == 1:
        return True
    # create a
    lck = RedLock("access_wait_{}:{}".format(resource, execution_id))
    if redis_db.get("{}:{}".format(resource, execution_id)):
        # Add self to the list of waiting processes

        # If waiting process equal active process: enable this lock
        pass
    else:
        set("{}:{}".format(resource, execution_id), {'wating': 1})
        pass


class SharedWaitResource(object):
    """
    Process safe shared resource shared amongst few running process.
    Scenario:
    The first process may change the resource state (on/off)
    Then it should wait for other running process to get to the point where the resource is needed.
    When all Active process
    """

    def __init__(self, execution_id, resource, process_id):
        self.redis = Redis()
        self.execution_id = execution_id
        self.resource = resource
        self.process_id = process_id
        self.key = '{}:{}'.format(self.execution_id, self.resource)
        self.active_key = 'active:{}'.format(self.execution_id)
        self.access_key = RedLock('access:{}:{}'.format(self.execution_id, self.resource))

    def active_process(self):
        active = self.redis.get(self.active_key)
        return active

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
            'waiting': []
        }
        self.redis.setnx(self.key, resource_key)
        resource_key = self.redis.get(self.key)
        if resource_key['state'] == state:
            return True
        else:
            return False

    def when_ready(self, retry=100, interval=0.005):
        self.access_key.acquire()
        # What if lock
        resource_key = self.redis.get(self.key)
        if not resource_key:
            # Someone deleted the resource or it was never created. Raise Exception
            return False
        else:
            if self.process_id not in resource_key['waiting']:
                resource_key['waiting'].append(self.process_id)
            self.redis.set(self.key, resource_key)
        self.access_key.release()
        for i in range(0, retry):
            resource_key = self.redis.get(self.key)
            if len(resource_key['waiting']) >= self.active_process():
                return True
            else:
                time.sleep(interval)
        # here we should raise timeout exception
        return False

    def set_and_wait(self, state, retry=100, interval=0.005):
        if not self.set_state(state):
            return False
        return self.when_ready(retry, interval)
