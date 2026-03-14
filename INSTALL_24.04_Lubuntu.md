# Installing Lubuntu 24.04

**Hardware:** Lenovo Laptop
**OS:** Lubuntu 24.04 (LXQt desktop, X11/Xorg)
**Purpose:** General workstation

> Lubuntu is Ubuntu-based. It lacks `snapd` by default — install it first.
> PyCharm Community did not work from the default install; see snap install steps below.
> **When in doubt, use instructions for Ubuntu.**
>
> **Critical:** swapfile must be ≥ 3 GB when RAM is only 4 GB.
> Set `vm.swappiness=10` (from 60) for better mouse responsiveness.

---

## Table of Contents

- [1. Boot and Install](#1-boot-and-install)
- [2. Initial Setup](#2-initial-setup)
- [3. GitHub Desktop](#3-github-desktop)
- [4. Install Applications](#4-install-applications)
- [5. Serial / USB Setup](#5-serial--usb-setup)
- [6. Arduino](#6-arduino)
- [7. Alternate Python Version](#7-alternate-python-version)
- [8. Sound Configuration](#8-sound-configuration)
- [9. Auto Suspend Scheduling](#9-auto-suspend-scheduling)
- [10. Cleanup](#10-cleanup)
- [11. HDMI Audio](#11-hdmi-audio)
- [12. Google Drive (Rclone)](#12-google-drive-rclone)
- [13. Optional Tools](#13-optional-tools)

---

## 1. Boot and Install

Insert ISO USB and boot:
- **F12** on Lenovo (rapid), **F10** on HP-Omen, **F7** on little_guy
- Set boot order to USB

Choose **"Normal installation"** (not minimal — minimal leaves things broken).

Restart will prompt to remove USB. System should restart to Lubuntu without BIOS boot.

After restart:
- Install Updates and reboot
- Install drivers (none may be available on Lenovo)

---

## 2. Initial Setup

```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt install -y git
sudo apt install snapd
sudo apt install -y ubuntu-restricted-extras
sudo apt install -y python3-pip
```

Lubuntu installs by default: LibreOffice, VLC, Firefox
    vlc - open and turn off acceleration tools - preferences - input/codecs - disable Hardware-accelerated decoding - save
    Firefox - see tuning elsewhere in here

**Connect Google Drive:**
- Check email for "google drive stuff"
- Menu → Desktop Settings → LXQt Settings → Autostart → `/usr/bin/google-drive-ocamlfuse`

---

## 3. GitHub Desktop

```bash
sudo wget https://github.com/shiftkey/desktop/releases/download/release-3.1.1-linux1/GitHubDesktop-linux-3.1.1-linux1.deb
sudo apt-get install -y gdebi-core
sudo gdebi GitHubDesktop-linux-3.1.1-linux1.deb
github
```

When prompted during initial clone, sign in to GitHub.com (password in BitWarden).
**Do not** proactively log in via the browser — wait for GitHub Desktop to request it to avoid an infinite authorization loop.

---

## 4. Install Applications

### VS Code

```bash
snap install code --classic
# Install Particle Workbench extension
# Sign into Particle ASAP
```

Fix missing `crc32` for Particle Workbench:

```bash
sudo apt install libarchive-zip-perl   # no restart needed
```

### PyCharm

```bash
sudo apt install -y python3-tk    # for PyCharm
snap install pycharm-community --classic
# Give it time to index on first launch
```

### Other Apps

```bash
sudo apt install LocalSend
```

### Optional: Jellyfin Media Server

> Better to have NO media server on a 4 GB Lenovo.

```bash
sudo apt install -y flatpak gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
# reboot
flatpak install flathub com.github.iwalton3.jellyfin-media-player
flatpak run com.github.iwalton3.jellyfin-media-player
# Remove:
flatpak remove com.github.iwalton3.jellyfin-media-player
```

### puTTY

```bash
sudo apt install -y putty
```

Add yourself to the `dialout` group:
- Preferences → LXQt Settings → Users and Groups → daveg → Properties → Groups → dialout & uucp

```bash
sudo nano /etc/udev/rules.d/01-ttyusb.rules
# Add:
SUBSYSTEMS=="usb-serial", TAG+="uaccess"
```

Log out and log back in.

### Screen timeout

Settings → Power → set as desired. Reboot.

### PyCharm: pyStateOfCharge

```bash
# Open GUI_..py — get it to run using local venv, then:
install.py
```

### PyCharm: movie_Scraper

```bash
# Setup local venv
# Open GUI_..py — get it to run using local venv, then:
install.py
# pysimpleguiKey.txt in same folder as this file
# Ignore: '_tkinter.TclError: can't use "pyimage7" as iconphoto'
```

---

## 5. Serial / USB Setup

Simple serial check (optional, for debugging):

```bash
sudo apt install screen
sudo screen /dev/ttyACM0 230400
```

---

## 6. Arduino

```bash
sudo apt install -y arduino
```

Libraries for CTE collision (Arduino IDE v1.8.19): `Arduino_LSM6DS3`, `AceCommon`, `AceCRC`, `AceRoutine`, `AceUtils`, `Adafruit BusIO`, `Adafruit LSM6DS`, `SafeString`

Boards: Boards Manager → Arduino SAMD boards → Arduino Nano 33 IoT

**Dark theme for Arduino IDE:**

```bash
cd /usr/share/arduino/lib
sudo mv theme themeOld
# Download DarkArduinoTheme from https://github.com/jeffThompson/DarkArduinoTheme
sudo cp -r /home/daveg/Downloads/DarkArduinoTheme-master/theme .
```

---

## 7. Alternate Python Version

> **Never replace the default Python in Debian-based Linux.**

Install build dependencies:

```bash
sudo apt update
sudo apt install -y wget build-essential libreadline-dev libncursesw5-dev \
  libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
  libffi-dev zlib1g-dev portaudio19-dev
```

Download and compile:

```bash
# From https://www.python.org/ftp/python/
cd Downloads/
tar -Jxf Python-3.11.9.tar.xz
cd Python-3.11.9/
./configure --enable-optimizations --enable-shared
sudo make -j4 && sudo make altinstall
sudo ldconfig /usr/local/lib

# Verify
python3.11 --version
python3.11 -m pip --version

# Uninstall (if needed)
cd Downloads/Python-3.11.9/
sudo make uninstall
```

Use `.venv` in PyCharm to set up an app with this Python version.

---

## 8. Sound Configuration

```bash
sudo apt install ffmpeg
sudo apt install -y portaudio19-dev
sudo nano /etc/modules-load.d/modules.conf
# Add:
snd-aloop

# Load for this session:
sudo modprobe snd-aloop
```

> The 4 GB Lenovo laptops don't have enough CPU bandwidth to run ffmpeg even at low quality — skip screencasting.

---

## 9. Auto Suspend Scheduling

```bash
chmod +x /home/daveg/bin/suspend_until

sudo crontab -e
# Add:
1 0 * * 1-6 /home/daveg/bin/suspend_until 16:00   # Mon-Sat: wake at 4 PM
1 0 * * 0   /home/daveg/bin/suspend_until 10:15   # Sun: 10:15 AM

sudo crontab -l   # verify
```

No restart needed.

---

## 10. Cleanup

Preferences - Xscreensaver  - Display modes - Blank 10, Cycle 10, Lock 45
                            - Advanced - Power Management 30 / 60 / 120 - Close

```bash
sudo apt autoremove
sudo apt autoclean
sudo apt clean
sudo apt install deborphan
sudo apt remove $(deborphan)

# Passwords (ignore warnings):
sudo passwd daveg
sudo passwd   # root
rm ~/.local/share/keyrings/login.keyring
```

---

## 11. HDMI Audio

```bash
sudo apt install pulseaudio alsa-utils
pactl load-module module-alsa-sink device=hw:0,3
sudo nano /etc/pulse/default.pa
# Add at end:
pactl load-module module-alsa-sink device=hw:0,3
```

Open PulseAudio Volume Control → Configuration → Profile: Digital Stereo (HDMI) Output + Analog Stereo Input.

---

## 12. Google Drive (Rclone)

See [INSTALL_24.04_Ubuntu.md](INSTALL_24.04_Ubuntu.md) for Rclone setup.

**Auto-start rclone on login:**

```bash
mkdir -p ~/bin
cat << EOF > ~/bin/Rclone
#!/bin/bash
rclone mount grive: ~/gdrive &
EOF
chmod +x ~/bin/Rclone

cat << EOF > ~/.config/autostart/rclone.desktop
[Desktop Entry]
Name=rclone
Exec=/home/daveg/bin/Rclone
Terminal=false
Type=Application
X-Desktop-File-Install-Version=0.27
EOF
chmod +x /home/daveg/.config/autostart/rclone.desktop
```

Test the autostart entry:

```bash
gio launch ~/.config/autostart/rclone.desktop
# or
sudo apt install dex
dex ./.config/autostart/rclone.desktop
```


Configuration steps:
1. Enter `n` to create a new remote
2. Name it `gdrive`
3. Select `drive` for Google Drive (type 18 or search)
4. Leave `client_id` and `client_secret` blank
5. Scope: `1` (Full access)
6. Leave `root_folder_id` and `service_account_file` blank
7. Advanced config:
   - OAuth Access Token: https://myaccount.google.com/apppasswords — name it `Rclone`
   - `auth_url`: blank
   - `token_url`: blank
   - `upload_cutoff`: 1G
8. `Use auto config?`: `y` — authenticate in browser
9. Team Drive: `n` (unless using Team Drive)
10. Confirm: `y`
11. Exit: `q`

**Mount Google Drive:**

```bash
mkdir ~/gdrive
rclone mount gdrive: ~/gdrive &
```

Add startup application: `"gdrive"` with command `"rclone mount gdrive: ~/gdrive &"`

Remove ocamlfuse if previously installed.

---

## 13. Optional Tools

### Jellyfin (alternative to Plex)

```bash
curl -s https://repo.jellyfin.org/install-debuntu.sh | sudo bash
sudo usermod -a -G daveg jellyfin
# Visit http://localhost:8096
sudo chown -R jellyfin /media/daveg
```

### Disk Usage

```bash
sudo apt install ncdu
sudo apt install baobab
sudo apt install git-filter-repo
```

### Bluetooth GUI

Lubuntu → System → Discover → search "bluetooth" → install "Bluetooth Manager"

### Chrome Browser

```bash
# Download .deb from https://www.google.com/chrome
cd Downloads
sudo dpkg -i google-chrome-stable_current_amd64.deb
# If dependency issues: sudo apt --fix-broken install
```

### Guake Terminal

```bash
sudo apt install guake
# Set to start on login
```

### Ferdium

Install via File → System Discover

### Firefox Performance

```
about:config
browser.sessionstore.interval = 150000
```

### Fix missing idlelib

```bash
sudo apt-get install idle-python3.12
```
