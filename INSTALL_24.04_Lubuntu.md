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
- [14. GPU Screen Recorder (Wayland Screencasting)](#14-gpu-screen-recorder-wayland-screencasting)
- [15. Moving from GNOME / X to Plasma / Wayland](#15-moving-from-gnome--x-to-plasma--wayland)
- [16. Work In Progress](#16-work-in-progress)

---

## 1. Boot and Install

Insert ISO USB and boot:
- **F12** on Lenovo (rapid), **F10** on HP-Omen, **F7** on little_guy
- Set boot order to USB

Choose **"Normal installation"** (not minimal — minimal leaves things broken).

Setup and choose a single large partition.  Installer will make a swap dynamically.

Restart will prompt to remove USB. System should restart to Lubuntu without BIOS boot.

After restart:
- Install Updates and reboot
- Install drivers (none may be available on Lenovo)

```bash
sudo apt update
sudo apt install refind   # accept all the dangerous-looking options e.g. autoinstall? select Yes
sudo nano /boot/efi/EFI/refind/refind.conf
  # enable_mouse  ********uncomment this line
```

This installs the rEFInd boot manager to make the EFI boot menu work properly with dual boot and wireless keyboard.

---

## 2. Initial Setup

### Desktop Setup (Wayland Session for Screencasting & Windows Dual Boot)

Lubuntu 24.04 ships by default with LXQt on X11. However, if dual-booting with Windows and performing screencasting/screen recording (e.g., using GPU Screen Recorder or PipeWire), a **Wayland** session is needed for modern capture protocols and display handling.

Install KDE Plasma to add a Wayland session option:

```bash
sudo apt update
sudo apt install -y plasma-desktop
```

> **Login selection:** At the SDDM / login screen, click the session/gear menu icon in the bottom or top bar and choose **Plasma (Wayland)**.
> 
> **Lubuntu-style menu:** To keep the familiar Lubuntu/LXQt menu feel inside Plasma, right-click the Application Launcher ("Start" icon) on the panel, choose **Show Alternatives...**, and select **Application Menu** (traditional cascading categories).
>
> *For detailed migration instructions from GDM/X11, SDDM Wayland configuration, and Wayland CLI display tools, see [15. Moving from GNOME / X to Plasma / Wayland](#15-moving-from-gnome--x-to-plasma--wayland).*

### Turn off light Perixx 317 keyboard

```bash
xmodmap -e "add mod3 = Scroll_Lock"
```

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

System - Discover - caffeine, vlc
**From System - Discover menu:**
- `caffeine` (the one with steam rising)
- `vlc` (open and turn off hardware acceleration)
- `audacity`
- `gnucash`
- `snapper`


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
sudo apt install xsel
sudo apt install -y pavucontrol        # for myPyScreencast
sudo apt install -y thunar
sudo apt install -y nautilus
pavucontrol  # defaults to low volume — set to 100% for screencasting.
```

Lubuntu installs by default: LibreOffice, Firefox
accelerated decoding - save


### xscreensaver
nano ~/.config/lxqt/lxqt.conf
[Screensaver]
lock_command=env XSECURELOCK_SAVER=blank xsecurelock

Configure the Idle Timeout Trigger (xautolock)
	- Go to LXQt Application Menu ➔ Preferences ➔ LXQt Settings ➔ Session Settings. 
	- Click on the Autostart tab on the left. 

Locate and uncheck the default XScreenSaver if it is running to avoid execution conflicts. 
	- Click the Add button to register xsecurelock for timeout management:
		Name: XSecureLock Timeout Manager
		Command: xautolock -time 20 -locker "env XSECURELOCK_COMPOSITE_OBSCURER=0 XSECURELOCK_SAVER=saver_xscreensaver xsecurelock" (Replace 20 with your preferred idle timeout limit in minutes). 
	- Click OK and then Close. 
Run the following to make sure background gets loaded
env XSECURELOCK_SAVER=saver_xscreensaver xsecurelock

Adjust LXQt Power Management Settings
To keep LXQt's internal power profiles from colliding with xsecurelock on an idle trigger: 
	- Navigate to LXQt Application Menu ➔ Preferences ➔ LXQt Settings ➔ Power Management. 
	- Under the Idleness tab, make sure the "Turn off monitor after" time is set to a value higher than your xautolock time, or disabled entirely. (I set turn off monitor after 25:00)
	- Under the Locks section, verify whether "Lock screen when idle" is managed by your new command. 

Log out of your Lubuntu session and log back in to apply the configuration.


### Firefox Security Exceptions
Add exceptions for: `hulu.com`, `amazon.com`, `play.max.com`, `netflix.com`

###Firefox tweaks (`about:config`):
```
layers.acceleration.force-enabled = true
gfx.webrender.all = true
browser.sessionstore.interval = 150000
```
- Open Settings → search for `DNS` → under **DNS over HTTPS**, select **Off** (Use your default DNS resolver) — prevents Firefox from bypassing network DNS / Pi-hole.

###Chrome tweaks (`chrome://settings/system`):
- Toggle on hardware acceleration → Relaunch
- Open Settings (`chrome://settings/security`) → search for `DNS` → toggle **Use secure DNS** to **Off** — prevents Chrome from bypassing network DNS / Pi-hole.


Use System - Discover to install these fine tools:
    vlc, 

### VLC
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

> **Do NOT use `snap install code --classic`** — sandboxes VS Code and breaks Particle build tools.

```bash
snap install code --classic
sudo apt install libarchive-zip-perl   # fixes missing crc32 for Particle Workbench
```

Start Code and install extensions.
Sign into Particle ASAP.


### Antigravity (gemini-cli)
See [INSTALL_Antigravity](INSTALL_Antigravity.md) for CLI install, VS Code/PyCharm integration, and YOLO configuration.
 
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
ifconfig  # copy ip string for inet from wlp2s0  e.g. 192.168.5.205  (http://192.168.5.205:8096/web/#/home.html)
# answer jellyfin_..._pkg by cut and paste from previous
# Remove:
flatpak remove com.github.iwalton3.jellyfin-media-player
```
Install server
```bash
curl -s https://repo.jellyfin.org/install-debuntu.sh | sudo bash
sudo usermod -a -G daveg jellyfin
# Visit http://localhost:8096
sudo chown -R jellyfin /media/daveg
```
Start
Browse to Start bookmarks in Firefox and visit Jellyfin
User is Jellyfin


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

### Python Projects (pyStateOfCharge, movie_Scraper, myPyScreencast)

See [INSTALL_Python_Projects](INSTALL_Python_Projects.md) for full project notes, venv setup, and dependencies.

---

## 5. Serial / USB Setup

See [INSTALL_PuTTY](INSTALL_PuTTY.md) for PuTTY installation, permissions, and serial configuration.

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

See [INSTALL_Alternate_Python](INSTALL_Alternate_Python.md) for installing build dependencies and compiling Python from source (e.g. Python 3.11.9).

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

> The 4 GB Lenovo laptops don't have enough CPU bandwidth to run ffmpeg even at low quality — skip screencasting. For Wayland sessions or hardware-accelerated screencasting, see [14. GPU Screen Recorder](#14-gpu-screen-recorder-wayland-screencasting).

---

## 9. Auto Suspend Scheduling (sleep)

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

See [INSTALL_Google_Drive_Rclone](INSTALL_Google_Drive_Rclone.md) for Rclone setup, mounting, and autostart.
See [INSTALL_Google_Drive_Backup](INSTALL_Google_Drive_Backup.md) for optimized rclone copy and sync commands.

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

### Add support for keypress in various pyCharm projects

Add a udev rule (permanent fix):
This is the recommended approach. A udev rule automatically sets the correct permissions when the device node is created during system boot.
Create a new rules file, for example, /etc/udev/rules.d/99-uinput.rules:

```bash
sudo nano /etc/udev/rules.d/99-uinput.rules
```
Add one of the following lines to the file. The first option adds your user to the input group, which is more secure than MODE="0666":

Option A (Recommended):
KERNEL=="uinput", SUBSYSTEM=="misc", OPTIONS+="static_node=uinput", GROUP="input", MODE="0660"

Option B (Less secure, grants access to everyone):
KERNEL=="uinput", MODE="0666"

Apply the changes:
Reload the udev rules:
```bash
sudo udevadm control --reload-rules
```
Trigger the rules to be applied immediately:
```bash
sudo udevadm trigger
```

Add your user to the input group (only for Option A above):
```bash
sudo usermod -a -G input $USER
```

Reboot your system for the group membership change to take effect. 
After following these steps, your pythons scripts should be able to open /dev/uinput for writing without sudo (evdev python >= v3.12).


### Reliable WiFi (DNS Fix)

If WiFi drops or DNS resolution fails (especially with competing hotspots):

```bash
sudo nano /etc/systemd/resolved.conf
# Add:
DNS=8.8.8.8 8.8.4.4
FallbackDNS=1.1.1.1 1.0.0.1
```

This ensures DNS works globally regardless of what NetworkManager does per-interface.

### Docker for DNS
```bash
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo nano /etc/systemd/resolved.conf
# Un-comment or add the following line under the [Resolve] section:
textDNSStubListener=no

sudo systemctl restart systemd-resolved

mkdir -p ~/pihole
cd ~/pihole
nano docker-compose.yml

version: "3"

services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80/tcp"
    environment:
      TZ: 'America/New_York'
      FTLCONF_webserver_api_password: 'YourSecurePasswordHere'
      FTLCONF_dns_listeningMode: 'all'
    # Volumes persist your adlists and settings across container updates
    volumes:
      - './etc-pihole:/etc/pihole'
      - './etc-dnsmasq.d:/etc/dnsmasq.d'
    cap_add:
      - NET_ADMIN
    restart: unless-stopped

# start in background
docker compose up -d

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

sudo nano /etc/systemd/resolved.conf
DNSStubListener=no

sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
sudo systemctl restart systemd-resolved
cd ~/pihole
docker compose up -d

# Accessing the DashboardFind your Linux machine's local IP address by running hostname -I in the terminal.Open your web browser and navigate to: http://192.168.5.216/admin.  Log in using the password you set in the docker-compose.yml file.

# fix not found
cd ~/pihole
nano docker-compose.yml
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8080:80/tcp"  # <-- Changed host port from 80 to 8080

docker compose up -d --force-recreate
http://192.168.5.216:8080/admin/login

# set dns to 192.168.5.216

# make the IP static in router setup

# Turn off advanced DNS in browsers.  See 'Firefox Tweaks' and 'Chrome Tweaks'
```

---

## 14. GPU Screen Recorder (Wayland Screencasting)

Traditional screencasters (such as `ffmpeg` using `x11grab` or SimpleScreenRecorder) only work on X11 and can cause high CPU utilization on low-power processors. Under Wayland, standard X11 capture fails.

[GPU Screen Recorder](https://git.dec05eba.com/gpu-screen-recorder) captures directly from the GPU framebuffer via KMS (Direct Rendering Manager) or PipeWire desktop portal and encodes video with hardware acceleration (VA-API on AMD/Intel, NVENC on NVIDIA). This allows smooth 60 FPS recording with negligible CPU overhead.

### Prerequisites

1. **Hardware Video Acceleration Drivers (VA-API):**
   Ensure Mesa VA-API drivers are installed for AMD or Intel GPUs:
   ```bash
   sudo apt update
   sudo apt install -y mesa-va-drivers vainfo
   vainfo   # verify driver reports VAProfileH264 / VAProfileHEVC support
   ```

2. **Audio Monitoring:**
   ```bash
   sudo apt install -y pavucontrol
   ```

### Option A: Install via Flatpak (Recommended — includes GUI)

Lubuntu requires `flatpak` to be installed and Flathub configured:

```bash
sudo apt update
sudo apt install -y flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

Install GPU Screen Recorder system-wide (allows acquiring Polkit capture permissions):

```bash
flatpak install flathub com.dec05eba.gpu_screen_recorder
```

**Launch:**
- Open **GPU Screen Recorder** from the LXQt Application Menu, or
- Run in terminal:
  ```bash
  flatpak run com.dec05eba.gpu_screen_recorder
  ```

### Option B: Build from Source (Native CLI)

```bash
sudo apt update
sudo apt install -y build-essential git meson ffmpeg \
    libxi-dev libdrm-dev libavcodec-dev libavformat-dev \
    libx11-dev libxcomposite-dev libxdamage-dev libxrender-dev \
    libxrandr-dev libpulse-dev libva-dev libcap-dev \
    libdbus-1-dev libpipewire-0.3-dev libavfilter-dev

git clone https://repo.dec05eba.com/gpu-screen-recorder
cd gpu-screen-recorder
sudo ./install_ubuntu.sh
```

### Usage & Wayland Notes

- **Encoder Selection:** Set Video Codec to **VAAPI** (or **Auto**) for AMD Radeon / Intel, or **NVENC** for NVIDIA.
- **Wayland Permissions (KMS Capture):** On startup under Wayland, GPU Screen Recorder prompts for root authentication (`pkexec` / Polkit) to capture directly from KMS for maximum performance and zero frame drops.
- **CLI Recording Example:**
  ```bash
  # Record full screen at 60 FPS with default system audio output:
  gpu-screen-recorder -w screen -f 60 -a "default_output" -o ~/Videos/screencast.mp4

  # Stop recording cleanly:
  # Press Ctrl + C in the terminal
  ```

---

## 15. Moving from GNOME / X to Plasma / Wayland

Migrating from GNOME or LXQt under X11 to KDE Plasma on Wayland provides modern display protocol benefits, tear-free rendering, smoother scaling, and native hardware-accelerated screencasting (via KMS and PipeWire).

### 1. Install Plasma & Wayland Packages

Install the KDE Plasma desktop, Wayland session compositor integration, SDDM configuration modules, and Wayland clipboard utilities:

```bash
sudo apt update
sudo apt install -y plasma-desktop plasma-workspace-wayland
sudo apt install -y kde-config-sddm sddm-kcm
sudo apt install -y wl-clipboard  # replaces xclip / xsel for terminal clipboard (wl-copy, wl-paste)
```

### 2. Configure SDDM for Wayland

Switch the default display manager from GDM3 to SDDM, and configure SDDM to run natively on Wayland rather than launching an X11 server for the login greeter:

```bash
# Set SDDM as the system default display manager:
sudo dpkg-reconfigure sddm
# Select 'sddm' when prompted

# Disable gdm3 to prevent dual display manager service conflicts:
sudo systemctl disable gdm3

# Create SDDM Wayland drop-in configuration:
sudo mkdir -p /etc/sddm.conf.d
sudo nano /etc/sddm.conf.d/10-wayland.conf
```

Add the following configuration:
```ini
[General]
DisplayServer=wayland
GreeterEnvironment=QT_WAYLAND_SHELL_INTEGRATION=layer-shell

[Wayland]
CompositorCommand=kwin_wayland --no-lockscreen
```

Restart SDDM (or reboot) to load the Wayland greeter:
```bash
sudo systemctl restart sddm
# Or reboot:
sudo reboot
```

*(Optional)* Configure automatic login to Plasma Wayland:
```bash
sudo nano /etc/sddm.conf
```
```ini
[Autologin]
User=daveg
Session=plasmawayland
```

### 3. Display Management & HDMI Reset (`kscreen-doctor` vs `xrandr`)

Under X11, `xrandr` was used to wake up or cycle modes on HDMI displays:
```bash
# X11 old method (does NOT change native modes under Wayland):
DISPLAY=:0 xrandr --output HDMI-A-1 --mode 1024x768; sleep 1; DISPLAY=:0 xrandr --output HDMI-A-1 --auto
```

Under Wayland, `xrandr` only affects Xwayland client surfaces. Use KDE's CLI display tool **`kscreen-doctor`**:

```bash
# List all connected outputs and available mode numbers/resolutions:
kscreen-doctor -o

# Force display cycle / mode re-sync on HDMI-A-1:
kscreen-doctor output.HDMI-A-1.mode.1024x768@60; sleep 1; kscreen-doctor output.HDMI-A-1.mode.auto
```

#### Reconfiguring KScreen & Restarting Plasma Shell (without reboot)
If the desktop shell or display daemon needs a reload:
```bash
# Restart Plasma Shell:
systemctl --user restart plasma-plasmashell.service

# Trigger KScreen reconfigure via D-Bus:
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
qdbus org.kde.kded5 /kded org.kde.kded5.loadModule kscreen
SSH_AUTH_SOCK="" qdbus org.kde.KScreen /org/kde/KScreen reconfigure
```

### 4. Wayland-Native Screen Recording

Legacy X11 grab tools (`ffmpeg -f x11grab`, `SimpleScreenRecorder`) fail under Wayland. Use Wayland-native recorders:

```bash
# GPU Screen Recorder (recommended for hardware VA-API / NVENC capture):
sudo apt install -y gpu-screen-recorder
# Or install via Flatpak:
flatpak install flathub com.dec05eba.gpu_screen_recorder

# wf-recorder (lightweight CLI recorder for Wayland/PipeWire):
sudo apt install -y wf-recorder
```
*See [14. GPU Screen Recorder](#14-gpu-screen-recorder-wayland-screencasting) for detailed setup and usage.*

### 5. Session Verification & Environment Variables

Verify your running session:
```bash
echo $XDG_SESSION_TYPE       # Should return 'wayland'
echo $WAYLAND_DISPLAY        # Usually 'wayland-0'
echo $XDG_CURRENT_DESKTOP    # Should return 'KDE'
ls /run/user/$(id -u) | grep wayland
```

To ensure Qt and GTK applications prefer native Wayland rather than falling back to Xwayland, ensure the following are set in `~/.bashrc` or `/etc/environment`:
```bash
export QT_QPA_PLATFORM="wayland;xcb"
export GDK_BACKEND="wayland,x11"
export MOZ_ENABLE_WAYLAND=1
```

### 6. Power Management, Screen Locking & Shortcuts

- **Screen Locking:** Replace X11-dependent tools (`xsecurelock`, `xautolock`, `xscreensaver`) with Plasma's native screen lock. Configure in **System Settings → Screen Locking** (`kscreenlocker`).
- **Keyboard Mappings:** `xmodmap` does not affect native Wayland applications. For custom keys (such as backlight toggle on Scroll Lock), configure shortcuts via **System Settings → Shortcuts** or create `udev` / `hwdb` rules.
- **Session Cleanup:**
  ```bash
  # Terminate any lingering user session when switching managers:
  sudo loginctl terminate-user $USER
  ```

---

## 16. Work In Progress

### Chrome Remote Desktop
See [INSTALL_Chrome_Remote_Desktop](INSTALL_Chrome_Remote_Desktop.md) for Rclone setup.

### noMachine Desktop Share
See [INSTALL_noMachine](INSTALL_noMachine.md) for Rclone setup.

### zoxide (https://www.howtogeek.com/stop-using-the-cd-command/)
sudo apt update
#sudo pacman -S zoxide # for users on Arch and its derivatives
sudo apt install zoxide # for users on Ubuntu, Debian, and their derivatives
echo 'eval "$(zoxide init bash)"' >> ~/.bashrc # adds eval "(zoxide init bash)" to your ~/.bashrc file
source ~/.bashrc # reloads the Bash configuration

# train it
zoxide add ~/Documents/"How to Geek"/Articles
zoxide add ~/Documents/Forbes/Articles
zoxide add ~/Projects ~/Documents ~/Downloads # add multiple directories


### Improved HandBrake (Encrypted DVD Ripping)

HandBrake does not include native DVD decryption (`libdvdcss`) out of the box due to licensing and legal restrictions. To rip encrypted/CSS-protected DVDs on Ubuntu:

#### 1. Install and Compile `libdvdcss` (this was already in place for Lubuntu)

Install the official package wrapper that downloads and builds `libdvdcss`:

```bash
# Update package index and install the automated DVD packaging tool
sudo apt update
sudo apt install -y libdvd-pkg

# Trigger automatic download, compilation, and installation of libdvdcss
sudo dpkg-reconfigure libdvd-pkg
```

> **Note:** During `dpkg-reconfigure`, a terminal dialog will prompt to confirm building the library. Select **Yes** and press Enter.

#### 2. Install Native (APT) HandBrake (this was already in place for Lubuntu)

The Snap version runs inside a strict sandbox container and cannot access `/usr/lib` where `libdvdcss` resides. Replace it with the native APT package:

```bash
# Remove restricted Snap version
sudo snap remove handbrake

# Install native system package
sudo apt install -y handbrake
```

#### 3. "VLC Cache Trick" for Stubborn Discs

Some DVDs use complex structural protections (such as fake playlists or 99-title traps) that hang the scanner. If HandBrake fails or hangs during the initial title scan:
1. Open VLC Media Player.
2. Play the encrypted DVD for 5–10 seconds (VLC cracks the handshake and loads the key into volatile memory cache).
3. Pause playback, leave VLC open, and open/scan the disc in HandBrake.

#### 4. Power-User Fallback: MakeMKV + HandBrake

If encountering stubborn DVDs with structural protections that `libdvdcss` cannot crack:
1. Use **MakeMKV** to decrypt the disc and extract a lossless 1:1 rip (`.mkv`) to the hard drive.
2. Open the `.mkv` file in **HandBrake** to transcode and compress to your preferred format and size.

```bash
sudo add-apt-repository ppa:heyarje/makemkv-beta
sudo apt update
sudo apt install makemkv-bin makemkv-oss -y
```

Launch:
```bash
makemkv
```


### end works in progress

