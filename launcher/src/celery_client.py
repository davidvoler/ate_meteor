__author__ = 'davidl'
from tasks import run_sequence
import uuid

uuts = [{'serial': '11101'}, {'serial': '11102'}, {'serial': '11103'}, {'serial': '11104'}]
sequence = [
    {'name': 'test1_ps_locked',
     'unique_lock': None,
     'wait_lock': None},
    {'name': 'test2',
     'unique_lock': None,
     'wait_lock': None},
    {'name': 'test3',
     'unique_lock': None,
     'wait_lock': None},
    {'name': 'test4',
     'unique_lock': None,
     'wait_lock': None},
    {'name': 'test5_on_switch',
     'unique_lock': None,
     'wait_lock': 'on_switch'}
]
execution_id = str(uuid.uuid4())
for uut in uuts:
    run_sequence.delay(execution_id, uut, sequence)
