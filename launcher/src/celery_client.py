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
        {'name': 'test5',
         'unique_lock': None,
         'wait_lock': None},
        {'name': 'test6_ps',
         'unique_lock': 'ps',
         'wait_lock': None},
        {'name': 'test7',
         'unique_lock': None,
         'wait_lock': None},
        {'name': 'test8',
         'unique_lock': None,
         'wait_lock': None},
        {'name': 'test_on_switch',
         'unique_lock': None,
         'wait_lock': 'on_switch'}
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
