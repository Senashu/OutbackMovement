import keyboard
import vgamepad as vg
import pymem
from pymem.process import module_from_name
import json
import psutil
import time

gamepad = vg.VDS4Gamepad()


def is_game_running():
    for process in psutil.process_iter(['name']):
        if process.name() == 'Mul-Ty-Player.exe' or process.name() == 'TY.exe':
            return process.name()
    return None


def get_current_level():
    game_name = is_game_running()
    if game_name:
        try:
            mem = pymem.Pymem(game_name)
            module = module_from_name(mem.process_handle, game_name).lpBaseOfDll
            return mem.read_int(module + 0x280594)
        except pymem.exception.ProcessNotFound:
            print("Game process not found. Waiting for it to reopen...")
            while is_game_running() is None:
                time.sleep(5)
            return get_current_level()
    else:
        return None


def ActionButton():
    if keyboard.is_pressed(Action):
        gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
        gamepad.update()
        print("Pressed Action Button")
    else:
        gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)


def OutbackMovement(CurrentLevel):
    y_value_float = 0.0

    if CurrentLevel == 10:
        if keyboard.is_pressed(Movement):
            y_value_float += 1.0
            print("Outback Movement active")
        else:
            y_value_float = 0.0

        gamepad.left_joystick_float(x_value_float=0, y_value_float=y_value_float)
        gamepad.update()
    else:
        y_value_float = 0.0
        gamepad.left_joystick_float(x_value_float=0, y_value_float=y_value_float)
        gamepad.update()


with open("settings.json", "r") as f:
    settings = json.load(f)
    Movement = settings["Movement"]
    Action = settings["Action"]
    Select = settings["Select"]

while True:
    CurrentLevel = get_current_level()
    if CurrentLevel is not None:
        ActionButton()
        OutbackMovement(CurrentLevel)
