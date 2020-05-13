# Definition of exceptions which will be thrown when there is a problem with loading elements of the MAQS app.config
class MaqsConfigException(Exception):
    # MAQS config exception
    # @param message Takes an exception message
    def maqs_config_exception(self, message):
        super(message)
