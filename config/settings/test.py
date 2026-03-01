from config.environment import Environment
from config.environs.test import EnvironSettingsTest

Environment._ENVIRON_SETTING = EnvironSettingsTest
Environment.get_environment_settings()
from config.settings.dev import *
