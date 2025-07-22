# 🎵 MusicPi

MusicPi is a modular, extensible, and hackable music/media system for Raspberry Pi, designed for physical controls, OLED display, and integration with custom hardware (like Pico microcontrollers). It’s perfect for building your own jukebox, media center, or interactive music player!

---

## 🚀 Features

- **Physical Controls:** Use buttons, rotary encoders, and potentiometers for playback, navigation, and volume/tone control.
- **OLED Display:** Real-time menu, notifications, and playback info on a Waveshare OLED screen.
- **MPV Integration:** Robust playback via MPV, supporting local files and streams.
- **Dynamic Menus:** Auto-generated menus from your music folder, including Play All, artist info, and folder navigation.
- **Pico Microcontroller Support:** CircuitPython/MicroPython code for sending keypresses and analog data to the Pi.
- **Logging:** All actions and errors are logged for easy debugging.
- **Modular Design:** Easy to extend with new controls, displays, or features.

---

## 🗂️ Project Structure

```
background.py           # Manages system state, power, and screen
evdevlib.py             # Makes using evdev easer to help with listening for key events from input devices
generate_albums_json.py # Scans music folders and generates menu JSON
handle_volume.py        # Handles volume changes via serial (Pico)
music_player.py         # MPV-based playback control
music_system.py         # Main system logic and menu navigation
OLED.py                 # OLED display abstraction
OLED/                   # OLED library, examples, and assets
Pico/                   # Microcontroller code and examples
```

---

## 🛠️ Setup & Installation

### 1. **Dependencies**

- Python 3.x
- [MPV](https://mpv.io/) media player
- [Pillow](https://python-pillow.org/) for image handling
- [Mutagen](https://mutagen.readthedocs.io/) for MP3 metadata
- [evdev](https://python-evdev.readthedocs.io/) for input device handling
- [gpiozero](https://gpiozero.readthedocs.io/) for GPIO
- [Waveshare OLED Python Library](OLED/lib/waveshare_OLED/)

Install dependencies:
```sh
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-numpy mpv socat
sudo pip3 install mutagen evdev gpiozero Pillow
```

### 2. **Hardware Connections**

- **OLED Display:** Connect as per [OLED/readme_EN.txt](OLED/readme_EN.txt).
- **Buttons/Potentiometers:** Wire to Pico as per [Pico/main.py](Pico/main.py).
- **Serial Connection:** Pico to Pi via USB (for volume/tone).

### 3. **Configuration**

- Place your music in `/home/me/Music` (or edit paths in the code).
- Edit device paths in the various programs if needed.
- Reprogram bits and pieces to work with alternate hardware

---

## 🏃 Running MusicPi

1. **Start the background manager:**
   ```sh
   python3 background.py
   ```
   This will handle power and screen state, and launch the main system.

2. **Main system logic:**
   - [`music_system.py`](music_system.py) is launched by the background manager.
   - OLED displays menus and playback info.
   - Key events from Pico or keyboard control navigation and playback.

3. **Volume Control:**
   - [`handle_volume.py`](handle_volume.py) listens for serial data from Pico and adjusts system volume.

---

## 🎛️ Controls

See [Pico/keys_used.txt](Pico/keys_used.txt) for key mappings:

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

## 🖥️ OLED Display

- Menus, notifications, and playback info are shown using [`OLED.py`](OLED.py).
- Customizable via Pillow fonts and images.
- Example usage in [OLED/example/waveshare_example.py](OLED/example/waveshare_example.py).

---

## 🧩 Extending MusicPi

- Add new menu actions in [`generate_albums_json.py`](generate_albums_json.py).
- Add new hardware controls by extending [`evdevlib.py`](evdevlib.py) or Pico code.
- Customize OLED display in [`OLED.py`](OLED.py).

---

## 📝 Example: Adding a New Button

1. Wire the button to Pico and assign a GPIO pin.
2. In [Pico/main.py](Pico/main.py), send a new keycode.
3. In [`music_system.py`](music_system.py), handle the new key in the `press` function.

---

## 🐛 Troubleshooting

- **No display:** Check OLED wiring and font paths.
- **No sound:** Ensure MPV is installed and working.
- **No key response:** Check device path in [`evdevlib.py`](evdevlib.py).
- **Volume not changing:** Check serial connection and Pico code.

---

## 📚 References

- [Waveshare OLED Documentation](OLED/readme_EN.txt)
- [MPV JSON IPC](https://mpv.io/manual/master/#json-ipc)
- [CircuitPython HID](https://circuitpython.readthedocs.io/en/latest/shared-bindings/adafruit_hid/)
- [gpiozero](https://gpiozero.readthedocs.io/)

---

## 💡 Credits

- ComputerL
- Waveshare for OLED libraries
- Adafruit for HID libraries
- Github Copilot helped mainly with evdevlib.py, generate_albums_json.py, and documentation

---

## 🦾 License

MIT License for all custom code. See individual files for third-party licenses.

---

## 🤘 Have fun hacking your music system!