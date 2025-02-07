import pydualsense as ds
import matplotlib.pyplot as plt
import numpy as np
import time



def trigger():
    controller= ds.pydualsense()
    controller.init()


    # trigger official mode 1
    controller.triggerL.setMode(ds.TriggerModes.Rigid)
    print("official mode 1")
    for i in range(10, -1, -1):
        print(f"\rCountdown: {i}", end='', flush=True)
        time.sleep(1)
    print()  # To move to the next line after the countdown
    controller.triggerL.setMode(ds.TriggerModes.Off)

    


    controller.close()

    pass



def plot_setting():
    # Define zones (0 to 255)
    zones = np.arange(256)

    # Scenario 1: Slope Feedback (e.g. drawing a bow)
    # Force is zero until zone 51, then increases linearly from 51 to 204 (zones 51 to 204),
    # and remains at 255 for zones 205 to 255.
    slope_force = np.zeros(256)
    for i in range(256):
        if i < 51:
            slope_force[i] = 0
        elif i <= 204:
            # Linear interpolation from 51 to 255 between zone 51 and 204
            slope_force[i] = round(51 + (255 - 51) * (i - 51) / (204 - 51))
        else:
            slope_force[i] = 255

    # Scenario 2: Weapon Effect (e.g. gun trigger snap)
    # Here we simulate a step: no effect until zone 76, then full force (255) from zones 76 to 153, then off.
    weapon_force = np.zeros(256)
    for i in range(256):
        if 76 <= i <= 153:
            weapon_force[i] = 255  # maximum resistance for a crisp snap
        else:
            weapon_force[i] = 0

    # Scenario 3: Constant Feedback (e.g. brake or lock)
    # Force is zero until zone 102, then a constant moderate force (128) is applied.
    feedback_force = np.zeros(256)
    for i in range(256):
        if i >= 102:
            feedback_force[i] = 128
        else:
            feedback_force[i] = 0

    # Scenario 4: Custom Multi-Zone Feedback
    # A custom force curve defined explicitly for each zone.
    custom_force = np.array([0, 32, 64, 128, 192, 255, 192, 128, 64, 32, 0])
    custom_force = np.interp(zones, np.linspace(0, 255, len(custom_force)), custom_force)

    # Plot all scenarios in a 2x2 grid
    plt.figure(figsize=(12, 8))

    # Slope Feedback Plot
    plt.subplot(2, 2, 1)
    plt.plot(zones, slope_force, marker='o', linestyle='-', color='blue')
    plt.title("Slope Feedback (Bow Draw)")
    plt.xlabel("Trigger Zone")
    plt.ylabel("Force Strength")
    plt.ylim(-10, 265)
    plt.grid(True)

    # Weapon Effect Plot
    plt.subplot(2, 2, 2)
    plt.plot(zones, weapon_force, marker='s', linestyle='-', color='red')
    plt.title("Weapon Effect (Gun Trigger)")
    plt.xlabel("Trigger Zone")
    plt.ylabel("Force Strength")
    plt.ylim(-10, 265)
    plt.grid(True)

    # Constant Feedback Plot
    plt.subplot(2, 2, 3)
    plt.plot(zones, feedback_force, marker='d', linestyle='-', color='green')
    plt.title("Constant Feedback (Brake/Lock)")
    plt.xlabel("Trigger Zone")
    plt.ylabel("Force Strength")
    plt.ylim(-10, 265)
    plt.grid(True)

    # Custom Multi-Zone Feedback Plot
    plt.subplot(2, 2, 4)
    plt.plot(zones, custom_force, marker='^', linestyle='-', color='purple')
    plt.title("Custom Multi-Zone Feedback")
    plt.xlabel("Trigger Zone")
    plt.ylabel("Force Strength")
    plt.ylim(-10, 265)
    plt.grid(True)

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    trigger()

    pass