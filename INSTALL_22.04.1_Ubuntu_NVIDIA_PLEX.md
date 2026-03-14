# Installing Ubuntu 22.04.1 LTS with NVIDIA Drivers (PLEX Server)

**Hardware:** HP Omen 15" 2022
**OS:** Ubuntu 22.04.1 LTS (GNOME)
**Purpose:** General workstation + Plex Media Server

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
- [14. Lessons Learned](#14-lessons-learned)
- [15. NVIDIA Notes](#15-nvidia-notes)
- [16. Jellyfin Media Server](#16-jellyfin-media-server)

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

Insert the ISO USB and boot:
- **F10** on HP-Omen, **F12** on Lenovo, **ESC** on HP-Phoenix, **F7** on little_guy
- Set boot order to USB

Choose **"Try or install Ubuntu"** — allow ~3 minutes (may hear music).

During installation:
- May need to disconnect the 3TB extra drive in cabinet to get past BitLocker tests (reinstall later)
- **Fresh clean install**, basic installation
- Username: `daveg` / password
  > Initial password becomes the LUKS encryption key. Start with your final password, then temporarily shorten it during install.
- When done, press Finish — prompts to remove media and restarts

After restart: may come up without WiFi — connect Ethernet first.

---

## 3. WiFi and Drivers

**Settings → Additional Drivers:**
- NVIDIA proprietary (tested) — was there by default
- Broadcom STA wireless — was there by default
- Apply → Close (no restart needed)

**Sign into WiFi** (`ourHappyHome5G`).

> **DO NOT activate `OurHappyHomeGuest`** — it interferes with PLEX and EERO modem by putting devices on different networks.

Add Google DNS:

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
sudo do-release-upgrade   # if desired
sudo apt autoremove
```

**Firefox:**
- Sign in and pin BitWarden to toolbar
- Always show Bookmarks Bar
- Sign into Gmail

**Users:**
- Add `plexmgr` user (same properties as `daveg`)

**Schedule suspend (copy from this repo):**

```bash
sudo cp Documents/GitHub/myComputer/suspend_until /usr/local/bin/.
sudo chmod +x /usr/local/bin/suspend_until
sudo crontab -e
# Add:
1 0 * * 1-6 /usr/local/bin/suspend_until 16:00   # Mon-Sat
1 0 * * 0   /usr/local/bin/suspend_until 10:15   # Sun (Face the Nation at 10:30)

sudo crontab -l   # confirm
```

No restart needed — cron reads all crontab files every minute.

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

Update software using Software Updater.

From App Center install: `sqlitebrowser`, `brasero`, `caffeine`, `Freefilesync`, `localsend`

Restart.

---

## 6. Install Applications

```bash
sudo snap install plexmediaserver
sudo apt install -y fuse libfuse2      # AppImage support
sudo apt install -y ffmpeg
sudo apt install -y dos2unix
sudo apt install -y git
sudo apt install --fix-missing -y python3-pip
sudo apt install -y python3-tk         # for PyCharm
sudo apt install -y dhcpcd5
sudo apt install LocalSend
sudo apt install -y vlc
sudo apt install xsel
sudo apt install -y pavucontrol        # for myPyScreencast
sudo snap install --classic pycharm-community
sudo apt install -y thunar
sudo apt install -y nautilus
```

### VS Code

> **Do NOT use `snap install code --classic`** — the snap sandboxes VS Code and breaks Particle build tools.

```bash
# Download .deb from https://code.visualstudio.com/docs/?dv=linux64_deb
sudo apt install ./Downloads/code_*.deb
sudo apt install libarchive-zip-perl   # fixes missing crc32 for Particle Workbench
```

### VLC

Tools → Preferences → Codecs → **disable hardware-accelerated decoding** → Save. Restart VLC.

### FreeFileSync (Backup)

```bash
# Plug in Lib and backup drives (Lib_Dupe, etc.)
# Open FreeFileSync from App Center
# Press green '+' for each backup row
# Left: browse to Lib; Right: browse to each backup
# Right gear → Mirror
# Compare (ignore 'lost and found' error)
# Synchronize
```

> Consider using `rsync` instead of FreeFileSync.

### Chrome Browser

```bash
sudo apt install libu2f-udev
cd Downloads
rm google-chrome-stable*.deb
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### Firefox Security Exceptions

Add exceptions for: `hulu.com`, `amazon.com`, `play.max.com`, `netflix.com`

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

- Setup `.venv` for Python; update pip before importing packages
- Use local dictionary: Settings → Editor → Natural Languages → Spelling
- **Caution:** Use PyCharm to install Python interpreters — deb install broke Ubuntu
- May need to start PyCharm twice on first launch

### movie_Scraper

- Use its own `.venv`
- Use `PySimpleGUI-4-foss` instead of `PySimpleGUI`
- Set DB location to `/home/daveg/Documents/GitHub/myComputer`
- Run `install.py` and follow instructions

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

Plex libraries:
- Movies: `/media/daveg/Lib/Movies`
- TV Shows: `/media/daveg/Lib/TV Shows`
- Other Videos: `/media/daveg/Lib/Videos`
- Add to TV Shows: `/media/daveg/Videos/DVRcache`

Settings:
- Transcoder → Deselect **Use hardware acceleration when available**
- Transcoder Temporary Directory: `/media/daveg/Videos/DVRcache` or `/home/daveg/Documents/Recordings`
- Network → Secure Connections → Required (to use wirelessly)
- Disable IPv6 on each network

After several hours of loading, restart Plex to see all content.

### Permissions

```bash
sudo usermod -a -G daveg plexmgr
# restart
```

Set folder permissions for `/media/daveg`:
- Owner: Create & Delete; Group (daveg): C&D; Others: C&D
- Files: Owner R&W; Group R&W; Other R
- Folders: Owner C&D; Group C&D; Other Access only

Switch library tabs from **Recommended** to **Library**.

---

## 12. Samba File Sharing

```bash
sudo apt install -y --fix-missing samba samba-common-bin
sudo apt install --fix-missing net-tools
sudo apt install vino -y
sudo apt install -y xrdp
sudo systemctl enable xrdp
sudo apt install libarchive-zip-perl    # for Particle Workbench
sudo mkdir /Public
sudo chmod -R 0777 /Public
sudo smbpasswd -a plexmgr               # or daveg; same password
sudo ufw allow samba
```

Edit `/etc/samba/smb.conf` — add before `[printers]`:

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
sudo gpasswd -a plexmgr samba   # or daveg
sudo mkdir -p /srv/samba/private/
sudo setfacl -R -m "g:samba:rwx" /srv/samba/private/
testparm
sudo systemctl restart smbd nmbd
ifconfig   # note IP address
```

Create static IP reservation via EERO phone app.

**Local access:**
```
smb://localhost
```

**Remote access (Windows shortcut):**
- Right-click desktop → New → Shortcut
- Location: `\\192.168.5.205\Public`

### Wireless Power Management

```bash
iwconfig   # get adapter name (e.g., wlp4s0)
sudo iwconfig wlp4s0 power off && \
  sudo sed -i 's/wifi.powersave = 3/wifi.powersave = 2/' \
  /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
```

---

## 13. Fixes and Troubleshooting

### gdm3 fails on restart

```bash
# Ctrl+Alt+F5 for TTY login:
sudo apt install --reinstall ubuntu-session
reboot
```

### Suspend not working (HP Envy / Ubuntu 24.04)

```bash
sudo systemctl disable nvidia-suspend
# No reboot needed
```

### PyCharm cannot find `/usr/local/bin`

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

### daveg doesn't have permissions to attached external drive

```bash
# restart
```

### `/var/log` flooded with "HDY_IS_CAROUSEL_BOX (self) failed"

```bash
sudo nano /etc/xdg/autostart/io.elementary.appcenter-daemon.desktop
# Change X-GNOME-Autostart-Delay from 60 to 0
```

---

## 14. Lessons Learned

- **Do not interrupt** a command-line upgrade — it will break the system.
- **Never directly upgrade or delete** the shipped Python. Use `altinstall`.
- **Always use `venv`** unique to each Python project.
- `pavucontrol` defaults to low volume — set to 100% for screencasting.
- Use `ffmpeg -sources pulse` to find the correct screencast source.
- `grub` reorders boot options when the kernel upgrades.
- Acer monitors won't display grub on boot — use a video capture card to see it.
- New Linux OSes default to **Wayland** — use **Xorg/X11** instead.
- Many boot problems fixable via **Ctrl+Alt+F5** TTY login.
- Ubuntu community is very supportive: StackExchange, Ubuntu Forums, Reddit, askUbuntu.

---

## 15. NVIDIA Notes

```bash
Settings → System → About   # shows NVIDIA if recognized
nvidia-smi                   # shows GPU state (always off during heavy movie/screencast use)
sudo apt dist-upgrade
sudo apt autoremove
```

If NVIDIA not working:
- Settings & Updates → Additional Drivers → apply nouveau → restart → run 15 min → restart → apply NVIDIA prop tested → restart
- BIOS (ESC) → Advanced → Enhanced (?) → Integrated Video

Check active GPU:

```bash
lspci -vnnn | perl -lne 'print if /^\d+\:.+(\[\S+\:\S+\])/' | grep VGA
# Whichever device shows [VGA controller] at the end is the active GPU
```

---

## 16. Jellyfin Media Server

```bash
uname -r   # verify x86/amd architecture
# Install from https://jellyfin.org/downloads/server/
# Visit http://192.168.5.205:8096
# Use same password as user

sudo usermod -a -G daveg jellyfin
sudo chown -R jellyfin /media/daveg
# Allow Jellyfin Incoming in Firewall
# Open browser to server address and fill libraries
```
