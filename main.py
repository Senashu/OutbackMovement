import keyboard
import vgamepad as vg
import pymem
from pymem.process import module_from_name
import json

gamepad = vg.VDS4Gamepad()
mem = pymem.Pymem("Ty.exe")


def get_current_level():
    module = module_from_name(mem.process_handle, "Ty.exe").lpBaseOfDll
    return mem.read_int(module + 0x280594)


def ActionButton():
    if keyboard.is_pressed(Action):
        gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
        gamepad.update()
        print("Pressed Action Button")
    else:
        gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)


# def SelectButton():
#    if keyboard.is_pressed(Select):
#        gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE)
#        gamepad.update()
#        print("Pressed Select Button")
#    else:
#        gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE)


def OutbackMovement(CurrentLevel):
    y_value_float = 0.0

    if CurrentLevel == 10:
        if keyboard.is_pressed(Movement):
            y_value_float -= 1.0
            print("Outback Movement active")
        else:
            y_value_float = 0.0

        gamepad.left_joystick_float(x_value_float=0, y_value_float=y_value_float)
        gamepad.update()
    else:
        y_value_float = 0.0
        gamepad.left_joystick_float(x_value_float=0, y_value_float=y_value_float)
        gamepad.update()


# Load settings from settings.json
with open("settings.json", "r") as f:
    settings = json.load(f)
    Movement = settings["Movement"]
    Action = settings["Action"]
    Select = settings["Select"]
while True:
    CurrentLevel = get_current_level()
    ActionButton()
    OutbackMovement(CurrentLevel)
    # SelectButton()
