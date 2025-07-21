# myevdev.py
# created by ChatGPT (chatgpt.com) 5/8/2025 on instruction from user
# Modified to use fixed input device: /dev/input/event4

from evdev import InputDevice, categorize, ecodes
import threading

class Listener:
    def __init__(self, on_press=None, device_path="/dev/input/event4"):
        # Callback function for key press
        self.on_press = on_press
        self.device_path = device_path  # <- using fixed device path
        self._device = None
        self._running = False
        self._thread = None

    def _listen(self):
        """
        Listen to key events from the input device.
        Calls self.on_press when a key is pressed.
        """
        try:
            self._device = InputDevice(self.device_path)
            self._running = True

            for event in self._device.read_loop():
                if not self._running:
                    break

                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        key_name = key_event.keycode
                        if isinstance(key_name, list):
                            key_name = key_name[0]

                        class Key:
                            def __init__(self, name):
                                self.char = name[4:].lower() if name.startswith('KEY_') else None
                                self.name = self.char if self.char else name

                            def __repr__(self):
                                return f"Key.{self.name}"

                        if self.on_press:
                            self.on_press(Key(key_name))

        except Exception as e:
            print(f"Listener error: {e}")

    def start(self):
        if not self._thread:
            self._thread = threading.Thread(target=self._listen, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def join(self):
        if not self._thread:
            self.start()
        while self._running:
            try:
                self._thread.join(1)
            except KeyboardInterrupt:
                break

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


# ✅ Example usage
if __name__ == "__main__":
    def on_press(key):
        print(f"Pressed: {key}")

    # Using fixed device: /dev/input/event4
    key_listener = Listener(on_press=on_press, device_path="/dev/input/event4")
    key_listener.join()