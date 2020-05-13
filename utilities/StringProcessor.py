import os
import traceback
import sys


class StringProcessor:
    # Creates a string based on the arguments. If no args are applied, then we want to just return the message
    # @param message The message being used
    # @param args    The arguments being used
    # @return A final string
    @staticmethod
    def safe_formatter(message, args=None):
        if args is None:
            return message
        try:
            if isinstance(args, str):
                return message.format(args)
            else:
                return message.format(*args)
        except Exception:
            builder = "Message: " + str(message)
            builder += " Arguments: "

            for arg in args:
                builder += str(arg) + " "
        return builder.rstrip()

    # Gets a string of a nested exception list
    # @param e Exception to print as string</param>
    # return A string of the Exceptions with stack trace</returns>
    @staticmethod
    def safe_exception_formatter(exception):
        sb = ""
        return StringProcessor.get_exception(exception, sb)

    # Recursive function to grab the inner exceptions
    # @param ex Exception to look into</param>
    # @param sb String builder to build the string</param>
    # @param level Recursive level for spacing of logs</param>
    # return A string with the exceptions</returns>
    @staticmethod
    def get_exception(exception, sb, level=0):
        # if str(traceback.format_stack()) is not None:
        #   sb.append(os.linesep + spaces + exception.msg + str(traceback.format_stack()))
        exc_type, exc_value, exc_tb = sys.exc_info()
        tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
        formatted = ''.join(tbe.format())
        trace = traceback.format_exc(2)
        sb = os.linesep + exception.msg + os.linesep + traceback.format_exc()

        if exception is Exception:
            # if (ex is Exception and (ex as AggregateException).InnerExceptions.Count > 0):
            for nested_exception in exception:
                # for exception in (ex as AggregateException).InnerExceptions):
                StringProcessor.get_exception(nested_exception, sb, level + 1)
        elif len(exception.args) is 0:
            StringProcessor.get_exception(exception.InnerException, sb, level + 2)
        return sb
