from plugin.utils import Plugin
from whitebox_plugin_device_insta360.devices import (
    Insta360X3,
    Insta360X4,
)


class WhiteboxPluginDeviceInsta360(Plugin):
    """
    A plugin that enables support for Insta360 cameras.

    Attributes:
        name: The name of the plugin.
    """

    name = "Insta360 Camera Support"
    device_classes = [Insta360X3, Insta360X4]


plugin_class = WhiteboxPluginDeviceInsta360
