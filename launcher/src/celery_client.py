__author__ = 'davidl'
from tasks import run_sequence

uuts = [{'serial':'11101'},{'serial':'11102'},{'serial':'11103'},{'serial':'11104'}]
sequence = ['test1','test2','test3','test4','test5','test6','test7']
for uut in uuts:
    run_sequence.delay(uut, sequence)
