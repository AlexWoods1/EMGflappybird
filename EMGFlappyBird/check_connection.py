from serial.tools import list_ports
from pyfirmata2 import Arduino


def find_arduino():
    """Find Arduino MEGA automatically"""
    for port in list_ports.comports():
        if 'arduino' in port.description.lower():
            print(f"Found Arduino at: {port.device}")
            return port.device
    return None


# Find and connect
def check_arduino_connection() -> str | None:
    """

    :rtype: object
    """
    connection = None
    try:
        arduino_port = find_arduino()
        if arduino_port is None:
            print("Unable to find Arduino!")
        else:
            board = Arduino(arduino_port)
            print('Connected to Arduino!')
            board.exit()
            connection = arduino_port
    except Exception as e:
        print(f"Failed to connect: {e}")
        print("Check your port in .env")
    finally:
        if connection is not None:
            return connection
        else:
            print('Failed to connect: exiting file.')
            exit("See:Check_connection.py")
