'''
This is a unit test for the system_test module.

@Author Connor J. Summeril
'''
import unittest
import system_test
import dummy_module

def main():
    unittest.main()

class SystemTestTests(unittest.TestCase):
    '''
    The class which contains the unit tests for the system_test module
    '''
    
    def test_get_classes_one_module(self):
        '''
        Test that the get_classes method can successfully return all test classes
        from one module.
        '''
        # Arrange
        expected_classes = [BarTests, FooTests, SystemTestTests]
        # Normally you would input the module's name. Using '__main__' is a special
        # case since the classes in the running module are being analyzed.
        test_runner = system_test.SystemTestRunner('__main__')
        # Act
        actual_classes = test_runner.get_classes()
        # Assert
        self.assertEqual(expected_classes, actual_classes)

    def test_get_classes_multiple_modules(self):
        # Arrange
        expected_classes = [BarTests, FooTests, SystemTestTests, dummy_module.DummyTests]
        test_runner = system_test.SystemTestRunner(['__main__', 'dummy_module'])
        # Act
        actual_classes = test_runner.get_classes()
        # Assert
        self.assertEqual(expected_classes, actual_classes)

class FooTests(unittest.TestCase):
    '''
    This is a dummy class used for testing.
    '''
    pass

class BarTests(unittest.TestCase):
    '''
    This is a dummy class used for testing.
    '''
    pass

if __name__ == '__main__':
    main()