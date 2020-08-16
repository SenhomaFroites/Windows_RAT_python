# -*- coding: utf-8 -*-

def translate(original):
    """ text """

    keys_dict = {
        "Key.esc": "[Esc]",
        "Key.f1": "[F1]",
        "Key.f2": "[F2]",
        "Key.f3": "[F3]",
        "Key.f4": "[F4]",
        "Key.f5": "[F5]",
        "Key.f6": "[F6]",
        "Key.f7": "[F7]",
        "Key.f8": "[F8]",
        "Key.f9": "[F9]",
        "Key.f10": "[F10]",
        "Key.f11": "[F11]",
        "Key.f12": "[F12]",
        "Key.insert": "[Insert]",
        "Key.delete": "[Del]",
        "Key.backspace": "[Backspace]",
        "Key.tab": "[Tab]",
        "Key.enter": "[Enter]",
        "Key.caps_lock": "[CapsLock]",
        "\\": "\"",
        "Key.shift": "[Left Shift]",
        "Key.shift_r": "[Right Shift]",
        "Key.ctrl_l": "[Left Ctrl]",
        "Key.cmd": "[Win]",
        "Key.alt_l": "[Left Alt]",
        "Key.space": "[Space]",
        "Key.alt_r": "[Right Alt]",
        "Key.ctrl_r": "[Right Ctrl]",
        "Key.left": "[Left]",
        "Key.up": "[Up]",
        "Key.down": "[Down]",
        "Key.right": "[Right]",
        "Key.home": "[Home]",
        "Key.page_up": "[Page Up]",
        "Key.page_down": "[Page Down]",
        "Key.end": "[End]",
        "Key.media_volume_mute": "[Vol Mute]",
        "Key.media_volume_down": "[VOL-]",
        "Key.media_volume_up": "[VOL+]",
        }

    for key, value in keys_dict.items():
        if str(original) == key:
            return value