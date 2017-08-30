from aureus.login import (
    mmc_credentials_factory,
    resource_credentials_factory
)


def configure_setting(settings, prop, value):
    if prop not in settings:
        settings[prop] = value


def configure(settings=None):
    if not settings:
        settings = {}
    configure_setting(settings, 'mmc.credentials', mmc_credentials_factory())
    configure_setting(settings, 'mmc.root.url', 'https://jssapps01.johnnyseeds.com:8443/mmc-console-3.8.0-HF1/api/')
    configure_setting(settings, 'nexus.root.url', 'https://jssnexus.eastus.cloudapp.azure.com:8443/repository/nexus-releases/')
    configure_setting(settings, 'nexus.credentials', resource_credentials_factory())
    return settings

