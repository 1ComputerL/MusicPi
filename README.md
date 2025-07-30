# MusicPi
What if you wanted to create a media player? Something portable, maybe even housed in an old boombox. And you decide to go completely crazy and gut out somebody’s dead Sony CFD-V15, replace all the parts but the speakers, and design all the software yourself. Maybe you feel that with Raspberry Pi, an audio DAC, some wrecking tools, and a lot of programming, you can make it work. But how?

That’s the challenge I gave myself, the one I worked hard on and still help to improve. MusicPi, a Linux and Python based system powered by a Raspberry Pi 4 and Pico! Running on programs designed for ease of use. An amazing, open source alternative to popular platforms with their distractions.

And here's the Github repo!

MusicPi is a modular, extensible, and hackable music/media Python system programmed in python for Raspberry Pi, designed for physical controls, OLED display, and integration with custom hardware (like Pico microcontrollers). It’s perfect for building your own jukebox, media center, or interactive music player! The system uses different programs to support easy setup and bug tracking.

I encourage you to edit the code to suit your needs. Further explanation is provided here, in the instructable.

---

## Features
MusicPi incorporates many features to make for the best user experience, simple interaction with an OLED display six buttons, and a potentiometer.

- **Physical Controls:** Use buttons, rotary encoders, and potentiometers for playback, navigation, and volume/tone control.
- **OLED Display:** Real-time menu, notifications, and playback info on an OLED screen.
- **MPV Integration:** Robust playback via MPV, supporting local files and streams.
- **Dynamic Menus:** Auto-generated menus from a specified music folder
- **Pico Microcontroller Support:** CircuitPython/MicroPython code for sending keypresses and analog data to the Pi.
- **Logging:** All actions and errors are logged for easy debugging.
- **Modular Design:** Easy to extend with new controls, displays, or features.

---

## Programs Structure
These small descriptions only provide an overview of the actual things the programs do and how they do them. To get a real feel for it, look at the code.

```
background.py           # Manages system state, power, and screen
evdevlib.py             # Makes using evdev easier to help with listening for key events from input devices
generate_albums_json.py # Scans music folders and generates menu JSON for music_system.py
handle_volume.py        # Handles volume commands via serial and adjust volume accordingly
music_player.py         # MPV-based playback control
music_system.py         # Main system logic and menu navigation
OLED.py                 # OLED display library
OLED/                   # OLED library, examples, and assets
Pico/                   # Microcontroller code and examples
```

---

## Setup & Installation

### 1. Dependencies
The free programs listed below are all necessary unless you edit the MusicPi system.

- [Python](https://docs.python.org/3/) for running the programs
- [MPV](https://mpv.io/) for playing media
- [socat](https://linux.die.net/man/1/socat) for sending ipc commands to mpv processes
- [Pillow](https://python-pillow.org/) for image handling
- [Mutagen](https://mutagen.readthedocs.io/) for MP3 metadata
- [evdev](https://python-evdev.readthedocs.io/) for input device handling
- [Waveshare OLED Python Library](https://www.waveshare.com/wiki/0.91inch_OLED_Module) for control of the OLED display

Here are some helpful references

- [MPV JSON IPC](https://mpv.io/manual/master/#json-ipc)
- [CircuitPython HID](https://circuitpython.readthedocs.io/en/latest/shared-bindings/adafruit_hid/)
- [gpiozero](https://gpiozero.readthedocs.io/)

Install dependencies:
```sh
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-numpy mpv socat
sudo pip3 install mutagen evdev gpiozero Pillow
```

### 2. Parts Suggestions
These are the parts I used, the bare minimum needed to run the MusicPi system. The full guide to replicating my build is detailed on the instructable linked to above. Any deviation from them will require reprogramming and optimization of the MusicPi code for your hardware (extra fun I think).
- Raspberry Pi 4 (any should work though)
- Raspberry Pi Pico (again, any should work, but I would suggest the Pico H as it's slightly less expensive then the other variants and comes with pre-soldered headers)
- Waveshare General 0.91" OLED Display Module
- USB Data Cable
- Breadboard
- Breadboard Jumper Wires
- Push buttons

---

### 2. Hardware Connections
Place the pico to the breadboard.
Connect the buttons to the GPIO pins as detailed in the MusicPi/Pico/main.py program, or switch things up and customize the code to register your different button connections.
Connect the OLED module to the Raspberry Pi as shown below (the MusicPi system does not use the originial waveshare OLED library so connect the wires my way or it won't work.)
Plug the USB data cable into the Pico on one end and a computer on the other.

--- 

### 3. Software Setup
- Install the dependencies with the following commands:
```sh
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-numpy mpv socat
sudo pip3 install mutagen evdev gpiozero Pillow
```
- Download the MusicPi folder into the root of a prepared Raspberry Pi OS computer
- Flash the Pico with the latest Circuit Python UF2 (https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython), and then copy the main.py program over to the Pico's root folder.
- Setup MusicPi/background.py to run on boot of the Raspberry Pi (you can use Botspot's Autostar https://github.com/Botspot/autostar)
- Fill ~/Music with media and music for the system
- Reboot

---

## Controls

These are the keypresses that music_system.py responds to. See [Pico/keys_used.txt](Pico/keys_used.txt) for key mappings:

| Button      | Key Sent | Function                |
|-------------|----------|-------------------------|
| Backward    | F1       | Previous track/menu up  |
| Play/Pause  | F2       | Play/Pause/Enter        |
| Forward     | F4       | Next track/menu down    |
| Mode        | F6       | Main menu               |
| Display     | F7       | Power off               |
| Stop        | F8       | Stop playback/back      |
| Power       | F9       | Toggle system power     |
| BCD         | F12      | Toggle screen           |

---

## OLED Display

- Menus, notifications, and playback info are shown using [`OLED.py`](OLED.py).
- Customizable with Pillow fonts and images.
- Example usage in [OLED/example/waveshare_example.py](OLED/example/waveshare_example.py).

---

## Extending MusicPi
Please feel free to suggest and push improvements to the repo. Here are a few things that could be added:
- Add new menu actions in [`generate_albums_json.py`](generate_albums_json.py).
- Add a web socket program to host a website and push keypresses inside the system based on buttons pressed on the website.

---

## Credits

- ComputerL
- VS Code
- Waveshare for OLED libraries
- Adafruit for HID libraries
- VS Code
- ChatGPT
- Github Copilot helped mainly with evdevlib.py, generate_albums_json.py, and documentation

---

## License

This project is licensed under the [MIT License](./LICENSE).  
© 2025 ComputerL (@1ComputerL). See the LICENSE file for details.