from django.test import TestCase

from plugin.manager import plugin_manager


class BasePluginTestCase(TestCase):
    def setUp(self) -> None:
        self.plugin = [
            x
            for x in plugin_manager.plugins
            if x.__class__.__name__ == "WhiteboxPluginDeviceInsta360"
        ][0]
        return super().setUp()
