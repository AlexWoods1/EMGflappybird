def signalreader(Player_1_Voltage, Player_2_Voltage):
    import pyfirmata2
    import serial
    from serial.tools import list_ports
    from pyfirmata2 import Arduino
    import time

    SAMPLING_RATE = 1000

    def find_arduino():
        """Find Arduino MEGA automatically"""
        for port in list_ports.comports():
            if 'arduino' in port.description.lower():
                print(f"Found Arduino at: {port.device}")
                return port.device
        return None

    # Find and connect
    arduino_port = find_arduino()
    if arduino_port is None:
        print(" Arduino not found!")
        exit()
    board = Arduino(arduino_port)

    #constants:
    V_SOURCE = 5.0


    def cb_a0(val):
        if val is None: return
        voltage = val * V_SOURCE
        if voltage < 0.01: voltage = 0.0
        with Player_1_Voltage.get_lock():
            Player_1_Voltage.value = voltage

    def cb_a1(val):
        if val is None: return
        voltage = val * V_SOURCE
        if voltage < 0.01: voltage = 0.0
        with Player_2_Voltage.get_lock():

            Player_2_Voltage.value = voltage

    # Specifies which pins we are using
    a0 = board.analog[0]
    a1 = board.analog[5]

    a0.register_callback(cb_a0)
    a1.register_callback(cb_a1)

    a0.enable_reporting()
    a1.enable_reporting()

    board.samplingOn(1000 / SAMPLING_RATE)
    # sets  board sampling rate as 1000ms / Desired Sampling rate which we can use to specify sampling in terms of HZ.

    # Keep the script running to listen for callbacks
    try:
        player_1 = []
        player_2 = []
        time_index = []
        while True:
            board.iterate()
            player_1.append(Player_1_Voltage.value)
            player_2.append(Player_2_Voltage.value)
            time_index.append(time.time())

            time.sleep(0.1)
    except KeyboardInterrupt:
        import pandas as pd
        df = pd.DataFrame({'VoltageP1': player_1, 'VoltageP2': player_2, 'TimeIndex': time_index})
        df.to_csv('C:/Users/alexa/PythonProject/temp/Sample_Data.csv')
        print(df)



    finally:
        board.exit()
