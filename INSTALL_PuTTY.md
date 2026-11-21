# PuTTY Installation & Serial Setup

## Installation (Ubuntu / Debian / Lubuntu)

```bash
sudo apt install -y putty
```

## Serial Permissions

Add your user to the `dialout` and `uucp` groups for serial access:

```bash
sudo usermod -aG dialout,uucp $USER
```

**GUI (LXQt only):**
- Preferences → LXQt Settings → Users and Groups → daveg → Properties → Groups → `dialout` & `uucp`

### USB Serial Udev Rule

```bash
sudo nano /etc/udev/rules.d/01-ttyusb.rules
# Add:
SUBSYSTEMS=="usb-serial", TAG+="uaccess"
```

Log out and log back in.

## Verify Connected Serial Devices

```bash
# Verify device after plugging in serial/microcontroller device (e.g., Photon 2, Arduino):
sudo dmesg | grep tty   # usually /dev/ttyACM0 or /dev/ttyUSB0
```
