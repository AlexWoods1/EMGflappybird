from multiprocessing import Process, Value
from signal_aquisition import signal_reader
from flappybird import run_game


if __name__ == "__main__":
    # Specifying Player Voltages So I can use multiprocessing
    player_1_voltage = Value('d', 0.0)
    player_2_voltage = Value('d', 0.0)

    # Create processes
    p1 = Process(target=signal_reader, args=(player_1_voltage, player_2_voltage))
    p2 = Process(target=run_game, args=(player_1_voltage, player_2_voltage))

    # Start processes
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Final value:", player_1_voltage.value)
    print("Final value:", player_2_voltage.value)
