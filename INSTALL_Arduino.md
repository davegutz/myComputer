# Arduino IDE & Microcontroller Setup

## 1. Installation

### Ubuntu / Debian / Lubuntu
```bash
sudo apt update
sudo apt install -y arduino
```

### Arch / CachyOS
```bash
sudo pacman -S arduino
# or for Arduino IDE 2.x:
# sudo pacman -S arduino-ide
```

---

## 2. Serial Permissions

Ensure your user belongs to `dialout` (and `uucp` on Arch) to upload sketches and communicate over serial:

```bash
# Ubuntu / Debian / Lubuntu:
sudo usermod -aG dialout $USER

# Arch / CachyOS:
sudo usermod -aG dialout,uucp $USER
```

Log out and log back in for changes to take effect.

---

## 3. Boards & Core Libraries

### Boards Manager
- Open Arduino IDE → **Tools** → **Board** → **Boards Manager...**
- Search for and install: **Arduino SAMD boards (32-bits ARM Cortex-M0+)** (for Arduino Nano 33 IoT)

### Required Libraries (CTE Collision & Sensor Projects)
In **Sketch** → **Include Library** → **Manage Libraries...**, install:
- `Arduino_LSM6DS3`
- `Adafruit LSM6DS`
- `Adafruit BusIO`
- `AceCommon`
- `AceCRC`
- `AceRoutine`
- `AceUtils`
- `SafeString`

---

## 4. Dark Theme for Arduino IDE v1.x (Optional)

```bash
cd /usr/share/arduino/lib
# Download DarkArduinoTheme from https://github.com/jeffThompson/DarkArduinoTheme
# Extract and copy:
sudo cp -r ~/Downloads/DarkArduinoTheme-master/theme .
```
Restart the Arduino IDE to apply the theme.
