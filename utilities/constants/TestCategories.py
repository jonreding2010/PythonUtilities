from enum import Enum


class ConfigSection(Enum):
    # Email unit test category.
    EMAIL = "Email Unit Tests"

    # Database unit test category.
    DATABASE = "Database Unit Tests"

    # Selenium unit test category.
    SELENIUM = "Selenium Unit Tests"

    # Utilities unit test category.
    UTILITIES = "Utilities Unit Tests"

    # Web service unit test category.
    WEB_SERVICE = "Web Service Unit Tests"

    # Base framework unit test category.
    FRAMEWORK = "Base Framework Unit Tests"

    # Appium unit test category.
    APPIUM = "Appium Unit Tests"