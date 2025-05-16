from __future__ import print_function  # WalabotAPI works on both Python 2 an 3.
from sys import platform
from os import system
from imp import load_source
import matplotlib.pyplot as plt
import numpy as np
from os.path import join
import time

if platform == "win32":
    modulePath = join(
        "C:/", "Program Files", "Walabot", "WalabotSDK", "python", "WalabotAPI.py"
    )
elif platform.startswith("linux"):
    modulePath = join("/usr", "share", "walabot", "python", "WalabotAPI.py")

wlbt = load_source("WalabotAPI", modulePath)
wlbt.Init()


def PrintBreathingEnergy(energy):
    system("cls" if platform == "win32" else "clear")
    print("Energy = {}".format(energy * 1e7))


def BreathingApp():
    # Walabot_SetArenaR - input parameters
    minInCm, maxInCm, resInCm = 30, 150, 1
    # Walabot_SetArenaTheta - input parameters
    minIndegrees, maxIndegrees, resIndegrees = -4, 4, 2
    # Walabot_SetArenaPhi - input parameters
    minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees = -4, 4, 2
    # Initializes walabot lib
    wlbt.Initialize()
    # 1) Connect : Establish communication with walabot.
    wlbt.ConnectAny()
    # 2) Configure: Set scan profile and arena
    # Set Profile - to Sensor-Narrow.
    wlbt.SetProfile(wlbt.PROF_SENSOR_NARROW)
    # Setup arena - specify it by Cartesian coordinates.
    wlbt.SetArenaR(minInCm, maxInCm, resInCm)
    # Sets polar range and resolution of arena (parameters in degrees).
    wlbt.SetArenaTheta(minIndegrees, maxIndegrees, resIndegrees)
    # Sets azimuth range and resolution of arena.(parameters in degrees).
    wlbt.SetArenaPhi(minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees)
    # Dynamic-imaging filter for the specific frequencies typical of breathing
    wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_DERIVATIVE)
    # 3) Start: Start the system in preparation for scanning.
    wlbt.Start()
    # 4) Trigger: Scan (sense) according to profile and record signals to be
    # available for processing and retrieval.

    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()

    all_data = []

    run = True
    print(wlbt.GetAntennaPairs())
    while run:
        appStatus, calibrationProcess = wlbt.GetStatus()
        wlbt.Trigger()
        antennaPair = wlbt.GetAntennaPairs()[0]
        rawData, timeAxis = wlbt.GetSignal(antennaPair)

        t = time.time_ns()

        reshaped_data = np.reshape(rawData, (4096, 1))

        all_data.append(reshaped_data)

        print(f"Captured {len(rawData)} data points for time {t}")

        if len(all_data) >= 2000:
            run = False

    all_data_array = np.array(all_data)

    np.save("raw_data_matrix.npy", all_data_array)

    print("Data saved successfully!")

    wlbt.Stop()
    wlbt.Disconnect()
    wlbt.Clean()
    print("Terminate successfully")


if __name__ == "__main__":
    BreathingApp()
