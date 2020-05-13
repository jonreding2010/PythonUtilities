import time

from numpy.core import long

from utilities.Config import Config
from datetime import datetime, timedelta


# The type Generic wait.
class GenericWait:
    def __init__(self):
        self.retry_time_from_config = long(Config().get_general_value("WaitTime"))
        self.timeout_from_config = long(Config().get_general_value("Timeout"))

    # Wait until boolean.
    # @param <T>         the type parameter
    # @param waitForTrue the wait for true
    # @param arg         the arg
    # @return the boolean
    # @throws InterruptedException the interrupted exception
    # @throws FunctionException    the function exception
    def wait_until(self, wait_for_true, arg=None):
        if not self.wait_boolean(wait_for_true, self.retry_time_from_config, self.timeout_from_config, arg):
            return self.wait_boolean(wait_for_true, self.retry_time_from_config, self.timeout_from_config, arg)
        else:
            raise TimeoutError("Timed out waiting for the wait_until method to return true")

    # Wait for true.
    # @ param waitForTrue the wait for true
    # @ param arg the arg
    def wait_for_true(self, wait_for_true, arg=None):
        if not self.wait(wait_for_true, self.retry_time_from_config, self.timeout_from_config, True, arg):
            raise TimeoutError("Timed out waiting for the wait_for_true method to return true")

    # Wait until match t.
    # @param waitForTrue      the wait for true
    # @param retryTime        the retry time
    # @param timeout          the timeout
    # @param comparativeValue the comparative value
    # @return the t
    # @throws InterruptedException the interrupted exception
    # def waitUntilMatch(Supplier<T> waitForTrue, long retryTime, long timeout, T comparativeValue):
    def wait_until_match(self, wait_for_true, comparative_value, retry_time=None, timeout=None):
        if retry_time is None:
            retry_time = self.retry_time_from_config
        if timeout is None:
            timeout = self.timeout_from_config

        start_time = datetime.now()
        value = wait_for_true

        # Checks if the two values are equal
        params_are_equal = self.params_equals([value, comparative_value])

        # while the params are not equal and the timout hasn't been met,
        # running them through another function because we can't use an operator with T
        while not params_are_equal and (start_time - datetime.now()) < timeout:
            # If they aren't, wait
            time.sleep(retry_time)
            value = wait_for_true

            # Check if they are equal
            # running them through another function because we can't use an operator with T
            if timeout is self.timeout_from_config and retry_time is self.retry_time_from_config:
                params_are_equal = self.params_equals([value, comparative_value])
            else:
                if self.params_equals([value, comparative_value]):
                    return value
        return value

    # Wait for match.
    # @param <T>              the type parameter
    # @param waitForTrue      the wait for true
    # @param retryTime        the retry time
    # @param timeout          the timeout
    # @param comparativeValue the comparative value
    # @throws InterruptedException the interrupted exception
    # @throws TimeoutException     the timeout exception
    # def waitForMatch(Supplier<T> waitForTrue, long retryTime, long timeout,T comparativeValue):
    def wait_for_match(self, wait_for_true, comparative_value, retry_time=None, timeout=None):
        if retry_time is None:
            retry_time = self.retry_time_from_config
        if timeout is None:
            timeout = self.timeout_from_config

        # Set start time and exception holder
        start_time = datetime.now()
        # Checks if the two values are equal
        params_are_equal = self.params_equals([wait_for_true, comparative_value])

        # While the params are not equal & the timeout hasn't met, keep checking
        while not params_are_equal and (start_time - datetime.now()) < timeout:
            if timeout is self.timeout_from_config and retry_time is self.retry_time_from_config:
                # If they aren't, wait
                time.sleep(retry_time)

            # Check if they are equal running them through another function because we can't use an operator with T
            params_are_equal = self.params_equals([wait_for_true, comparative_value])

            if timeout is not self.timeout_from_config and retry_time is not self.retry_time_from_config:
                # If they aren't, wait
                time.sleep(retry_time)

        if not params_are_equal:
            raise TimeoutError(
                "Timed out waiting for the supplier to return the expected value of " + comparative_value)

    # Wait for t.
    # @param <T>     the type parameter
    # @param waitFor the wait for
    # @return the t
    # def waitFor(Supplier<T> waitFor):
    def wait_for(self, wait_for, arg=None):
        return self.wait(wait_for, self.retry_time_from_config, self.timeout_from_config, arg)

    # Wait boolean.
    # @param waitForTrue    the wait for true
    # @param retryTime      the retry time
    # @param timeout        the timeout
    # @param throwException the throw exception
    # @return the boolean
    # public static boolean wait(BooleanSupplier waitForTrue, long retryTime, long timeout, boolean throwException)
    @staticmethod
    def wait_boolean(wait_for_true, retry_time, timeout, throw_exception, arg=None):
        # Set start time and exception holder
        start_time = datetime.now()
        exception = None

        while int((datetime.now() - start_time).total_seconds()) < timeout:
            try:
                # Clear out old exception
                exception = None
                # Check if the function returns true
                if wait_for_true:
                    return True
            except Exception as e:
                # Save of the exception if we want to throw exceptions
                exception = ValueError("BooleanSupplier exception caught.", e)
                # Give the system a second before checking if the page is updating
            time.sleep(retry_time)
        # Check if we had an exceptions
        if throw_exception and exception is not None:
            raise exception
            # We timed out waiting for the function to return true
        return False

    # Wait t.
    # @param <T>       the type parameter
    # @param <U>       the type parameter
    # @param waitFor   the wait for two parameter
    # @param retryTime the retry time
    # @param timeout   the timeout
    # @param arg       the arg
    # @return the t
    # def wait(self, Function<U, T> waitFor, long retryTime, long timeout, U arg):
    @staticmethod
    def wait(wait_for_true, retry_time, timeout, arg=None):
        # Set start time and exception holder
        start_time = datetime.now()
        exception = None
        while int((datetime.now() - start_time).total_seconds()) < timeout:
            try:
                if arg is None:
                    return wait_for_true.append(arg)

                value = wait_for_true

                if value is not None:
                    return value
            except Exception as e:
                exception = e
                # Give the system a second before checking if the page is updating
            time.sleep(retry_time)
        raise TimeoutError("Timed out waiting for the wait method to return" + exception)

    @staticmethod
    def params_equals(param):
        # For each item
        for item in param:
            # and each item
            for item2 in param:
                # Compare each item
                if not item.equals(item2):
                    # If any do not match, then they are not equal
                    return False
        # If we get here, then we had no mismatches
        return True
