# Installing Lubuntu 22.04 LTS with NVIDIA Drivers (PLEX Server)

**Hardware:** HP Omen 15" 2022
**OS:** Lubuntu 22.04 LTS (LXQt desktop, X11/Xorg)
**Purpose:** General workstation + Plex Media Server

> Lubuntu is Ubuntu-based. It lacks `snapd` by default — install it first.
> PyCharm Community did not work from the default install; see the snap install steps below.
> **When in doubt, use instructions for Ubuntu.**
>
> **Critical:** swapfile must be ≥ 6 GB (prefer 8 GB) when RAM is only 4 GB.
> Set `vm.swappiness=10` (from 60) for better mouse responsiveness.

---

## Table of Contents

- [1. Preparation](#1-preparation)
- [2. Boot and Install](#2-boot-and-install)
- [3. WiFi and Drivers](#3-wifi-and-drivers)
- [4. Initial Setup](#4-initial-setup)
- [5. GitHub Desktop](#5-github-desktop)
- [6. Install Applications](#6-install-applications)
- [7. Sound Configuration](#7-sound-configuration)
- [8. YouTube Downloader (ClipGrab)](#8-youtube-downloader-clipgrab)
- [9. Development Setup](#9-development-setup)
- [10. Cleanup](#10-cleanup)
- [11. Plex Media Server](#11-plex-media-server)
- [12. Samba File Sharing](#12-samba-file-sharing)
- [13. Fixes and Troubleshooting](#13-fixes-and-troubleshooting)
- [14. Performance Tuning](#14-performance-tuning)
- [15. Lessons Learned](#15-lessons-learned)

---

## 1. Preparation

- Phone ready to approve Google requests and USB tethering if needed
- Make space for Linux — note partition numbers
- Have a >4 GB thumbdrive
- On Windows: download the ISO and flash using **balenaEtcher**
- Turn off BitLocker on all drives
- Deauthorize tools like DVDfab, WinXDVD, ePubor (in case you can't get back)
- Unplug second monitor and extra USB devices (may leave mouse and keyboard)

---

## 2. Boot and Install

Insert the ISO USB drive and boot:
- **F10** on HP-Omen, **F12** on Lenovo, **ESC** on HP-Phoenix, **F7** on little_guy
- Set boot order to USB

Choose **"Try or install Lubuntu"** — allow ~3 minutes to next step (may hear music).

During installation:
- **Fresh clean install** (normal, not minimal — minimal leaves things broken)
- **Encrypted** (LUKS) — the initial password becomes the LUKS key; start with your final password then temporarily shorten it for install
- Username: `daveg`
- When done, press Finish; it will prompt to remove the USB media and restart

---

## 3. WiFi and Drivers

After first boot (may come up without WiFi — connect Ethernet first):

**Preferences → Additional Drivers:**
- NVIDIA proprietary (tested)
- Broadcom STA wireless
- Apply → Close → Restart

**Sign into WiFi** (`ourHappyHome5G`), then add Google DNS:

```bash
sudo nano /etc/resolv.conf   # add to bottom:
nameserver 8.8.8.8
nameserver 8.8.8.4
```

Restart.

---

## 4. Initial Setup

```bash
sudo apt update && sudo apt upgrade
sudo apt install synaptic
sudo apt autoremove
```

Using Synaptic, install: `firefox`, `dos2unix`, `featherpad` — then restart.

Open Firefox:
- Sign in and pin BitWarden to toolbar
- Always show Bookmarks Bar
- Sign into Google

**Add plexmgr user:**
- Preferences → Users → Add `plexmgr` (same properties as `daveg`, main group `daveg`)

**BIOS scheduled power-on at 16:00 daily.** Then set cron to shut down:

```bash
sudo nano /etc/crontab
# Add:
22 30 * * * root /usr/sbin/shutdown -h now
01 00 * * * root /usr/sbin/shutdown -h now
```

---

## 5. GitHub Desktop

```bash
sudo wget https://github.com/shiftkey/desktop/releases/download/release-3.1.1-linux1/GitHubDesktop-linux-3.1.1-linux1.deb
sudo apt-get install -y gdebi-core
sudo gdebi GitHubDesktop-linux-3.1.1-linux1.deb
github
```

Sign in to GitHub.com (password in BitWarden). Use passkey — easiest.
If caught in an authorization loop, try URL clone instead.

Repeat if needed (also listed under ASAP):

```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
```

Using Synaptic install: `sqlitebrowser`, `brasero`, `caffeine`, `vlc` — restart.

---

## 6. Install Applications

```bash
sudo snap install plexmediaserver
sudo apt install -y fuse libfuse2          # AppImage support
sudo apt install -y ffmpeg
sudo apt install -y git
sudo apt install --fix-missing -y python3-pip
sudo apt install -y python3-tk             # for PyCharm
sudo apt install -y dhcpcd5
sudo apt install LocalSend
sudo apt install xsel
sudo apt install -y pavucontrol            # for myPyScreencast
sudo snap install --classic pycharm-community
```

### VS Code

> **Do NOT use `snap install code --classic`** — the snap version sandboxes VS Code and breaks Particle build tools.

```bash
# Download the .deb from https://code.visualstudio.com/docs/?dv=linux64_deb
sudo apt install ./Downloads/code_*.deb
sudo apt install libarchive-zip-perl       # fixes missing crc32 for Particle Workbench
```

### VLC

Tools → Preferences → Codecs → **disable hardware-accelerated decoding** → Save. Restart VLC.

### kdenlive

Download flatpak from https://kdenlive.org/en/download/ and install.

---

## 7. Sound Configuration

```bash
sudo nano /etc/modules-load.d/modules.conf
# Add:
snd-aloop

# Load for this session:
sudo modprobe snd-aloop
```

Alternatively, plug in a USB headset and adjust sound settings in the GUI.

### Screencast audio setup

```bash
ffmpeg -sources pulse   # find the loopback source name
pactl list short sources
# Use: alsa_output.platform-snd_aloop.0.analog-stereo.monitor
```

Check ffmpeg capabilities:

```bash
ffmpeg -version | grep x11grab && ffmpeg -version | grep gpl && \
ffmpeg -version | grep libx264 && ffmpeg -version | grep libmp3lame
```

```bash
sudo snap install audacity   # optional, alongside pavucontrol
```

> **pavucontrol** defaults to low volume. Set output to 100% for screencasting to work.

---

## 8. YouTube Downloader (ClipGrab)

1. Download `yt-dlp` for Linux from https://github.com/yt-dlp/yt-dlp
2. Download ClipGrab from https://clipgrab.org/download-clipgrab/

```bash
cd Downloads
chmod a+x ClipGrab-3.9.10-x86_64.AppImage
./ClipGrab-3.9.10-x86_64.AppImage   # errors first time — press Continue (not Exit)
mv yt-dlp /home/daveg/.local/share/ClipGrab/ClipGrab/
```

Save the ClipGrab icon (blue circle) as `Downloads/ClipGrab.jpeg`, then create a desktop entry:

```bash
cat << EOF > /home/daveg/Desktop/ClipGrab.desktop
[Desktop Entry]
Name=ClipGrab
Exec=/home/daveg/Downloads/ClipGrab-3.9.10-x86_64.AppImage
Icon=/home/daveg/Downloads/ClipGrab.jpeg
comment=app
Type=Application
Terminal=false
Encoding=UTF-8
Categories=Utility;
EOF
```

Right-click → Allow Launching → Properties → Run as Program → Re-run.

```bash
sudo mv /home/daveg/Desktop/ClipGrab.desktop /usr/share/applications/
```

---

## 9. Development Setup

### PyCharm

- Setup venv for Python (can also be used in VS Code)
- Use local dictionary: Settings → Editor → Natural Languages → Spelling (uncheck "use single...")
- **Caution:** Use PyCharm to install Python interpreters — installing via `deb` made Ubuntu unbootable
- Choose local interpreter; run something to confirm packages: `numpy`, `matplotlib`, `reportlab`, `easygui`, `pyshortcuts`, `openai-whisper`, `configparser`
- May need to start PyCharm twice on first launch

### movie_Scraper

- Use its own `.venv`
- Search email for "License key of..." for PySimpleGUI key
- Set DB location to `/home/daveg/google-drive/Movies Stuff`
- Run `install.py` and follow instructions

### myPyScreencast

- Use its own `.venv`
- Open browser and play music on YouTube; insert headphones first
- Use `pavucontrol` to assign browser cast to LoopbackAnalogStereo (verifies it mutes speakers)
- Set pavucontrol volume to 100%

```bash
ffmpeg -f pulse -i alsa_output.platform-snd_aloop.0.analog-stereo.monitor \
  -t 12.0 -y "/home/daveg/Documents/Recordings/test1_raw.mp4"
```

---

## 10. Cleanup

```bash
sudo passwd daveg     # ignore warnings
sudo passwd           # root
rm ~/.local/share/keyrings/login.keyring
sudo apt autoremove
sudo apt autoclean
sudo apt clean
sudo apt install deborphan
sudo apt remove $(deborphan)
```

---

## 11. Plex Media Server

### Permissions

```bash
sudo usermod -a -G daveg plexmgr
# restart
sudo chown daveg /media/daveg
sudo chmod -R a+rwx /media/daveg
```

Set "Permissions for Enclosed Files":
- Owner: Create & Delete
- Group (daveg): Create & Delete
- Others: Create & Delete
- Files: Owner R&W, Group R&W, Other R
- Folders: Owner C&D, Group C&D, Other Access only

### Libraries

Add libraries in Plex:
- Movies: `/media/daveg/Lib/Movies`
- TV Shows: `/media/daveg/Lib/TV Shows`
- Other Videos: `/media/daveg/Lib/Videos`
- Add to TV Shows library: `/media/daveg/Videos/DVRcache`
- Switch each library tab from **Recommended** to **Library**

Settings → Transcoder:
- Deselect **Use hardware acceleration when available**
- Transcoder Temporary Directory: `/media/daveg/Videos/DVRcache`

After several hours of content loading, restart Plex to see content on other devices.

Mount the 3TB drive using Disks. *(TODO: document next steps)*

---

## 12. Samba File Sharing

```bash
sudo apt install -y samba samba-common-bin
sudo apt install net-tools
sudo apt install vino -y
sudo apt install -y xrdp
sudo systemctl enable xrdp
sudo apt install libarchive-zip-perl    # for Particle Workbench
sudo mkdir /Public
sudo chmod -R 0777 /Public
sudo smbpasswd -a plexmgr               # use same password as daveg
sudo ufw allow samba
```

Edit `/etc/samba/smb.conf` — add before `[printers]` section:

```ini
inherit permissions = yes
```

Add at bottom:

```ini
[Public]
comment = public share, no need to enter username and password
path = /Public/
browseable = yes
writable = yes
guest ok = yes
```

```bash
sudo systemctl start smbd nmbd
sudo service smbd restart && sudo service nmbd restart
sudo groupadd samba
sudo gpasswd -a plexmgr samba
sudo mkdir -p /srv/samba/private/
sudo setfacl -R -m "g:samba:rwx" /srv/samba/private/
testparm
sudo systemctl restart smbd nmbd
ifconfig   # note IP address
```

Make IP static via EERO phone app (reservation).

**Local access:**
```
smb://localhost
```

**Remote access:**
```
smb://192.168.4.21
```

---

## 13. Fixes and Troubleshooting

### gdm3 fails on restart / kauditd_printk_skb hang

Press **Ctrl+Alt+F5** for TTY login, then:

```bash
sudo apt install --reinstall ubuntu-session
reboot
```

### Wake from suspend

```bash
sudo kernelstub -a mem_sleep_default=deep
# restart
```

### PyCharm cannot find `/usr/local/bin`

Problem is with flatpak version. Uninstall and reinstall using snap:

```bash
sudo snap install --classic pycharm-community
```

### Missing Settings

```bash
sudo apt-get install -y ubuntu-desktop
```

### "gnome-control-center not found in path"

```bash
sudo apt install gnome-control-center
```

### Missing desktop icons

```bash
sudo apt-get install --reinstall ubuntu-desktop
# restart
```

### `/var/log` flooded with "HDY_IS_CAROUSEL_BOX (self) failed"

```bash
sudo nano /etc/xdg/autostart/io.elementary.appcenter-daemon.desktop
# Change X-GNOME-Autostart-Delay from 60 to 0
```

### AMD GPU kernel parameters

```bash
sudo kernelstub -a "amdgpu.ppfeaturemask=0xffffffff"
```

---

## 14. Performance Tuning

### Updates and Drivers

```bash
sudo apt update && sudo apt upgrade -y
# Use proprietary drivers where available
sudo apt install gparted synaptic
sudo apt install preload    # learns what to pre-start
```

### Timeshift Backup

```bash
sudo apt install timeshift
# Run timeshift: rsync, back up to USB drive formatted ext4
```

### Network Speed

- Turn off automatic DNS for WiFi network (IPv4 and IPv6)
- Set DNS to: `8.8.8.8, 8.8.4.4`
- Apply and restart WiFi

**Firefox tweaks** (`about:config`):
```
layers.acceleration.force-enabled = true
gfx.webrender.all = true
```

**Chrome tweaks** (`chrome://settings/system`):
- Toggle on "Use hardware acceleration when available" → Relaunch

### Firewall

```bash
sudo apt install gufw
# Open "Firewall Configuration" and turn on Status — that's it
```

### Cleanup

```bash
sudo apt install bleachbit
```

### NoMachine Remote Desktop

```bash
cd Downloads
sudo cp -p nomachine_9.0.188_11_x86_64.tar.gz /usr
cd /usr
sudo tar zxf nomachine_9.0.188_11_x86_64.tar.gz
sudo /usr/NX/nxserver --install
# Port: 4000 — allow through firewall (gufw)
```

### Bluetooth

```bash
sudo apt install blueman
```

### Zoom

```bash
cd ~/Downloads
sudo apt install gdebi
gdebi-gtk   # browse to and open the .deb file
```

### Disk Utility

```bash
sudo apt install gnome-disk-utility
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
sudo fallocate -l 8G /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
swapon --show
```

---

## 15. Lessons Learned

- **Do not interrupt** a command-line upgrade — it will break the system. Let it finish.
- **Never directly upgrade or delete** the shipped Python. Use `altinstall` make directive.
- **Always use a virtual environment** (`venv`) unique to each Python project for portability.
- `pavucontrol` defaults to low volume on outputs. Set to 100% for screencasting.
- Use `ffmpeg -sources pulse` (or `ffmpeg -sources alsa`) to find the correct screencast source.
- `grub` reorders boot options when the kernel upgrades — watch for this with secondary monitors.
- Acer monitors won't display grub on boot. Use a video capture card + phone to view it.
- New Linux OSes default to **Wayland** — many programs break. Use **Xorg/X11** instead.
- Many boot problems can be fixed via **Ctrl+Alt+F5** TTY login and `sudo` commands.
- Use `puTTY` as a tried-and-true cross-platform terminal emulator.
- `ffmpeg` is a tried-and-true cross-platform media tool. Python's native ffmpeg is ~4× faster than system-installed.
- Ubuntu community is very supportive. In order of helpfulness: StackExchange, Ubuntu Forums, Reddit, askUbuntu.
- Python's built-in UNIX time utilities are easier than online epoch sites.
- GitHub is great for cross-platform coordination. Don't track: `dist/`, `build/`, `.idea/`, `.vscode/`, `venv/`.
- Install settings files in local temp folders — don't track in GitHub.
- Don't install figures in GitHub; reproduce them with interactive plot tools instead.
- Don't expect other users to use GitHub — distribute binaries or use GitHub yourself on their machines.
- Avoid depending on streaming data (Particle Cloud, Blynk, Google Cloud) — eventually they charge.
- Use Python whenever possible. Scilab/Matlab tools can all be replaced by Python.
