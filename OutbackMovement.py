import keyboard
import vgamepad as vg

gamepad = vg.VDS4Gamepad()

button_states = {
    "0": False, #stop overall
    "ctrl": False, # dpad up
}

while True:
    for key in button_states:
        if keyboard.is_pressed(key):
            button_states[key] = True
        else:
            button_states[key] = False

    if button_states["0"]:
        break

    x_value_float = 0.0
    y_value_float = 0.0

    if button_states["ctrl"]:
        y_value_float += 1.0
        print("Outback Movement: ON")
    else:
        print("Outback Movement: OFF")

    gamepad.left_joystick_float(x_value_float=x_value_float, y_value_float=y_value_float)
    gamepad.update()
