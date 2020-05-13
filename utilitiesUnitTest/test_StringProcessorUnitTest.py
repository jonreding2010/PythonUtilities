import unittest
from utilities.StringProcessor import StringProcessor


class StringProcessorUnitTest(unittest.TestCase):
    def test_SafeFormatter(self):
        successful = StringProcessor.safe_formatter("This is a {} message.", "successful")
        self.assertEqual(successful, "This is a successful message.")

    def test_SafeFormatterMessage(self):
        successful = StringProcessor.safe_formatter("This is a message.")
        self.assertEqual(successful, "This is a message.")

    def test_SafeFormatterMessageNull(self):
        string = StringProcessor.safe_formatter(None, ["Message", "String", None])
        self.assertEqual(string, "Message: None Arguments: Message String None")

    # Test method for checking JSON strings
    def test_StringFormatterCheckForJson(self):
        string = StringProcessor.safe_formatter("{This is a test for JSON}")
        self.assertEqual("{This is a test for JSON}", string)

    #  Test method for checking string format
    def test_StringFormatterCheckForStringFormat(self):
        message = StringProcessor.safe_formatter('This {} should return {}', ["Test", "Test"])
        self.assertEqual("This Test should return Test", message)

    # Single exception to validate string data
    def test_SingleExceptionSafeFormatter(self):
        format_exception = SyntaxError("Format Exception")
        formatted_exception = StringProcessor.safe_exception_formatter(format_exception)
        self.assertTrue("Format Exception" in formatted_exception)

    # the stack trace is formatted and included in the string
    def test_ThrowSingleExceptionSafeFormatter(self):
        try:
            raise SyntaxError("Format Exception")
        except SyntaxError as e:
            formatted_exception = StringProcessor.safe_exception_formatter(e)
            self.assertTrue("Format Exception" in formatted_exception)
            self.assertTrue("utilitiesUnitTest\\test_StringProcessorUnitTest.py" in formatted_exception)
            self.assertTrue("in test_ThrowSingleExceptionSafeFormatter" in formatted_exception)
