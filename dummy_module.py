'''
This module provides dummy information for the system_test_test module.
'''
import unittest

class DummyTests(unittest.TestCase):
    def test_nothing(self):
        pass

class DummyClass():
    '''
    This class should not be found by SystemTestRunner.get_classes()
    '''
    def do_nothing():
        pass
