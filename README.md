# EMG Controlled Flappy Bird Project
##### UCSD BENG 152 FINAL PROJECT
A two-player game controlled by muscle contractions, built as a bioengineering demonstration of EMG use cases. Each player's EMG signal is read via electrodes, processed in real time, and mapped to control a character in a Flappy-Bird style game.

### How It Works
Each player has 2 electrodes placed on a muscle. The raw EMG signal is acquired via Arduino, filtered, and the RMS value is computed. Each player's RMS value controls the vertical position of their bird on screen. Players must contract their muscles to flap and navigate through pipes.

## Built With
* Python
* Arduino
* Pyfirmata
* Pygame
* Pandas
* Numpy

## Getting Started: Hardware
TODO

## Getting Started: Software

#### Arduino Instructions:
  1. Open Arduino IDE
  2. Open File
  3. Go to Examples
  4. Open Firmate
  5. Select Standard Firmata
  6. Upload to Board

#### Terminal Instructions:
  1. git clone https://github.com/AlexWoods1/EMGflappybird.git
  2. cd EMGflappybird
  3. py -m venv test_env
  4. source test_env/Scripts/activate
  5. pip install -r requirements.txt
  6. python EMGFlappyBird/main.py


In a single line for Git Bash:
**git clone https://github.com/AlexWoods1/EMGflappybird.git && cd EMGflappybird && py -m venv test_env && source test_env/Scripts/activate && pip install -r requirements.txt && python EMGFlappyBird/main.py**


For re-running the Python files, run step #6 again.

To delete the files and exit the virtual environment, run in Git Bash.

deactivate && cd .. && rm -rf EMGFlappyBird

## Authors
* Alex Woods 
* Andrew Habata 
