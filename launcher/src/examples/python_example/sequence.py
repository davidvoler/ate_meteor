__author__ = 'davidl'
import sys
import time
from random import randrange
import requests

STATUS_URL = 'http://localhost:7919'


def rand_verdict():
    r = randrange(0, 10)
    if r % 4 == 0:
        return False
    else:
        return True

def test(name, resource_lock=None, resource_wait=None):
    time.sleep(randrange(1, 1500) / 1000.0)
    # todo use REST api to set function status
    verdict = rand_verdict()
    payload = {'verdict': verdict, 'name': name}
    print (payload)
    #requests.get("http://httpbin.org/get", data=payload)



def main(argv):
    # print argv
    test(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
