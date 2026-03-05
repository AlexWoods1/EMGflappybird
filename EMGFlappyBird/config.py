from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True)
class Hardware:
    SAMPLING_RATE: int = 500
    V_SOURCE: float = 5.0
    PLAYER_1_PIN: int = 0
    PLAYER_2_PIN: int = 5

@dataclass(frozen=True)
class Screen:
    WIDTH: int = 1000
    HEIGHT: int = 750

@dataclass(frozen=True)
class Options:
    SAVE_FILE: bool = True

    @staticmethod
    def file_path(time):
        return './Trial_files/trial_{time}.csv'.format(time=time)



@dataclass(frozen=True)
class Physics:
    GRAVITY: float = 0.0
    GAME_GRAVITY: float = 0.2
    FLAP: float = -6.0

@dataclass(frozen=True)
class Pipes:
    PIPE_SPEED: int = 3
    PIPE_GAP: int = 190
    PIPE_WIDTH: int = 60
    PIPE_INTERVAL: int = 1500

@dataclass(frozen=True)
class EMG:
    RMS_WINDOW: int = 200
    THRESHOLD_1: float = 0.2
    THRESHOLD_2: float = 0.2
    READY_RMS_MAX: float = 5.0
    READY_TIME: int = 5000       # ms before auto-start fallback

    def buffer_length(self, sampling_rate: int) -> int:
        return int(sampling_rate * self.RMS_WINDOW / 1000)

HARDWARE = Hardware()
SCREEN = Screen()
PHYSICS = Physics()
PIPES = Pipes()
EMG = EMG()

# Derived constants
BUFFER_LENGTH = EMG.buffer_length(HARDWARE.SAMPLING_RATE)
OUTPUT_PATH = Options.file_path(time=datetime.now().strftime("%Y%m%d_%H%M%S"))