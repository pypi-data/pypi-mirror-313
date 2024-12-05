from base import BasePluginTestCase


class TestPlugin(BasePluginTestCase):
    def test_device_classes_available(self):
        device_classes = self.plugin.get_device_classes()

        self.assertEqual(len(device_classes), 2)
        self.assertIn("insta360_x3", device_classes)
        self.assertIn("insta360_x4", device_classes)
