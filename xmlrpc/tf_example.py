__author__ = 'avraham'
import time


class MyType(type):

    def __new__(cls, name, bases, attrs):
        bases = (object,)
        return super(MyType, cls).__new__(cls, name, bases, attrs)


class TFExample(object):

    """Version 123
This is the docstring for the class, any relevant info should go here
This is the example class for making a TFE compliant class, class names should begin with TF
Use docstring where relevant and @values extension for checkboxes
    """
    __metaclass__ = MyType

    def __init__(self, *args, **kwargs):
        super(TFExample, self).__init__(*args, **kwargs)
        # raise Exception('Azohenvey')
        self.name = 'TFExample'

    # def __del__(self):
        # print('deleting...')

    def no_docs(self, cavity):
        pass

    def sleep5(self):
        """
        Sleeps 5 seconds
        """
        time.sleep(5)
        return "OK", [1, 2, 3], 4.5, {"status": "running"}

    def bad_method(self, x):
        """
        This method divides by zero
        @rtype : int
        @param x: Dummy, it doesn't actually use this
        @return: Won't return because the method should raise an exception when trying to divide by zero
        """
        return 10 / 0

    def add(self, a, b=7):
        """
        This method adds the two parameters and returns the result
        @rtype : int or float
        @return : The sum of the two parameters
        @param a: First parameter
        @param b: Second parameter
        @type b: int or float
        @type a: float
        @values a: 1,2,3,4,5,6,7,8,9,10,11
        """
        return a + b

    def makelist(self, a, b=2, c=3):
        """
        Takes the parameters and insert them in a list as is
        @param a: firstone
        @param b: second
        @param c: third
        @type a: int
        @type b: int
        @type c: int
        @values a: 1,2
        @values b: 3,4
        @values c:5,6
        """
        print 'a', a
        print 'b', b
        print 'c', c
        print a + b
        return [a, b, c]

    def complex_method(self, bcd, adc, zxc, kkk, bbb):
        """
        Takes a lof parameters placed in non alphabetical order
        @rtype : str
        @return : formatted string
        @param bcd: first argument
        @param adc: second argument
        @param zxc: third argument
        @param kkk: fourth argument
        @param bbb: fifth argument
        @type bcd: int
        @type adc: int
        @type zxc: int
        @type kkk: str
        @type bbb: str
        """
        return '{}:{}:{}:{}:{}'.format(bcd, adc, zxc, kkk, bbb)

    def get_tf_name(self, param):
        """
        All TF classes are expected to have this method with this signature, this is used to check if it is online
        @param not used:
        @return: class name
        """
        return self.__class__.__name__

    def tf_list_cavities(self):
        """
        Return a list of cavities
        @param not used:
        @return: a list of cavities
        """

        return ['cavity1', 'cavity2', 'cavity3']

    def tf_health(self):
        return {'fixture_status': {}}
