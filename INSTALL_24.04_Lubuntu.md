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
- [14. Work In Progress](#14-work-in-progress)

---

## 1. Boot and Install

Insert ISO USB and boot:
- **F12** on Lenovo (rapid), **F10** on HP-Omen, **F7** on little_guy
- Set boot order to USB

Choose **"Normal installation"** (not minimal — minimal leaves things broken).

Setup and choose a single large partition. Installer will make a swap dynamically.

Restart will prompt to remove USB. System should restart to Lubuntu without BIOS boot.

After restart:
- Install Updates and reboot
- Install drivers (none may be available on Lenovo)

---

## 2. Initial Setup

### Swappiness

```bash
cat /proc/sys/vm/swappiness
sudo sysctl vm.swappiness=10
sudo nano /etc/sysctl.conf
# Add: vm.swappiness=10
```

### Increase Swap

```bash
swapon --show
sudo swapoff /swapfile
sudo fallocate -l 8G /swapfile  # 24G for venus-littleguy
sudo mkswap /swapfile
sudo swapon /swapfile
swapon --show
```

### Basic Installs

```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt install -y git
sudo apt install snapd
sudo apt install -y ubuntu-restricted-extras
sudo apt install -y fuse libfuse2      # AppImage support
sudo apt install -y ffmpeg
sudo apt install -y dos2unix
sudo apt install --fix-missing -y python3-pip
sudo apt install -y python3-tk         # for PyCharm
sudo apt install -y dhcpcd5
sudo apt install LocalSend
# sudo apt install -y vlc  (use Discover instead)
sudo apt install xsel
sudo apt install -y pavucontrol        # for myPyScreencast
sudo apt install -y thunar
sudo apt install -y nautilus
pavucontrol  # defaults to low volume — set to 100% for screencasting
```

Lubuntu installs by default: LibreOffice, Firefox.

### Firefox Security Exceptions

Add exceptions for: `hulu.com`, `amazon.com`, `play.max.com`, `netflix.com`

### Firefox tweaks (`about:config`)

```
layers.acceleration.force-enabled = true
gfx.webrender.all = true
browser.sessionstore.interval = 150000
```

### Chrome tweaks (`chrome://settings/system`)

- Toggle on hardware acceleration → Relaunch

### VLC

Install via System → Discover.

Tools → Preferences → Codecs → **disable hardware-accelerated decoding** → Save. Restart VLC.

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
# answer jellyfin_..._pkg by cut and paste from hint below box during initial run
# Remove:
flatpak remove com.github.iwalton3.jellyfin-media-player
```

**Install server:**

```bash
curl -s https://repo.jellyfin.org/install-debuntu.sh | sudo bash
sudo usermod -a -G daveg jellyfin
# Visit http://localhost:8096
sudo chown -R jellyfin /media/daveg
```

**Start:** Browse to Start bookmarks in Firefox and visit Jellyfin. User is `jellyfin`.

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

### myPyScreencast
- Use its own `.venv`
- may need to uninstall and reinstall pillow to eliminate the interpreter's confusion

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
cp home/daveg/Documents/GitHub/myComputer/suspend_until /home/daveg/bin/.
chmod +x /home/daveg/bin/suspend_until

sudo crontab -e
# Add:
1 0 * * 1-6 /home/daveg/bin/suspend_until 16:00   # Mon-Sat: wake at 4 PM
1 0 * * 0   /home/daveg/bin/suspend_until 10:15   # Sun: 10:15 AM

sudo crontab -l   # verify

nano .bashrc
  alias suspend='suspend_until 16:00'
```

No restart needed.

---

## 10. Cleanup

Open **Xscreensaver** (Preferences → Xscreensaver):
- Display Modes: Blank 10, Cycle 10, Lock 45
- Advanced → Power Management: 30 / 60 / 120 → Close

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

See [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md) for Rclone setup.

---

## 13. Optional Tools

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
sudo apt install libu2f-udev
cd Downloads
rm google-chrome-stable*.deb
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

**Uninstall Chrome:**

```bash
# Uninstall 'google chrome' from Ubuntu Software app
sudo apt remove libu2f-udev
sudo apt autoremove
sudo apt autoclean && sudo apt clean
sudo apt install deborphan && sudo apt remove $(deborphan)
```

### Guake Terminal

```bash
sudo apt install guake
# Set to start on login
```

### Ferdium

Install via File → System Discover

### Fix missing idlelib

```bash
sudo apt-get install idle-python3.12
```

### Add support for keypress in pyCharm projects

A udev rule automatically sets correct permissions on `/dev/uinput` at boot.

Create `/etc/udev/rules.d/99-uinput.rules`:

```bash
sudo nano /etc/udev/rules.d/99-uinput.rules
```

Add one of the following:

**Option A (Recommended):** Adds your user to the input group.
```
KERNEL=="uinput", SUBSYSTEM=="misc", OPTIONS+="static_node=uinput", GROUP="input", MODE="0660"
```

**Option B (Less secure):** Grants access to everyone.
```
KERNEL=="uinput", MODE="0666"
```

Apply the changes:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

For Option A, also add your user to the input group:

```bash
sudo usermod -a -G input $USER
```

Reboot for group membership to take effect. Python scripts can then open `/dev/uinput` without `sudo` (evdev >= v3.12).

### Reliable WiFi (DNS Fix)

If WiFi drops or DNS resolution fails (especially with competing hotspots):

```bash
sudo nano /etc/systemd/resolved.conf
# Add:
DNS=8.8.8.8 8.8.4.4
FallbackDNS=1.1.1.1 1.0.0.1
```

This ensures DNS works globally regardless of what NetworkManager does per-interface.

---

## 14. Work In Progress

### Chrome Remote Desktop

See [INSTALL_Chrome_Remote_Desktop](INSTALL_Chrome_Remote_Desktop.md) for setup.

### noMachine Desktop Share

See [INSTALL_noMachine](INSTALL_noMachine.md) for setup.

### VPN/DNS on Travel Router

Configure the TP-Link TL-WR1502X as a VPN client using Proton's OpenVPN files, then set custom NextDNS IPv4 addresses in the router's IPv4 settings.

**Step 1: Download Proton VPN Configuration**

Log in at <https://account.protonvpn.com/downloads>. Go to Downloads → OpenVPN configuration files. Select Router as the platform and OpenVPN UDP (or TCP). Choose a server location and click Download. Extract the `.ovpn` file — you will also need the Service Credentials (Username/Password) from your dashboard, which differ from your normal login credentials.

**Step 2: Set up Proton VPN on the Router**

Connect to the TL-WR1502X via Wi-Fi or Ethernet and open:

```
http://192.168.1.1/webpages/index.html#/vpnClient
```

Go to Advanced → VPN Client → Enable. Under Server List, click Add. Set VPN Type to OpenVPN, give it a name (e.g., `ProtonVPN`), and upload the `.ovpn` file. Enter the OpenVPN credentials from your dashboard:

```
uname: I5nijajmI7JqvX6s
pwd:   cmvjTOo9Jzb9weqsBZBrTuQ3FLpJB0ou
```

- Remove the `auth-user-pass` line from the `.ovpn` file
- Enable VPN kill switch
- Save the profile and enable the connection
- Add devices

**Step 3: Add Custom NextDNS Servers**

Log in at NextDNS → Setup tab and note your assigned IPv4 addresses (e.g., `45.90.28.0` and `45.90.30.0`). In the router admin panel, go to Network → DHCP Server (or Internet → IPv4). Set Primary DNS and Secondary DNS to your NextDNS addresses. Save and reboot the router.

**Captive Portal (e.g., HWPL)**

Turn off VPN to connect through captive portal authenticators, then navigate to:

```
http://neverssl.com
```

---

### NextDNS and ProtonVPN on Linux

Configure system DNS to use NextDNS IPv4/IPv6 addresses while ProtonVPN handles encryption. May not work with captive portals.

**Step 1: Get Your NextDNS IP Addresses**

Log in to the NextDNS Dashboard → Setup tab. Note:

```
IPv4: 45.90.28.54, 45.90.30.54
IPv6: 2a07:a8c0::bb:2878, 2a07:a8c1::bb:2878
```

**Step 2: Configure Ubuntu Network Settings**

Open Settings → Network (or Wi-Fi) → gear icon → IPv4 tab → DNS → Manual. Enter your NextDNS IPv4 address and click Apply. Repeat in the IPv6 tab with the IPv6 address.

**Install ProtonVPN:**

```bash
wget https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.8_all.deb
sudo apt update
sudo dpkg -i ./protonvpn-stable-release_1.0.8_all.deb && sudo apt update
sudo apt install proton-vpn-gnome-desktop
```

See also: <https://protonvpn.com/support/official-linux-vpn-ubuntu>

**Step 3: Configure ProtonVPN**

Open the ProtonVPN GUI → Settings → Connection:
- Turn **NetShield Ad-blocker OFF** (incompatible with custom DNS)
- Under Custom DNS, toggle ON and add: `45.90.28.54`, `45.90.30.54`
- Click Save, then connect to a VPN server.

**Step 4: Verify**

Disconnect and reconnect to apply changes, then confirm in a browser:

```
https://test.nextdns.io/
https://ip.me/
```

---

### Thunderbird

Sign in using Google mail and password for Google.

### Enable/Disable touchpad

```bash
xinput list   # note number N of touchpad
xinput disable <N>
xinput enable <N>
```

Add a bash shortcut:

```bash
nano .inputrc  # add alias
```
