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
- **Encryption:** Choose the **Encryption** option (LUKS) at the appropriate place during disk/partition setup to enable disk encryption.

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

> **Hardware Recommendation:** Installing KDE Plasma is recommended for **powerful PCs only** (such as Minisforum Venus or systems with ample RAM). Specifically, do **NOT** install Plasma on lower-spec machines like Lenovo 4 GiB RAM laptops—stick with the default lightweight LXQt desktop on those to avoid memory exhaustion and system slowdowns.

Install KDE Plasma to add a Wayland session option (powerful PCs only):

```bash
sudo apt update
sudo apt install -y plasma-desktop
```

> **Login selection:** At the SDDM / login screen, click the session/gear menu icon in the bottom or top bar and choose **Plasma (Wayland)**.
> 
> **Lubuntu-style menu:** To keep the familiar Lubuntu/LXQt menu feel inside Plasma, right-click the Application Launcher ("Start" icon) on the panel, choose **Show Alternatives...**, and select **Application Menu** (traditional cascading categories).
>
> *For detailed migration instructions from GDM/X11, SDDM Wayland configuration, and Wayland CLI display tools, see [INSTALL_Lubuntu_Plasma](INSTALL_Lubuntu_Plasma.md).*


### Sleep & Wake Configuration for Ryzen Mini PC (Minisforum Venus / rEFInd):
  
Minisforum UM773 (AMD Ryzen 7 7735HS) firmware implements traditional ACPI S3 sleep (`supports S0 S3 S4 S5`) and lacks ACPI Low-Power S0 Idle (`LPS0` / Modern Standby). Using `s2idle` can cause failed wakes, unresponsiveness, and `amdgpu` warnings. Additionally, AMD Rembrandt / Radeon 680M integrated graphics can experience Display Core timing generator timeouts (`optc31_disable_crtc line:145`) when resuming displays on HDMI.

Configure traditional deep S3 sleep and the AMD Display Core debug mask:

```bash
# Edit refind_linux.conf and append mem_sleep_default=deep amdgpu.dcdebugmask=0x10 to the option strings:
sudo nano /boot/refind_linux.conf
#    "Boot with standard options"  "root=UUID=7ea0e489-a564-4f95-b0e0-6a65e95b104e ro quiet splash vt.handoff=7 mem_sleep_default=deep amdgpu.dcdebugmask=0x10"
#    "Boot to single-user mode"    "root=UUID=7ea0e489-a564-4f95-b0e0-6a65e95b104e ro quiet splash vt.handoff=7 mem_sleep_default=deep amdgpu.dcdebugmask=0x10 single"
#    "Boot with minimal options"   "ro root=/dev/nvme0n1p5"
#  (No need to run update-grub for rEFInd; it reads this file dynamically on every boot).

# Test deep sleep state now:
echo deep | sudo tee /sys/power/mem_sleep
cat /sys/power/mem_sleep
# should say: s2idle [deep]
```

> **Note on Bluetooth Keyboards:** Bluetooth devices (such as Logitech Pebble K380s) have wakeup disabled in the kernel by default and cannot wake the system from suspend. Use a wired/wireless USB mouse or the physical power button to wake the PC.

Enable USB Wakeup for Your Mouse (Optional valid if install refind):

To allow waking the PC by clicking your USB mouse from sleep, both the USB root hubs (so the wake signal travels upstream to the host controller) and the mouse itself must have wakeup enabled.

Create `/etc/udev/rules.d/90-usb-wakeup.rules`:
```bash
sudo nano /etc/udev/rules.d/90-usb-wakeup.rules
```

Add the following rules:
```udev
# 1. Enable wakeup on USB root hubs (1d6b is Linux Foundation root hub) so wake signals pass upstream
ACTION=="add|bind|change", SUBSYSTEM=="usb", ATTR{idVendor}=="1d6b", ATTR{power/wakeup}="enabled"

# 2. Enable wakeup for the Lenovo Optical Mouse (adjust idVendor/idProduct if using a different mouse)
ACTION=="add|bind|change", SUBSYSTEM=="usb", ATTRS{idVendor}=="17ef", ATTRS{idProduct}=="602e", ATTR{power/wakeup}="enabled"
```

Reload and trigger udev, then verify:
```bash
# Reload and trigger udev rules
sudo udevadm control --reload && sudo udevadm trigger --action=add --subsystem-match=usb

# Verify wakeup is enabled (both should output: enabled)
cat /sys/bus/usb/devices/5-1/power/wakeup
cat /sys/bus/usb/devices/usb5/power/wakeup
```


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

### Lubuntu Secure (`systemd-homed` Encrypted Home)

> [!NOTE]
> This section is **only for migrating an already-built user folder to encryption**. If you selected the **Encryption** option during the initial install, disk encryption is already built-in at install and you should skip this section.

When `/home/daveg` is managed as a `systemd-homed` encrypted BTRFS loopback container (`/home/daveg.home`), `systemd-homed` defaults to `shrink-and-grow` resize mode, which attempts to shrink the BTRFS filesystem and relocate tens of thousands of extents on every logout/shutdown—causing shutdown to hang or spin indefinitely.

Disable auto-shrinking on shutdown by setting resize mode to `grow` only:

```bash
sudo homectl update daveg --auto-resize-mode=grow
```

*(To reclaim free space back to `/` on demand without shrinking the container, use `~/Documents/GitHub/myLinux/scripts/clean_root.sh` which runs `fstrim`.)*

To show `systemd-homed` users (UIDs `60001`–`60513`) on the SDDM login screen without exposing the system `nobody` account (UID `65534`), edit `/etc/sddm.conf`:

```bash
sudo nano /etc/sddm.conf
```

Add or update the `[Users]` section:

```ini
[Users]
MinimumUid=1000
MaximumUid=60513
HideUsers=nobody
```

Once `daveg` is verified to have working `sudo` access (`groups daveg` and `sudo -v`), remove any temporary setup account (such as `tempadmin`) so it does not leave background sessions hanging at shutdown:

```bash
sudo loginctl terminate-user tempadmin
sudo deluser --remove-home tempadmin
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
# NOTE: Do NOT install dhcpcd5 on Lubuntu (conflicts with NetworkManager and causes Wi-Fi drops)
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

### Chrome tweaks:
See [INSTALL_chrome](INSTALL_chrome.md) for hardware acceleration and secure DNS settings.


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

See [INSTALL_visual_studio](INSTALL_visual_studio.md) for Visual Studio Code installation, Particle Workbench setup, extensions, and USB permissions.


### Antigravity (gemini-cli)
See [INSTALL_Antigravity](INSTALL_Antigravity.md) for CLI install, VS Code/PyCharm integration, and YOLO configuration.

### Claude Code
See [INSTALL_claude_code](INSTALL_claude_code.md) for CLI installation and Anthropic authentication.
 
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

See [INSTALL_Arduino](INSTALL_Arduino.md) for Arduino IDE installation, SAMD board managers, collision libraries, and dark theme setup.

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

## 9. Auto Suspend Scheduling (sleep for standalone screencast machine that is used for nothing else)

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

### veracrypt
```bash
sudo add-apt-repository ppa:unit193/encryption -y
sudo apt update
sudo apt install veracrypt -y
```

### Bluetooth GUI

Lubuntu → System → Discover → search "bluetooth" → install "Bluetooth Manager"

### Chrome Browser

See [INSTALL_chrome](INSTALL_chrome.md) for Google Chrome installation, deb package setup, uninstallation, and hardware acceleration/DNS tweaks.


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


### Docker for DNS (i.e. piHole)

See [INSTALL_pihole](INSTALL_pihole.md) for installing Docker, disabling `systemd-resolved` DNS stub listener, and deploying Pi-hole via docker-compose.

---

## 14. GPU Screen Recorder (Wayland Screencasting)

See [INSTALL_gpu_screen_recorder](INSTALL_gpu_screen_recorder.md) for GPU Screen Recorder installation (Flatpak/native), VA-API hardware acceleration, and Wayland KMS/portal configuration.

---

## 15. Moving from GNOME / X to Plasma / Wayland
See [INSTALL_Lubuntu_Plasma](INSTALL_Lubuntu_Plasma.md) for full instructions on migrating to KDE Plasma on Wayland, SDDM configuration, and display management.

---

## 16. Chrome Remote Desktop
See [INSTALL_Chrome_Remote_Desktop](INSTALL_Chrome_Remote_Desktop.md) for Rclone setup.

---

## 17. noMachine Desktop Share
See [INSTALL_noMachine](INSTALL_noMachine.md) for Rclone setup.

---

## 18. Security Camera (motion / motionEye)
See [INSTALL_secure_cam](INSTALL_secure_cam.md) for security camera setup, motion detection, and motionEye web NVR interface.

---

## 19. zoxide

See [INSTALL_zoxide](INSTALL_zoxide.md) for zoxide smart directory navigation setup, shell integration, and training.

---

## 20. Work In Progress


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

---

## Linux Environment Post-Installation Configurations

To standardize environment configurations (such as global shell modifications, text editors, custom tools, and profile settings) across low-spec and primary Linux environments, sync this machine with the unified configuration manager:

1. Refer to the target environment documentation details in [myLinux Configuration Guide](../myLinux/README.md).
2. Execute the initialization process script directly:
   ```bash
   ~/Documents/GitHub/myLinux/scripts/bootstrap.sh
   ```

---

## Lessons Learned & Gotchas

### 1. Do NOT Install `dhcpcd5` alongside NetworkManager
* **Issue:** Installing `dhcpcd5` (`sudo apt install -y dhcpcd5`) runs `dhcpcd.service` in parallel with `NetworkManager`. Both daemons fight over the Wi-Fi/Ethernet interface, assign competing IP addresses, and cause `dhcpcd` to repeatedly delete and re-add the default gateway (`deleting default route via <gateway>`). This manifests as intermittent internet and DNS drops.
* **Fix:** Remove `dhcpcd5` from the install workflow. On an affected system, disable and purge it:
  ```bash
  sudo systemctl stop dhcpcd
  sudo systemctl disable dhcpcd
  sudo apt purge -y dhcpcd5 dhcpcd
  ```

### 2. Disable Wi-Fi Power Saving on Intel Wireless (e.g., AC-9560 / `iwlwifi`)
* **Issue:** Default power saving (`wifi.powersave = 3`) causes periodic high latency spikes, packet loss, or beacon dropouts on certain Intel and Realtek wireless chipsets.
* **Fix:** Set power saving to disabled (`2`):
  ```bash
  sudo sed -i 's/wifi.powersave = 3/wifi.powersave = 2/' /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
  sudo systemctl restart NetworkManager
  ```

### 3. Clean Up Duplicate Wi-Fi Profiles
* **Issue:** Multiple profiles for the same SSID (with autoconnect enabled) can cause tray applets (like `nm-tray`) to trigger unnecessary re-association (`disconnecting for new activation request`).
* **Fix:** List and delete redundant profiles:
  ```bash
  nmcli connection show
  sudo nmcli connection delete <OLD_OR_DUPLICATE_UUID>
  ```


