from pyfirmata2 import Arduino
from check_connection import check_arduino_connection
from config import HARDWARE,Options, OUTPUT_PATH
import pandas as pd
import time


def save_results(data, path):
    df = pd.DataFrame(data, columns=['VoltageP1', 'VoltageP2', 'TimeIndex'])
    df.to_csv(path, index=False)

def make_callback(player_voltage):
    def callback(pin_value):
        if pin_value is None: return
        pin_voltage = pin_value * HARDWARE.V_SOURCE
        if pin_voltage < 0.01: pin_voltage = 0.0
        with player_voltage.get_lock():
            player_voltage.value = pin_voltage
    return callback

def signal_reader(player_1_voltage, player_2_voltage):
    board = Arduino(check_arduino_connection())
    board.samplingOn(1000 // HARDWARE.SAMPLING_RATE)
    samples = []

    # specify each pin and variable it is attached to
    for pin, voltage in [(HARDWARE.PLAYER_1_PIN, player_1_voltage), (HARDWARE.PLAYER_2_PIN, player_2_voltage)]:
        channel = board.analog[pin]
        channel.register_callback(make_callback(voltage))
        channel.enable_reporting()


    try:
        while True:
            samples.append((player_1_voltage.value, player_2_voltage.value, time.monotonic()))
            time.sleep(1 / HARDWARE.SAMPLING_RATE)

    except KeyboardInterrupt:
        pass
    finally:
        board.samplingOff()
        board.exit()
        if Options.SAVE_FILE:
            save_results(samples, OUTPUT_PATH)

        print('signal collected!')
    return