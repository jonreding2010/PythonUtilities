import unittest
from utilities.Config import Config
from utilities.constants.ConfigSection import ConfigSection


class ConfigUnitTest(unittest.TestCase):
    # Test getting an entire section from the config.
    # @Test(groups = TestCategories.UTILITIES)
    def test_getSectionWithConfigSecEnumTest(self):
        config = Config()
        test_section = config.get_section(str(ConfigSection.SeleniumMaqs.value))
        self.assertEquals(test_section.get("TestKey"), "testValueTwo")
        self.assertEquals(test_section.get("Browser"), "Internet Explorer")

    # Test adding a list of test settings to the config.
    # @Test(groups = TestCategories.UTILITIES)
    def test_addTestSettingValuesNewSectionTest(self):
        new_value_map = {"BROWSER1": "CHROME1", "DBString2": "Dbstring2222"}
        config = Config()
        config.add_test_setting_values(new_value_map, "NewSection", False)
        test_section = config.get_section("NewSection")
        self.assertEquals(test_section.get("BROWSER1"), "CHROME1")
        self.assertEquals(test_section.get("DBString2"), "Dbstring2222")

    # Test overriding existing values in the config.
    # @Test(groups = TestCategories.UTILITIES)
    def test_addGeneralTestSettingValuesOverrideValuesTest(self):
        new_value_map = {"BrowserOverride": "CHROME", "TimeoutOverride": "13333333"}
        config = Config()
        config.add_general_test_setting_values(new_value_map, True)
        self.assertEquals(config.get_general_value("BrowserOverride"), "CHROME")
        self.assertEquals(config.get_general_value("TimeoutOverride"), "13333333")

    # Test not overriding existing values in the config.
    # @Test(groups = TestCategories.UTILITIES)
    def test_addGeneralTestSettingValuesDoNotOverrideValuesTest(self):
        new_value_map = {"DontBrowserOverride": "CHROME", "DontTimeoutOverride": "13333333"}
        new_value_map_two = {"DontBrowserOverride": "IE", "DontTimeoutOverride": "5555"}

        # add values to the override config since the values don't exist in the override config
        config = Config()
        config.add_general_test_setting_values(new_value_map, False)
        self.assertEquals(config.get_general_value("DontBrowserOverride"), "CHROME")
        self.assertEquals(config.get_general_value("DontTimeoutOverride"), "13333333")

        # don't add the values to the override config since the values do exist in the override config
        config.add_general_test_setting_values(new_value_map_two, False)
        self.assertEquals(config.get_general_value("DontBrowserOverride"), "CHROME")
        self.assertEquals(config.get_general_value("DontTimeoutOverride"), "13333333")

        # do add the values because of the override flag
        config.add_general_test_setting_values(new_value_map_two, True)
        self.assertEquals(config.get_general_value("DontBrowserOverride"), "IE")
        self.assertEquals(config.get_general_value("DontTimeoutOverride"), "5555")

    # Test getting a value out of the default section of the config.
    # @Test(groups = TestCategories.UTILITIES)
    def test_getGeneralValueTest(self):
        config = Config()
        self.assertEquals(config.get_general_value("TestKey"), "testValue")
        self.assertEquals(config.get_general_value("nonExistentKey", "defaultValue"), "defaultValue")

    # Test getting a value of a specified section of the config.
    # @Test(groups = TestCategories.UTILITIES)
    def test_getValueForSectionTest(self):
        config = Config()
        self.assertEquals(config.get_value_for_section("SeleniumMaqs", "TestKey"), "testValueTwo")
        self.assertEquals(config.get_value_for_section(ConfigSection.SeleniumMaqs.value, "Browser"), "Internet Explorer")
        self.assertEquals(config.get_value_for_section("SeleniumMaqs", "nonExistentKey", "defaultValue"), "defaultValue")

    # Test getting a value from the config using the full defined path.
    # @Test(groups = TestCategories.UTILITIES)
    def test_getValueTest(self):
        config = Config()
        self.assertEquals(config.get_value("MagenicMaqs.TestKey", "defaultValue"), "defaultValue")
        self.assertEquals(config.get_value("SeleniumMaqs.TestKey"), "testValueTwo")

    # Test checking if the key exists.
    # @Test(groups = TestCategories.UTILITIES)
    def test_doesKeyExistTest(self):
        config = Config()
        self.assertTrue(config.does_key_exist("SeleniumMaqs.TestKey"))
        self.assertTrue(config.does_general_key_exist("TimeoutOverride"))
        self.assertTrue(config.does_key_exist("HubAddress", ConfigSection.SeleniumMaqs.value))
        self.assertFalse(config.does_key_exist("HubAddress", ConfigSection.MagenicMaqs.value))
