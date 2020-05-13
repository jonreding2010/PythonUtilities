from enum import Enum


class ConfigSection(Enum):
    # The default magenic maqs section.
    MagenicMaqs = "MagenicMaqs"

    # The default appium maqs section.
    AppiumMaqs = "AppiumMaqs"

    # The default appium capabilities section.
    AppiumCapsMaqs = "AppiumCapsMaqs"

    # The default database maqs section.
    DatabaseMaqs = "DatabaseMaqs"

    # Database Caps Section.
    DatabaseCapsMaqs = "DatabaseCapsMaqs"

    # The default email maqs section.
    EmailMaqs = "EmailMaqs"

    # The default selenium maqs section.
    SeleniumMaqs = "SeleniumMaqs"

    # The default remote selenium capabilities section.
    RemoteSeleniumCapsMaqs = "RemoteSeleniumCapsMaqs"

    # The default web service section.
    WebServiceMaqs = "WebServiceMaqs"
