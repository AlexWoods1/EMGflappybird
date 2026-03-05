from multiprocessing import Process, Value
import SignalAquisition
import flappybird

if __name__ == "__main__":
    ("\n"
     "    Here I decided to split the cores of my computer and use different Processes to run the game UI\n"
     "     and the signal aquisition separately. This leads to the memories being split as well and thus\n"
     "      I have to define which variables are shared below\n"
     "      ")
    # Specifying Player Voltages So I can use multiprocessing
    Player_1_Voltage = Value('d', 0.0)
    Player_2_Voltage = Value('d', 0.0)


    # Create processes
    p1 = Process(target=SignalAquisition.signalreader, args=(Player_1_Voltage, Player_2_Voltage))
    p2 = Process(target=flappybird.RUN_GAME, args=(Player_1_Voltage, Player_2_Voltage,))


    # Start processes
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Final value:", Player_1_Voltage.value)
    print("Final value:", Player_2_Voltage.value)