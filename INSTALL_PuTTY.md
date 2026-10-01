# PuTTY Installation & Serial Setup

## Installation (Ubuntu / Debian / Lubuntu)

```bash
sudo apt-get install -y putty
```

## Serial Permissions

Add your user to the `dialout` group for serial access:

```bash
sudo usermod -aG dialout $USER
# Log out and log back in
```

## Verify Connected Serial Devices

```bash
# Verify device after plugging in serial/microcontroller device (e.g., Photon 2, Arduino):
sudo dmesg | grep tty   # usually /dev/ttyACM0 or /dev/ttyUSB0
```
