'''
This module provides functionality to run a unittest script or multiple unittest scripts
in any order, for any amount of iterations desired. Scripts can be run in random order,
source code order, alphabetical order, or a list of tests can be given to run.
'''
import sys
import inspect
import unittest

class SystemTestRunner():
    '''
    The SystemTestRunner allows for abstraction and testing of the 
    system_test module itself.
    '''
    def __init__(self, module_names):
        '''
        Create the initial list for modules. 
        Cast module_names to a list in case only one name is provided.
        '''
        if isinstance(module_names, str):
            self.module_names = [module_names]
        else:
            self.module_names = module_names

    def get_requested_order_suite(tests_to_run):
        '''
        Return a suite of tests to run in the order defined by tests_to_run;
        tests_to_run should be a list of strings.
        '''
        test_classes = get_classes()

        # A dictionary is used for O(n) efficiency versus a list,
        # which would yeild O(n^2) efficiency.
        methods = {}

        # This loop maps the all of method objects in this module to their names
        for test_case in test_classes:
            for function in test_case.__dict__:
                test_method = getattr(test_case, function)
                if callable(test_method) and not function.startswith('__'):
                    methods[test_method.__name__] = test_method

        # Now generate the test suite in the order of the list declared above
        suite = unittest.TestSuite()
        for method_name in tests_to_run:
            try:
                real_test_case = methods[method_name]
                name_list = real_test_case.__qualname__.split('.')
                class_name = name_list[0]
                real_method_name = name_list[1]
                if 'test' in real_method_name:
                    test_case_class = getattr(sys.modules[__name__], class_name)
                    suite.addTest(test_case_class(real_method_name))
            except KeyError as error:
                # This error is thrown if the test case declared in tests_to_run
                # is not actually in the source code.
                logging.info(str(error) + ' is not a method in this unittest.\n'
                             + 'Please check your spelling in the specific listing order.')
        return suite


    def get_random_order_suite():
        '''
        Run every test in this module in random order, not
        just each class in random order.
        '''
        # Get all of the classes in this module
        test_classes = get_classes()

        # This loop maps the all of method objects in this module to their names
        methods = []
        for test_case in test_classes:
            for function in test_case.__dict__:
                test_method = getattr(test_case, function)
                if callable(test_method) and not function.startswith('__'):
                    methods.append(test_method)

        rand_generator = random.Random()
        sort_function = lambda : rand_generator.randint(-RANDOM_RANGE_CONSTANT,
                                                      RANDOM_RANGE_CONSTANT + 1)
        random_methods = sorted(methods, key=sort_function)
        display_list = []
        suite = unittest.TestSuite()
        for method_object in random_methods:
            name_list = method_object.__qualname__.split('.')
            class_name = name_list[0]
            method_name = name_list[1]
            if 'test' in method_name:
                display_list.append(method_name)
                test_case_class = getattr(sys.modules[__name__], class_name)
                suite.addTest(test_case_class(method_name))
        logging.info('Running tests in the following order: ' + str(display_list))
        return suite

    def order_classes(run_type=None):
        '''
        Given the run type, sort the members of this module into distinct
        test classes and return a list of them.

        If no run type is given, classes will be run in alphabetical order
        '''
        test_classes = get_classes()

        if run_type is None:
            return test_classes

        if run_type == 'random_order':
            rand_generator = random.Random()
            sort_function = lambda x: rand_generator.randint(-RANDOM_RANGE_CONSTANT,
                                                             RANDOM_RANGE_CONSTANT + 1)
        elif run_type == 'source_order':
            sort_function = lambda x: inspect.findsource(x)[1]

        return sorted(test_classes, key=sort_function)

    def set_run_type(loader, class_object, run_type=None):
        '''
        Pass strings to this method to change your test execution order
        if none are passed, the tests are run in alphabetical order.
        '''
        if run_type == 'random_order':
            # Run tests in a random order, this order changes every time main is called
            # This order is useful to ensure that your tests are truly independent.
            seed = time.time()
            custom_random = random.Random()
            custom_random.seed(seed)
            loader.sortTestMethodsUsing = lambda x, y: custom_random.randint(-RANDOM_RANGE_CONSTANT,
                                                                             RANDOM_RANGE_CONSTANT + 1)
            logging.info('Running ' + class_object.__name__ + ' in the following psuedo random order : '
                         + str(loader.getTestCaseNames(class_object)))
            # Reinitialize the random object so that when the loader actually loads the
            # tests, you get the same order as the displayed list. If you don't understand
            # why this works, research psuedo random numbers.
            custom_random = random.Random()
            custom_random.seed(seed)

        if run_type == 'source_order':
            # Source order means the order the tests appear in the source code.
            # To sort by this order, you use the method's name to get its line
            # number. Then you subtract the line numbers of two methods to get
            # an integer value for sorting.
            logging.info('Running ' + class_object.__name__ + ' in source code order.')
            line_number = lambda m: getattr(class_object, m).__code__.co_firstlineno
            line_number_compare = lambda x, y: line_number(x) - line_number(y)
            loader.sortTestMethodsUsing = line_number_compare

    def get_classes(self):
        '''
        Get a list of all of the class objects in the target modules.
        '''
        classes = []
        all_members = []
        test_classes = []
        for module_name in self.module_names:
            # sys.modules is a dictionary
            classes = sys.modules[module_name]
            all_members += inspect.getmembers(classes)
        test_classes = []
        # There are several members of this module which are not test classes
        # parse them out.
        for _, module_object in all_members:
            if inspect.isclass(module_object) and 'Test' in module_object.__name__:
                test_classes.append(module_object)
        return test_classes