import unittest
from utilities.GenericWait import GenericWait
from datetime import datetime, timedelta


# Unit test for the GenericWait class.
class GenericWaitUnitTest(unittest.TestCase):
    def setUp(self):        # Constant test string.
        self.main_test_string = "Test String"

        # Test override retry time.
        self.test_retry = 200

        # Test override time out time.
        self.test_timeout = 1000

        # Counter for unit tests.
        self.number = 0

    # Test wait until with no parameters works when the wait function returns true.
    # @Test(groups = TestCategories.UTILITIES)
    def test_passNoParamUntilTest(self):
        # have to use an array because the iterator needs to be mutable
        loop = [0]
        try:
            self.assertTrue(GenericWait().wait_until(loop[0] > 3), "Failed no parameter test")
        except Exception as e:
            self.fail("waitUntil no parameter test failed with exception", e.args)

    # Test wait until with an array of parameters works when the wait function returns true.
    # @Test(groups = TestCategories.UTILITIES)
    def test_passObjectArrayUntilTest(self):
        objects = ["one", {}]
        # objects.add(new HashMap<Integer, UUID>());

        try:
            self.assertTrue(GenericWait().wait_until(self.is_two_parameters, objects), "Failed parameter array test")
        except Exception as e:
            self.fail("waitUntil generic object test failed with exception", e)

    # Test wait for with an array of parameters works when the wait function returns true.
    # @Test(groups = TestCategories.UTILITIES)
    def test_passObjectArrayForTest(self):
        objects = ["one", {}]
        # objects.add(new HashMap<Integer, UUID>());

        try:
            GenericWait().wait_for(self.is_two_parameters, objects)
        except Exception as e:
            self.fail("waitFor generic object test failed with exception", e)

    # Test wait until with a single parameter works when the wait function returns false.
    # @Test(groups = TestCategories.UTILITIES)
    def test_failStringUntilTest(self):
        try:
            self.assertFalse(GenericWait().wait_until(self.is_param_test_String("Bad")),
                             "Failed single parameter test")
        except Exception as e:
            self.fail("waitUntil failed with exception", e)

    # Test wait until with a parameter array works when the wait function returns false.
    # @Test(groups = TestCategories.UTILITIES)
    def test_failObjectArrayUntilTest(self):
        objects = []
        try:
            self.assertFalse(GenericWait().wait_until(self.is_two_parameters, objects), "Failed parameter array test")
        except Exception as e:
            self.fail("waitUntil failed with exception", e)

    # Test wait until with a parameter array works when the wait function returns false.
    # @Test(expectedExceptions = UnsupportedOperationException.class, groups = TestCategories.UTILITIES)
    def test_throwExceptionWithoutParamTest(self):
        with self.assertRaises(NotImplementedError):
            try:
                GenericWait().wait_for_true(self.throw_error)
            except Exception as e:
                raise e.args()

    # Test waitForTrue passes.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitForTruePasses(self):
        try:
            GenericWait().wait_for_true(bool(2 == 2))
        except Exception as e:
            self.fail("waitForTrue threw unexpected exception", e)

    # Test waitForTrue passes.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitForTruePassesWithParameters(self):
        try:
            GenericWait().wait_for_true(lambda c: 2 == c, 2)
        except Exception as e:
            self.fail("waitForTrue threw unexpected exception", e)

    # Test wait for with no parameters returns the a timeout exception.
    # @Test(expectedExceptions = TimeoutException.class, groups = TestCategories.UTILITIES)
    def throwTimeoutExceptionWithoutParamTest(self):
        with self.assertRaises(TimeoutError):
            GenericWait().wait_for_true(self.is_param_test)

    # Test wait for with a parameter returns the function exception when the check times out.
    # @Test(expectedExceptions = RuntimeException.class, groups = TestCategories.UTILITIES)
    def throwExceptionWithParamTest(self):
        with self.assertRaises(RuntimeError):
            try:
                GenericWait().wait_for_true(self.throw_error, self.main_test_string)
            except Exception as e:
                raise e.getCause()

    # Test wait for with parameters returns the a timeout exception.
    # @Test(expectedExceptions = TimeoutException.class, groups = TestCategories.UTILITIES)
    def throwTimeoutExceptionWithParamTest(self):
        with self.assertRaises(TimeoutError):
            GenericWait().wait_for_true(self.is_two_parameters, ([]))

    # Test wait without parameters returns function exception.
    # @Test(expectedExceptions = UnsupportedOperationException.class, groups = TestCategories.UTILITIES)
    def test_throwExceptionWithoutParamWithCustomTimesTest(self):
        with self.assertRaises(IOError):
            try:
                GenericWait().wait(self.throw_error, self.test_retry, self.test_timeout, True)
            except Exception as e:
                raise e.message()

    # Test wait with parameters returns function exception.
    # @Test(expectedExceptions = RuntimeException.class, groups = TestCategories.UTILITIES)
    def test_throwExceptionWithParamWithCustomTimesTest(self):
        with self.assertRaises(IOError):
            try:
                GenericWait().wait(self.throw_error, self.test_retry, self.test_timeout, True, "Anything")
            except Exception as e:
                raise e.getCause()

    # Verify custom timeout without parameters works.
    # @Test(groups = TestCategories.UTILITIES)
    def test_customTimeoutWithoutParamTest(self):
        try:
            max_time = int(self.test_timeout) + int(self.test_retry) + int(self.test_retry)
            start = datetime.now()
            GenericWait().wait(self.is_param_test, self.test_retry, self.test_timeout, False)
            duration = datetime.now() - start
            self.assertTrue(duration < datetime.fromtimestamp(max_time),
                            "The max wait time should be no more than " + max_time + " but was " + duration)
        except Exception as e:
            self.fail("wait threw unexpected exception", e)

    # Verify custom timeout with parameters works.
    # @Test(groups = TestCategories.UTILITIES)
    def test_customTimeoutWithParamTest(self):
        try:
            max_time = timedelta(self.test_timeout) + timedelta(self.test_retry) + timedelta(self.test_retry)
            start = datetime.now()
            GenericWait().wait(self.is_param_test, self.test_retry, self.test_timeout, False, "bad")
            duration = datetime.now() - timedelta(start)
            self.assertTrue(duration < max_time,
                            "The max wait time should be no more than " + max_time + " but was " + duration)
        except TimeoutError as e:
            self.fail("wait threw unexpected exception: " + e.message)

    # Verify that Wait with input parameter throws expected exception.
    # @Test(expectedExceptions = TimeoutException.class, groups = TestCategories.UTILITIES)
    def test_waitForFunctionWithInputExceptionThrown(self):
        GenericWait().wait(self.throw_error, self.test_retry, self.test_timeout, "input")

    # Verify that WaitFor returns the correct value of its called function.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitForTest(self):
        try:
            self.assertFalse(GenericWait().wait_for(self.is_param_test()))
        except Exception as e:
            self.fail("waitFor threw unexpected exception", e)

    # Verify that Wait without input parameter throws expected exception.
    # @Test(expectedExceptions = TimeoutException.class, groups = TestCategories.UTILITIES)
    def test_waitForFunctionWithoutInputExceptionThrown(self):
        GenericWait().wait(self.throw_error, self.test_retry, self.test_timeout)

    # Verify waitUntilMatch returns as expected.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitUntilMatchNeverMatch(self):
        # TODO: make sure test is set up properly
        try:
            loop = ["aa"]
            loop.insert(0 , "")
            loop.insert(0, "bb")
            # self.assertEquals(GenericWait().wait_until_match((lambda x: loop.insert(0, "") and loop.insert(0, "bb")), "aa"))
            self.assertEquals(GenericWait().wait_until_match((lambda x: loop.insert(0, "") and loop.insert(0, "bb")), "aa"))
        except InterruptedError as e:
            self.fail("waitUntil threw unexpected exception", e)

    # Verify waitUntilMatch returns as expected.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitUntilMatch(self):
        try:
            loop = [""]
            self.assertEquals(
                GenericWait().wait_until_match((lambda x: loop.insert(0, "a"), loop.insert(0, "aaa")), "aaa"))
        except InterruptedError as e:
            self.fail("waitUntil threw unexpected exception", e)

    # Verify waitUntilMatch with timeout returns as expected.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitUntilMatchTimeout(self):
        try:
            loop = ["aa"]
            self.assertEquals(
                GenericWait().wait_until_match(lambda x: loop.insert(0, ""), "bb", self.test_retry, self.test_timeout),
                "aa")
        except InterruptedError as e:
            self.fail("waitUntil threw unexpected exception", e)

    # Verify waitForMatch with passes as expected.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitForMatchPass(self):
        try:
            loop = [""]
            GenericWait().wait_for_match(lambda x: loop.insert(0, "a"), "aaa")
        except Exception as e:
            self.fail("waitFor threw unexpected exception", e)

    # Verify waitForMatch throws timeout exception.
    # @Test(expectedExceptions = TimeoutException.class, groups = TestCategories.UTILITIES)
    @staticmethod
    def test_waitForMatchTimeoutException(self):
        with self.assertRaises(TimeoutError):
            loop = ["a"]
            GenericWait().wait_for_match(lambda x: loop.insert(0, "a"), "bb")

    # Verify waitForMatch with time retry.
    # @Test(groups = TestCategories.UTILITIES)
    def test_waitForMatchDefinedRetryPass(self):
        try:
            test_loop = [""]
            GenericWait().wait_for_match(lambda x: test_loop.insert(0, "a"), "aaa", self.test_retry, self.test_timeout)
        except Exception as e:
            self.fail("waitFor threw unexpected exception", e)

    # Verify waitForMatch with time retry and time overridden throws timeout exception.
    # @Test(expectedExceptions = TimeoutException.class, groups = TestCategories.UTILITIES)
    def test_waitForMatchDefinedRetryTimeout(self):
        with self.assertRaises(TimeoutError):
            test_loop = ["a"]
            GenericWait().wait_for_match(lambda x: test_loop.insert(0, "a"), "bb", self.test_retry, self.test_timeout)

    # Test function that always returns false.
    # @return Always returns false
    @staticmethod
    def is_param_test():
        return False

    # Test function that checks if the test string passed in is the same as the constant test string.
    # @param testString The test string
    # @return True if the constant and passed in test strings match
    def is_param_test_String(self, input_test_string):
        return input_test_string == self.main_test_string + str(self.number + 1)

    # Test function that checks if the object array passed in is in the form expected.
    # @param parameters Object array
    # @return True if the array is in the form expected
    @staticmethod
    def is_two_parameters(parameters):
        return parameters.__sizeof__() == 2 and isinstance(parameters[0], str) and isinstance(parameters[1], dict)

    # Test function that always throws a runtime exception or not implemented exception error
    # @param testString Test string
    # @return Always throws an exception
    @staticmethod
    def throw_error(test_string=None):
        if test_string is None:
            # UnsupportedOperationException()
            raise IOError()
        else:
            raise RuntimeError()
