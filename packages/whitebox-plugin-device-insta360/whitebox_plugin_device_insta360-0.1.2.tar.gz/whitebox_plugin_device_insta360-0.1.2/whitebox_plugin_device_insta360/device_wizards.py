from django.templatetags.static import static

from devices.base import DeviceWizard
from utils.data_transformation import URLString


def generate_info_step(
    step_indicator,
    title,
    description,
    media_url,
    media_type,
    next_button_text,
):
    elements = [
        {
            "type": media_type,
            "config": {
                "url": URLString(static(media_url)),
                "classes": "wizard-media-container",
            },
        },
        {
            "type": "text",
            "config": {
                "text": step_indicator,
                "style": {
                    "color": "high-emphasis",
                    "size": "lg",
                    "font_weight": "semibold",
                },
            },
        },
        {
            "type": "text",
            "config": {
                "text": title,
                "style": {
                    "size": "2xl",
                    "font_weight": "semibold",
                },
            },
        },
        {
            "type": "text",
            "config": {
                "text": description,
                "style": {
                    "color": "high-emphasis",
                    "font_weight": "medium",
                    "font_height": "6",
                },
            },
        },
    ]

    actions = {
        "left": {
            "type": "button",
            "config": {
                "text": "Skip to end",
                "action": "WIZARD_STEP_LAST",
            },
        },
        "right": {
            "type": "button",
            "config": {
                "text": next_button_text,
                "action": "WIZARD_STEP_NEXT",
            },
        },
    }

    return {
        "elements": elements,
        "actions": actions,
    }


introduction = generate_info_step(
    "Introduction",
    "{model_name} setup guide",
    (
        "Welcome to the {model_name} setup guide! "
        "Follow these simple steps to get your camera ready for action. "
        "Let’s get started!"
    ),
    "{introduction_step_picture}",
    "image",
    "Start",
)

step_1 = generate_info_step(
    "Step 1 of 4",
    "MicroSD: Insert",
    (
        "Before you begin recording, make sure to insert a compatible MicroSD "
        "card into your {model_name}. To insert the card, open the side "
        "compartment on the camera, remove the battery and gently push the "
        "MicroSD card into the slot until it clicks into place, and close the "
        "compartment securely."
    ),
    "whitebox_plugin_device_insta360/insta360_x4/wizard_step_1.mp4",
    "video",
    "Checked",
)

step_2 = generate_info_step(
    "Step 2 of 4",
    "Camera: Charge",
    (
        "Before heading out to shoot, check that your {model_name} is fully "
        "charged. Use the provided USB cable to connect the camera to a power "
        "source. The camera’s LED indicator will turn off when the battery is "
        "fully charged. It’s a good idea to keep a spare battery or portable "
        "charger handy for longer sessions."
    ),
    "whitebox_plugin_device_insta360/insta360_x4/wizard_step_2.mp4",
    "video",
    "Checked",
)

step_3 = generate_info_step(
    "Step 3 of 4",
    "Camera: Activate",
    (
        "To activate your camera, power it on and enable Wi-Fi. Download the "
        "Insta360 app from the App Store or Google Play, then follow the app’s "
        "prompts to connect to your camera’s Wi-Fi and complete the pairing "
        "process. The app will also guide you through any necessary firmware "
        "updates."
    ),
    "whitebox_plugin_device_insta360/insta360_x4/wizard_step_3.mp4",
    "video",
    "Checklist complete",
)

step_4 = {
    "elements": [
        {
            "type": "video",
            "config": {
                "url": static(
                    "whitebox_plugin_device_insta360/insta360_x4/wizard_step_3.mp4",
                ),
                "classes": "wizard-media-container",
            },
        },
        {
            "type": "text",
            "config": {
                "text": "Step 4 of 4",
                "style": {
                    "color": "high-emphasis",
                    "size": "lg",
                    "font_weight": "semibold",
                },
            },
        },
        {
            "type": "text",
            "config": {
                "text": "Wi-Fi: Enter details",
                "style": {
                    "size": "2xl",
                    "font_weight": "semibold",
                },
            },
        },
        {
            "type": "wizard_field_block",
            "config": {},
        },
    ],
    "actions": {
        "left": {
            "type": "button",
            "config": {
                "text": "Back",
                "action": "WIZARD_STEP_INITIAL",
            },
        },
        "right": {
            "type": "button",
            "config": {
                "text": "Connect device",
                "action": "WIZARD_ADD_DEVICE",
            },
        },
    },
}


class BaseInsta360Wizard(DeviceWizard):
    wizard_step_config = [
        introduction,
        step_1,
        step_2,
        step_3,
        step_4,
    ]


class Insta360X3Wizard(BaseInsta360Wizard):
    wizard_step_format_strings = {
        "model_name": "Insta360 X3",
        "introduction_step_picture": (
            "whitebox_plugin_device_insta360/insta360_x3/insta360_x3.webp"
        ),
    }


class Insta360X4Wizard(BaseInsta360Wizard):
    wizard_step_format_strings = {
        "model_name": "Insta360 X4",
        "introduction_step_picture": (
            "whitebox_plugin_device_insta360/insta360_x4/insta360_x4.webp"
        ),
    }
