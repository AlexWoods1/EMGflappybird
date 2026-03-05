# EMG Controlled Flappy Bird Project
##### UCSD BENG 152 FINAL PROJECT
A two-player game controlled by muscle contractions, built as a bioengineering application for pediatric EMG testing. Each player's EMG signal is read via electrodes, processed in real time, and mapped to a Flappy Bird-style game — making muscle function testing more engaging for younger patients.
### How It Works
Each player has 2 electrodes placed on a muscle. The raw EMG signal is acquired via Arduino, filtered, and the RMS value is computed. Each player's RMS value controls the vertical position of their bird on screen. Players must contract their muscle to flap and navigate through pipes.

## Built With
* Python
* Arduino
* Pyfirmata
* Pygame
* Pandas
* Numpy

## Getting Started
Follow the installation process and run it. 


### Installation
  For the Arduino:
  1. Open Arduino IDE
  2. Open File
  3. Go to Examples
  4. Open Firmate
  5. Select Standard Firmata
  6. Upload to Board
 In the terminal Do:
  1. git clone https://github.com/AlexWoods1/EMGflappybird.git
  2. cd EMGflappybird # This will leave you without Signal_Analysis, containing the Jupyter notebook, but it isn't necessary for signal acquisition.
  4. make install or pip install -r requirements.txt
  5. make check
  6. make run
  7. make notebook # If you downloaded Signal_Analysis


In a single line for the terminal:
git clone https://github.com/AlexWoods1/EMGflappybird.git && cd EMGflappybird && python -m venv test_env && test_env\Scripts\activate && pip install -r requirements.txt && python EMGFlappyBird/main.py

python -m venv test_env && test_env\Scripts\activate && pip install -r requirements.txt && python EMGFlappyBird/main.py

## Contact
* Alex Woods - [a5woods@ucsd.edu](mailto:a5woods@ucsd.edu)
* Andrew Habata - [Your Email Address](mailto:your.email@example.com)
