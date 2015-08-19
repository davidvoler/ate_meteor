__author__ = 'davidl'
from tasks import run_sequence, report_execution_status
import uuid
import time

def main():
    uuts = [{'serial': '11101', 'id': 0},
            {'serial': '11102', 'id': 1},
            {'serial': '11103', 'id': 2},
            {'serial': '11104', 'id': 3}]
    sequence = [
        {'name': 'test1',
         'unique_lock': None,
         'wait_lock': None,'progress':10},
        {'name': 'test2',
         'unique_lock': None,
         'wait_lock': None,'progress':20},
        {'name': 'test3',
         'unique_lock': None,
         'wait_lock': None,'progress':30},
        {'name': 'test4',
         'unique_lock': None,
         'wait_lock': None,'progress':40},
        {'name': 'test5',
         'unique_lock': None,
         'wait_lock': None,'progress':50},
        {'name': 'test_on_switch',
         'unique_lock': None,
         'wait_lock': 'on_switch','progress':60},
        {'name': 'test6_ps',
         'unique_lock': 'ps',
         'wait_lock': None,'progress':65},
        {'name': 'test7',
         'unique_lock': None,
         'wait_lock': None,'progress':70},
        {'name': 'test8',
         'unique_lock': None,
         'wait_lock': None,'progress':80},
        {'name': 'test9',
         'unique_lock': None,
         'wait_lock': None,'progress':85},
        {'name': 'test10',
         'unique_lock': None,
         'wait_lock': None,'progress':90},
        {'name': 'test11',
         'unique_lock': None,
         'wait_lock': None,'progress':95},
        {'name': 'cleanup',
         'unique_lock': None,
         'wait_lock': None,'progress':100},

    ]
    execution_id = str(uuid.uuid4())
    fixture_id = 'kay8KPM4yGXiCJHui'
    report_execution_status(fixture_id, 'running')
    print (uuts)
    for uut in uuts:
        res = run_sequence.delay(fixture_id, execution_id, uut, sequence)
        print (res)


if __name__ == '__main__':
    main()
