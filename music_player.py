### IMPORTS ###
import sys
# add the System directory to the system path
sys.path.append('/home/me/System')
import os
import subprocess
import json
import logging
import socket

### LOGGING SETUP ###
# create new logger
log = logging.getLogger('my_logger')
# configure the logger
logging.basicConfig(filename='/home/me/System/musicpilog.log', level=logging.INFO, format='%(asctime)s - %(message)s')

### MUSIC CLASS ###
class Player:
# initialize the music class;
    def __init__(self):
# define the path to the mpv socket
        self.ipc_socket = "/tmp/mpvsocket"  # Define the IPC socket path
# define the process variable
        self.process = None  # To store the mpv process
# kill all mpv processes
        os.system("killall mpv")
# logging
        log.info("Player: initialized;")

# function to play a media file or stream
    def play(self, what):
# if the process is already running and not terminated
        if self.process and self.process.poll() is None:
# stop any existing mpv process
            self.stop()

# start the mpv process with the IPC server
        self.process = subprocess.Popen(
            ['mpv', '--no-terminal', '--input-ipc-server=' + self.ipc_socket, what],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
# lgging
        log.info(f"Player: playing: {what};")

# funtion to stop the mpv process
    def stop(self):
# if process is running and not terminated
        if self.process and self.process.poll() is None:
# send the quit command to the mpv process via the IPC socket
            os.system(f"echo '{{ \"command\": [\"quit\"] }}' | socat - {self.ipc_socket}")
# terminate the process
            self.process.terminate()
# kill all mpv processes
            os.system("killall mpv")
# reset the process variable
            self.process = None
# logging
            log.info("Player: stopped playing;")

# if process is not running
        else:
# do nothing
            pass

# function to pause or resume the currently playing media
    def toggle (self):
# send the cycle pause command to the mpv process via the IPC socket
        os.system(f"echo '{{ \"command\": [\"cycle\", \"pause\"] }}' | socat - {self.ipc_socket}")
# logging
        log.info("Player: toggled playing;")

# function to go to the next track
    def next (self):
# send the next track command to the mpv process via the IPC socket
        os.system(f"echo '{{ \"command\": [\"playlist-next\"] }}' | socat - {self.ipc_socket}")
# logging
        log.info("Player: playing next track;")

# function to go to the previous track
    def previous (self):
# send the previous track command to the mpv process via the IPC socket
        os.system(f"echo '{{ \"command\": [\"playlist-prev\"] }}' | socat - {self.ipc_socket}")
# logging
        log.info("Player: playing previous track;")

# function to get the currently playing song
    def get(self):
# try to connect to the mpv IPC socket
        try:
# create a socket connection
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
# connect to the mpv IPC socket
            client.connect(self.ipc_socket)
# send the get_property command to get the current playing song info
            client.sendall(json.dumps({"command": ["get_property", "media-title"]}).encode('utf-8') + b'\n')
# receive the response from the mpv process
            response = client.recv(1024)
# close the socket connection
            client.close()
# decode the response and load it as JSON
            result = json.loads(response.decode('utf-8'))
# if there is an error part and it has anything in it, set data to nothing
            if "error" in result:
                if result["error"] and result["error"] != "success":
                    result["data"] = "nothing"
                del result["error"]
# take off the file name extension (.*) and the numbers at the beginning of the file name (0-9.)
            if result.get("data") and isinstance(result["data"], str):
                import re
                result["data"] = re.sub(r'\.[^.\\/:*?"<>|\s]+$', '', result["data"])
                result["data"] = re.sub(r'^\d{2}\.\s', '', result["data"])
# logging
            log.info(f"Player: returning current playing song info: {result};")
# return the song info
            return result.get("data")
# if error
        except:
# logging
            log.info("Player: error getting current playing song info;")
# return nothing
            return "nothing"