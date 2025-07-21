### IMPORTS ###
import sys
# add the System directory to the system path
sys.path.append('/home/me/System')
import subprocess
import logging
import evdevlib
import time
import signal
import os

# delay
time.sleep(3)

### LOGGING SETUP ###
# create new logger
log = logging.getLogger('my_logger')
# configure the logger
logging.basicConfig(filename='/home/me/System/musicpilog.log', level=logging.INFO, format='%(asctime)s - %(message)s')

### INITIATE THINGS ###
# global variables to track state of power button
power_button_state = False
prev_power_button_state = False
# set up the systemprogram variable
systemprogram = None
# get the state of the screen
result=os.system(" xrandr | grep -q \" connected [0-9]\"")
# if the result is 0, the screen is (open)
if result == 0:
# set the screen open state to True
    screenOpenState = True
else:
# set the screen open state to False (closed)
    screenOpenState = False
# set the previous screen open state to the current state
screenOpenState_prev = screenOpenState
# function to handle stop signals
def handle_stop_signal(signum, frame):
# terminate subprocess
    try:
        systemprogram.terminate()
    except:
        pass
# logging
    log.info("BackgroundProgram: received stop signal; terminated subprocesses and now exiting;")
# exit the program
    sys.exit(0)

# register the signal handler for SIGTERM
signal.signal(signal.SIGTERM, handle_stop_signal)
# register the signal handler for SIGTSTP
signal.signal(signal.SIGTSTP, handle_stop_signal)
# function to handle f9 key press events
def on_press(key):
# sanitize the key input
    key=str(key)
# enable editing of these global variables
    global power_button_state, screenOpenState
# if the key pressed is f9
    if key == "Key.f9":
# toggle the power button state 
        power_button_state = not power_button_state
# if the key pressed is f7
    elif key == "Key.f12":
# toggle the screen open state
        screenOpenState = not screenOpenState

# create listener to monitor key presses
key_listener = evdevlib.Listener(on_press=on_press)
# start the listener
key_listener.join()

# logging
log.info("BackgroundProgram: background.py started; initiated things (log, stop signal handler, key listener);")

### MAIN LOOP ###
while True:
# if the power button was just now turned off
    if power_button_state == False and prev_power_button_state == True:
# teminate the system.py main program
        systemprogram.terminate()
# update the variable
        prev_power_button_state = False
# logging
        log.info('BackgroundProgram: terminated system.py main program;')

# if the screen was just now opened
    if screenOpenState == False and screenOpenState_prev == True:
# turn on the screen
        os.system("wlr-randr --output DSI-1 --on")
# update the variable
        screenOpenState_prev = False

# if the power button was just now turned on
    if power_button_state == True and prev_power_button_state == False:
# open system.py main program as subprocess
        systemprogram = subprocess.Popen(
            ['/bin/python', '/home/me/System/music_system.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
# update the variable
        prev_power_button_state = True
# logging
        log.info('BackgroundProgram: opened system.py main program as subprocess;')

# if the screen was just now closed
    if screenOpenState == True and screenOpenState_prev == False:
# turn off the screen
        os.system("wlr-randr --output DSI-1 --off")
# update the variable
        screenOpenState_prev = True

# delay
    time.sleep(.05)
