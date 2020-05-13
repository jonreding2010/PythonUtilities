import pathlib
from os import path
from utilities.constants.ConfigSection import ConfigSection
from utilities.StringProcessor import StringProcessor
from utilities.MaqsConfigException import MaqsConfigException
import xml.etree.ElementTree as ElementTree


# Configuration class.
class Config:
    def __init__(self):
        # The default section MagenicMaqs.
        self.default_maqs_section = ConfigSection.MagenicMaqs
        # The configuration containing values loaded in from the config.xml file.
        self.config_values = self.get_file()
        # The configuration containing values that were added to the configuration.
        self.override_config = dict()
        # The base configs object.
        self.configs = dict()

    # reads the config file and reads its values
    def get_file(self):
        # default config.xml file name.
        config_file = pathlib.Path(__file__).with_name("config.xml")

        try:
            if path.exists(config_file):
                tree = ElementTree.parse(config_file)
                root = tree.getroot()

                new_config_values = {}

                for parent in root:
                    new_config_values[parent.tag] = {}
                    for child in parent:
                        new_config_values[parent.tag][child.tag] = child.text
                return new_config_values
        except Exception as e:
            raise TimeoutError(StringProcessor.safe_formatter(
                "Exception creating the xml configuration object from the file : " + e.args))
   
    # Validates the app config section by ensuring required values are present
    # @param configSection The config section to be validated
    # @param configValidation A list of strings containing the requried field names
    def validate(self, config_section, config_validation):
        if config_validation is None:
            raise MaqsConfigException("The value passed in for config_validation"
                                      " (required fields in a config) is null")
        #config_section_passed = Config.get_section(self, config_section)
        config_section_passed = self.get_section(config_section)

        exceptions = []
        for requiredField in config_validation.RequiredFields:
            if requiredField not in config_section_passed:
                exceptions.append("Key missing " + requiredField)
        if exceptions.__sizeof__() > 0:
            message = []
            for mess in exceptions:
                message.append(mess)
            raise MaqsConfigException(message)
                
    # Gets a specific section from the configuration.
    # @param section The desired section
    # @return A dictionary of the values in the section
    def get_section(self, section):
        section_values = {}
        # first parse the override config
        override_paths = self.override_config.get(section)

        if override_paths is not None:
            for key in override_paths:
                key = key.__str__()
                edited_key = key.replace(section + ".", "")
                section_values[edited_key] = override_paths.get(key)

        # then parse the base config, ignoring duplicates
        config_value_paths = self.config_values.get(section)

        if config_value_paths is not None:
            for key in config_value_paths:
                key = key.__str__()
                edited_key = key.replace(section + ".", "")

                if edited_key not in section_values:
                    section_values[edited_key] = config_value_paths.get(key)
        return section_values

    # Add dictionary of values to maqs section.
    # @param configurations   Dictionary of configuration values
    # @param overrideExisting True to override existing values, False otherwise
    def add_general_test_setting_values(self, configurations, override_existing):
        self.add_test_setting_values(configurations, self.default_maqs_section.value, override_existing)

    # Add dictionary of values to specified section.
    # @param configurations   Dictionary of configuration values
    # @param section          Section to add the value to
    # @param overrideExisting True to override existing values, False otherwise
    def add_test_setting_values(self, configurations, section, override_existing):
        for key, value in configurations.items():
            # Make sure the section exists
            if self.look_for_section(section, self.override_config) is None:
                self.override_config = {section: {}}

            # See if we need to add a new key value pair
            if self.contains_key(key, self.override_config) is False:
                self.override_config[section][key] = value
            elif override_existing:
                # We want to override existing values
                self.override_config[section][key] = value

    # Get the specified value out of the default section.
    # @param key          The key
    # @param defaultValue The value to return if the key does not exist
    # @return The configuration value
    def get_general_value(self, key, default_value=None):
        if default_value is None:
            return self.get_value_for_section(self.default_maqs_section.value.__str__(), key)
        else:
            return self.get_value_for_section(self.default_maqs_section.value.__str__(), key, default_value)

    # Get the specified value out of the specified section.
    # @param section      The section to search
    # @param key          The key
    # @param defaultValue The value to return if the key is not found
    # @return The configuration value
    def get_value_for_section(self, section, key, default_value=None):
        key_with_section = section + "." + key
        return self.get_value(key_with_section, default_value)

    @staticmethod
    def get_key(key, dictionary):
        if dictionary is not None or dictionary > 0:
            for section in dictionary:
                if section in key:
                    for value in dictionary[section]:
                        key = key[key.find(".") + 1:len(key)]
                        if value == key:
                            return dictionary[section][value]
        return None

    @staticmethod
    def contains_section(section, dictionary):
        if dictionary is not None or dictionary > 0:
            for sections in dictionary:
                if section in sections:
                    return True
        return False

    @staticmethod
    def contains_key(key, dictionary):
        if dictionary is not None or dictionary > 0:
            for section in dictionary:
                for value in dictionary[section]:
                    if value == key:
                        return True
        return False

    @staticmethod
    def look_for_section(section, dictionary):
        if len(dictionary) > 0:
            for sections in dictionary:
                if section in sections:
                    return section
        return None

    def check_configs_for_key(self, key):
        ret_val = self.get_key(key, self.override_config)
        if ret_val is None:
            return self.get_key(key, self.config_values)
        else:
            return ret_val

    # Get the configuration value for a specific key. Does not assume a section.
    # @param key The key
    # @param defaultValue Value to return if the key does not exist
    # @return The configuration value - Returns the default string if the key is not found
    def get_value(self, key, default_value=None):
        ret_val = self.check_configs_for_key(key)
        if default_value is not None and ret_val != default_value:
            return default_value
        else:
            return ret_val

    # Check the config for a specific key. Searches the specified section.
    # @param key     The key
    # @param section The specified section
    # @return True if the key exists, false otherwise
    def does_key_exist(self, key, section=None):
        if section is not None:
            if section in self.override_config:
                if key in self.override_config[section]:
                    return True
                else:
                    return False
            else:
                return key in self.config_values[section]
        else:
            if self.override_config is not None and len(self.override_config) > 0:
                return key in self.override_config
            else:
                if self.get_key(key, self.config_values):
                    return True
                return False

        # Check the config for a specific key. Searches the default section.
    # @param key The key
    # @return True if the key exists, false otherwise
    def does_general_key_exist(self, key):
        return self.does_key_exist(key, self.default_maqs_section.value)
