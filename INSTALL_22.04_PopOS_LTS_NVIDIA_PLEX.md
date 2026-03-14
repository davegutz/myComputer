# Installing Pop!_OS 22.04 LTS with NVIDIA Drivers (PLEX Server)

**Hardware:** HP Omen 15" 2022
**OS:** Pop!_OS 22.04 LTS (X11/Xorg)
**Purpose:** General workstation + Plex Media Server

> Pop!_OS is superb for NVIDIA hardware — System76 optimized it for NVIDIA gaming.
> It lacks `snapd` by default — install it first.
> Pop!_OS gives poor screencast results and there were difficulties with unencrypted install due to NVIDIA/Pop screen resolution incompatibility.
> **When in doubt, use instructions for Ubuntu.**

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
- [10. Auto Suspend Scheduling](#10-auto-suspend-scheduling)
- [11. Cleanup](#11-cleanup)
- [12. Plex Media Server](#12-plex-media-server)
- [13. Samba File Sharing](#13-samba-file-sharing)
- [14. Fixes and Troubleshooting](#14-fixes-and-troubleshooting)

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

Choose **"Try or install..."** — allow ~3 minutes (may hear music).

During installation:
- Initial display may be wonky (Pop may not recognize old Acer monitor)
- **Fresh clean install**, minimal, install updates
- Username: `daveg` / password
  > The initial password becomes the LUKS file system encryption key. Start with your final password, then temporarily change to a short one during install.
- When done, press Finish — it will prompt you to remove media

After restart it should boot to Linux without BIOS intervention.
It may come up without WiFi — connect Ethernet to grab updates and fix wireless.

---

## 3. WiFi and Drivers

**Preferences → Additional Drivers:**
- NVIDIA proprietary (tested)
- Broadcom STA wireless
- Apply → Close → Restart

**Sign into WiFi**, then add Google DNS:

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
sudo apt install snapd
# Log out and log back in after installing snapd — IMPORTANT!
sudo apt autoremove
```

Install from Pop Shop (Applications): `sqlitebrowser`, `brasero`, `caffeine`, `vlc`

```bash
sudo kernelstub -a mem_sleep_default=deep   # prevent not waking after suspend
```

Restart.

---

## 5. GitHub Desktop

```bash
sudo wget https://github.com/shiftkey/desktop/releases/download/release-3.1.1-linux1/GitHubDesktop-linux-3.1.1-linux1.deb
sudo apt-get install -y gdebi-core
sudo gdebi GitHubDesktop-linux-3.1.1-linux1.deb
github
```

Sign in to GitHub.com (password in BitWarden). Download `myComputer` to get this file.

---

## 6. Install Applications

```bash
sudo snap install snapd
# Log out / log back in to organize snapd ########## IMPORTANT — it will work after this
sudo snap install plexmediaserver   # for remote laptop (trips) and basement server
sudo apt install ./Downloads/code_1.90.2-1718751586_amd64.deb
sudo apt install -y fuse libfuse2   # AppImage support
sudo apt install -y ffmpeg
sudo apt install -y git
sudo apt install --fix-missing -y python3-pip
sudo apt install -y python3-tk      # for PyCharm
sudo apt install -y dhcpcd5
sudo apt install dos2unix
sudo apt install LocalSend
sudo apt install xsel
sudo apt install -y pavucontrol     # for myPyScreencast
```

### PyCharm

> Flatpak (used in Pop!_OS) causes path errors — PyCharm cannot find custom Python builds in `/usr/local/bin`.
> **Uninstall the flatpak version and use snap instead.**

```bash
sudo apt install snapd
sudo snap install --classic pycharm-community
```

### Alternate Python Version

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
```

### VLC

Tools → Preferences → Codecs → **disable hardware-accelerated decoding** → Save. Restart VLC.

---

## 7. Sound Configuration

```bash
sudo nano /etc/modules-load.d/modules.conf
# Add:
snd-aloop

# Load for this session:
sudo modprobe snd-aloop
```

### Screencast audio setup

```bash
ffmpeg -sources pulse   # find the loopback source
pactl list short sources
# Target: alsa_output.platform-snd_aloop.0.analog-stereo.monitor
```

> **pavucontrol** defaults to low volume — set loopback output to 100%.

```bash
sudo snap install audacity   # optional for audio debugging
```

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

- Setup venv for Python; update pip before importing more packages
- Use local dictionary: Settings → Editor → Natural Languages → Spelling
- **Caution:** Use PyCharm to install Python interpreters — deb install broke Ubuntu
- May need to start PyCharm twice on first launch

### movie_Scraper

- Use its own `.venv`
- Set DB location to `/home/daveg/google-drive/Movies Stuff`
- Run `install.py` and follow instructions

### myPyScreencast

- Use its own `.venv`
- Insert headphones, open browser, play music on YouTube
- Use `pavucontrol` to assign browser to LoopbackAnalogStereo

---

## 10. Auto Suspend Scheduling

```bash
# Copy suspend_until script from this repo
chmod +x /home/daveg/bin/suspend_until

sudo crontab -e
# Add:
1 0 * * 1-6 /home/daveg/bin/suspend_until 16:00   # Mon-Sat: wake at 4 PM
1 0 * * 0   /home/daveg/bin/suspend_until 10:15   # Sun: wake at 10:15 AM (Face the Nation)

sudo crontab -l   # verify
```

No restart needed — cron reads crontab files every minute.

Pop!_OS Settings → Power → Automatic Suspend: Off; Screen Blank: 15 min

---

## 11. Cleanup

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

## 12. Plex Media Server

Turn off the main Plex server in the house before proceeding (it will confuse Plex).

```bash
# Start plexmediaserver from Applications menu (snap didn't auto-start)
```

Sign in with Google ID. **Claim** this new installation (look for yellow exclamation points/triangles).

Name: `PLEX-LINUX` on pc for server. Uncheck "Allow me to access my media outside my home."

Connect USB drive, then:

- Plex → Manage Libraries → Add sources:
  - Movies: `/media/daveg/Lib/Movies`
  - TV Shows: `/media/daveg/Lib/TV Shows`
  - Other Videos: `/media/daveg/Lib/Videos`

> **WAIT before finishing a library add or the path will be shortened.**

- Settings → Transcoder:
  - Deselect **Use hardware acceleration when available**
  - Transcoder Temporary Directory: `/media/daveg/Videos/DVRcache`
- Add to TV Shows library: `/media/daveg/Videos/DVRcache`
- Switch library tabs from **Recommended** to **Library**

After several hours, restart Plex to see all content.

### Permissions

```bash
sudo usermod -a -G daveg plexmgr
# restart
sudo chown daveg /media/daveg
sudo chmod -R a+rwx /media/daveg
```

Set folder permissions:
- Owner: Create & Delete
- Group (daveg): Create & Delete
- Others: Create & Delete

---

## 13. Samba File Sharing

```bash
sudo apt install -y samba samba-common-bin
sudo apt install net-tools
sudo apt install vino -y
sudo apt install -y xrdp
sudo systemctl enable xrdp
sudo apt-get install libarchive-zip-perl    # for Particle Workbench crc32
sudo mkdir /Public
sudo chmod -R 0777 /Public
sudo adduser --no-create-home plexmgr
sudo usermod -u 998 plexmgr
sudo smbpasswd -a plexmgr   # same password as daveg
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
ifconfig   # note IP; make static via EERO phone app
```

Pop!_OS Settings → Sharing: enable everything, set password same as others.

---

## 14. Fixes and Troubleshooting

### gdm3 fails on restart

```bash
# Ctrl+Alt+F5 for TTY login, then:
sudo apt install --reinstall ubuntu-session
reboot
```

### Wake from suspend

```bash
sudo kernelstub -a mem_sleep_default=deep
# restart
```

### PyCharm cannot find `/usr/local/bin`

Problem is flatpak version. Uninstall and reinstall:

```bash
sudo snap install --classic pycharm-community
pycharm-community   # to start (won't appear in menus initially)
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
