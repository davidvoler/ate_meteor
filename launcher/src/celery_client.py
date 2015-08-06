__author__ = 'davidl'
from tasks import run_sequence

uuts = [{'serial':'11101'},{'serial':'11102'},{'serial':'11103'},{'serial':'11104'}]
sequence = [
    {'name':'test1_ps_locked',
     'unique_lock':'ps',
     'wait_lock':None},
    {'name':'test2',
     'unique_lock':None,
     'wait_lock':None},
    {'name':'test3',
     'unique_lock':None,
     'wait_lock':None},
    {'name':'test4',
     'unique_lock':None,
     'wait_lock':None},
    {'name':'test5_print_locked',
     'unique_lock':'print',
     'wait_lock':None}
]
for uut in uuts:
    run_sequence.delay(uut, sequence)
