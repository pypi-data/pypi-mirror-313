from devices.base import Device
from base import BasePluginTestCase
from whitebox_plugin_device_insta360.whitebox_plugin_device_insta360 import (
    Insta360X3,
    Insta360X4,
)


class BaseInsta360TestCase(BasePluginTestCase):
    @property
    def device_class(self) -> type[Device]:
        raise NotImplementedError

    def test_get_connection_types(self):
        connection_types = self.device_class.get_connection_types()

        self.assertEqual(
            connection_types,
            {
                "wifi": {
                    "name": "Wi-Fi",
                    "fields": {
                        "ssid": {
                            "name": "Network Name",
                            "type": "text",
                            "required": True,
                        },
                        "password": {
                            "name": "Network Password",
                            "type": "password",
                            "required": True,
                        },
                    },
                },
            },
        )

    def test_check_connectivity(self):
        device_instance = self.device_class(None, None)
        self.assertTrue(device_instance.check_connectivity())


class TestInsta360X3(BaseInsta360TestCase):
    device_class = Insta360X3


class TestInsta360X4(BaseInsta360TestCase):
    device_class = Insta360X4
