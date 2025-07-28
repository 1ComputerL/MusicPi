# This module is a better version of pynput that can be used in much the same way and incorporates evdev to listen for key events from a specific device
# It is used by both background.py and music_system.py
# Created by AI with instructions and code from ComputerL

### IMPORTS ###
# import evdev classes for reading input events
from evdev import InputDevice, categorize, ecodes
# import threading module to run listener in background
import threading
# import json to read device settings from a file
import json
import sys
import os

### PATH SETUP ###
# get the parent directory of this file
parentdir = os.path.dirname(os.path.abspath(__file__))
# add the MusicPi directory to the system path
sys.path.append(parentdir)

### CONFIGURATION ###
# open settings.json file in read mode
with open(parentdir+'/settings.json', 'r') as file:
# parse the json content into a python dictionary
    data = json.load(file)

# extract the value for "eventDevice" key from the dictionary
eventDevice = data["eventDevice"]


### LISTENER CLASS ###
# listener class to handle key events from the device
class Listener:

    # constructor takes optional on_press callback and device path
    def __init__(self, on_press=None, device_path=eventDevice):
        # store the callback function
        self.on_press = on_press

        # store the path to the input device
        self.device_path = device_path

        # placeholder for the InputDevice instance
        self._device = None

        # flag to control the listening loop
        self._running = False

        # placeholder for the listener thread
        self._thread = None


    # private method that runs in a separate thread to handle input events
    def _listen(self):
        """
        listen to key events from the input device.
        calls self.on_press when a key is pressed.
       s """
        try:
            # create an InputDevice instance with the given path
            self._device = InputDevice(self.device_path)

            # set the running flag to true
            self._running = True

            # loop through incoming input events
            for event in self._device.read_loop():

                # if listener is stopped, exit loop
                if not self._running:
                    break

                # check if event is a key event
                if event.type == ecodes.EV_KEY:

                    # categorize the raw event into a key event
                    key_event = categorize(event)

                    # check if the key is pressed down
                    if key_event.keystate == key_event.key_down:

                        # get the name of the key
                        key_name = key_event.keycode

                        # if keycode is a list, take the first item
                        if isinstance(key_name, list):
                            key_name = key_name[0]

                        # inner class to represent a key press
                        class Key:

                            # initialize with key name
                            def __init__(self, name):

                                # extract character name if it starts with "KEY_"
                                self.char = name[4:].lower() if name.startswith('KEY_') else None

                                # use character if available, else original name
                                self.name = self.char if self.char else name

                            # string representation of the key
                            def __repr__(self):
                                # return formatted key name
                                return f"Key.{self.name}"

                        # if callback is defined
                        if self.on_press:

                            # call the callback with a Key instance
                            self.on_press(Key(key_name))

        # handle any exception during listening
        except Exception as e:

            # print error message
            print(f"Listener error: {e}")


    # method to start the listener in a background thread
    def start(self):

        # if thread hasn't been started yet
        if not self._thread:

            # create a new thread targeting _listen
            self._thread = threading.Thread(target=self._listen, daemon=True)

            # start the thread
            self._thread.start()


    # method to stop the listener
    def stop(self):

        # set running flag to false
        self._running = False

        # if thread exists
        if self._thread:

            # wait for the thread to finish
            self._thread.join()


    # method to block and wait for listener thread (used in __main__)
    def join(self):

        # if thread hasn't started yet
        if not self._thread:

            # start the thread
            self.start()

        # while the listener is running
        while self._running:
            try:
                # join thread with timeout to allow keyboard interrupt
                self._thread.join(1)

            # allow graceful exit on ctrl+c
            except KeyboardInterrupt:
                break


    # context manager enter method
    def __enter__(self):

        # start the listener
        self.start()

        # return self so user can interact with the object
        return self


    # context manager exit method
    def __exit__(self, exc_type, exc_val, exc_tb):

        # stop the listener when exiting context
        self.stop()

"""
# example usage of the Listener class
### MAIN ENTRY POINT ###

# check if script is run directly
if __name__ == "__main__":

    # define callback to run when a key is pressed
    def on_press(key):

        # print the key that was pressed
        print(f"Pressed: {key}")

    # create listener instance with callback and device path
    key_listener = Listener(on_press=on_press, device_path=eventDevice)

    # start the listener and wait for it to finish (blocks until interrupted)
    key_listener.join()
"""