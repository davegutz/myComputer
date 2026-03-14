# Installing Ubuntu (Dual Boot) on Venus

**Hardware:** MINISFORUM Venus Series UM773 Lite Mini PC
- Processor: AMD Ryzen 7 7735HS with Radeon Graphics × 16
- Memory: 32 GB DDR5-4800
- Storage: 1 TB PCIe 4.0 SSD
- Graphics: REMBRANDT (LLVM 15.0.7, DRM 3.54)
- OS Name: Ubuntu 22.04.4 LTS (64-bit)
- GNOME 42.9, Wayland
- Wireless: `4C:24:CE:D7:76:45` (static: `192.168.1.45`)
- Hostname: `daveg-Venus-Linux`
- BIOS: F7 (repeatedly)

> **Read the Lessons Learned section before installing as a dual-boot system.**

---

## Table of Contents

- [1. Preparation](#1-preparation)
- [2. Boot and Install](#2-boot-and-install)
- [3. Connect Online Accounts](#3-connect-online-accounts)
- [4. Initial Setup](#4-initial-setup)
- [5. Mount Windows Partition (Optional)](#5-mount-windows-partition-optional)
- [6. Install Applications](#6-install-applications)
- [7. Google Drive (ocamlfuse)](#7-google-drive-ocamlfuse)
- [8. GitHub Desktop](#8-github-desktop)
- [9. Plex Media Server](#9-plex-media-server)
- [10. YouTube Downloader (ClipGrab)](#10-youtube-downloader-clipgrab)
- [11. Alternate Python Version](#11-alternate-python-version)
- [12. puTTY Setup](#12-putty-setup)
- [13. Development Setup](#13-development-setup)
- [14. Cleanup](#14-cleanup)
- [15. Network and WiFi](#15-network-and-wifi)
- [16. Optional Tools](#16-optional-tools)
- [17. LTSpice via Wine](#17-ltspice-via-wine)
- [18. Lessons Learned](#18-lessons-learned)

---

## 1. Preparation

- Phone ready to approve Google requests and USB tethering if needed
- Make space for Linux — note partition numbers
- Have a >4 GB thumbdrive
- On Windows: download the ISO, flash using **balenaEtcher**
- Turn off BitLocker on all drives
- Deauthorize DVDfab, WinXDVD, ePubor
- Unplug second monitor and extra USB devices

> **NOTE:** don't use an all-number password — you won't be able to drop into lightdm with it.

---

## 2. Boot and Install

Insert the ISO USB and boot:
- **F7** on Venus (little_guy), **F10** on HP-Omen, **F12** on Lenovo

Choose **"Try or install Ubuntu"** — allow ~3 minutes.

Partition setup (Custom):

| Partition | Size | Type | Mount |
|-----------|------|------|-------|
| p5 | all remaining | ext4 | `/` |

> *Commented-out alternatives:*
> - p5: swap 35 GB (larger than 32 GB RAM)
> - p6: ext4 `/` 21 GB
> - p7: ext4 `/boot` 500 MB
> - p8: ext4 `/home` remaining

Username: `daveg` / `daveg-Venus-Linux`

Wait ~12 minutes. When prompted to reboot, leave USB in until prompted to remove it.
Start with a short password during install, then change it at the end.

**If `grub>` command prompt appears due to crash:** type `exit` to boot into Windows.

**If system boots Windows instead of Ubuntu:** re-open BIOS → Boot → move Ubuntu to the top.

---

## 3. Connect Online Accounts

- Google
- GNOME
- Allow location services

---

## 4. Initial Setup

```bash
# Ctrl+Alt+T for terminal
sudo apt update
sudo apt upgrade
sudo apt autoremove
```

### Power Button

Settings → Power → Power Button Behavior → **Nothing** (prevents accidental shutdown).

### Second Monitor

Plug it in. Leave built-in display primary. Turn on night light (low setting).
Configure desktop at this time.

Open this file in Drive for copy/paste reference:
- WiFi → personal: `7ef79856c1a52598410c`
- Turn off automatic for Guest5G network

Firefox: sign in, start BitWarden. Restart.

---

## 5. Mount Windows Partition (Optional)

Open Disks utility → select Windows partition → Edit Mount Options:
- Turn off "Use Session Defaults"
- Mount at system startup
- Show in user interface
- Display Name: `Windows`
- Mount point: `/mnt/Windows`
- Identify As: `LABEL=Windows`
- Filesystem Type: `auto`

---

## 6. Install Applications

```bash
sudo snap install plexmediaserver
sudo snap install --classic pycharm-community
sudo snap install sqlitebrowser
```

Open Snap GUI (Applications) → Accept updates → Restart

```bash
# Open Snap GUI again and install: code, gnucash, brasero, vlc, gnome-calculator, caffeine
sudo apt update && sudo apt upgrade
```

Restart.

```bash
sudo apt install -y fuse libfuse2      # AppImage support
sudo apt install -y ffmpeg
sudo apt install -y git
sudo apt-get install -y putty
sudo apt-get install -y python3-tk     # for PyCharm
sudo apt install -y dhcpcd5
sudo apt install dos2unix
sudo apt install xsel
sudo apt install -y pavucontrol        # for myPyScreencast
sudo apt-get install ubuntu-restricted-extras
```

### VLC

Tools → Preferences → Codecs → **disable hardware-accelerated decoding** → Save. Restart VLC.

### Fix missing Settings (if needed)

```bash
sudo apt-get install ubuntu-desktop
# Restart
```

---

## 7. Google Drive (ocamlfuse)

```bash
sudo add-apt-repository ppa:alessandro-strada/ppa
sudo apt update && sudo apt install -y google-drive-ocamlfuse
```

> Special: needs to run with a secret. Search Gmail for "google-drive-ocamlfuse" for the command.
> Had to set up Google Cloud free trial (Project 6102) and enable the Google Drive API.

After authorizing in browser ("Access token retrieved"):

```bash
mkdir ~/google-drive
google-drive-ocamlfuse ~/google-drive/
# Add -debug for troubleshooting; then: more /home/daveg/.gdfuse/default/gdfuse.log

nano .gdfuse/default/config
# Add:
stream_large_files=true

mkdir ~/bin
cat << EOF > /home/daveg/bin/start_google-drive-ocamlfuse
#!/bin/bash
while true; do
  if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    google-drive-ocamlfuse /home/daveg/google-drive/; break;
  else
    sleep 1
  fi
done
EOF
chmod +x /home/daveg/bin/start_google-drive-ocamlfuse
```

Open **Startup Applications** and add this script.

---

## 8. GitHub Desktop

```bash
sudo wget https://github.com/shiftkey/desktop/releases/download/release-3.1.1-linux1/GitHubDesktop-linux-3.1.1-linux1.deb
sudo apt-get install -y gdebi-core
sudo gdebi GitHubDesktop-linux-3.1.1-linux1.deb
github
```

Sign in to GitHub.com (password in BitWarden).

---

## 9. Plex Media Server

Turn off the main Plex server in the house before proceeding.

Start plexmediaserver from Applications → Sign in with Google ID.

**Claim** this new installation (look for yellow exclamation points/triangles in menus).

Name: `PLEX-LINUX` on pc for server.

Connect USB drive, then set up libraries:
- Movies: `/media/daveg/Lib/Movies`
- TV Shows: `/media/daveg/Lib/TV Shows`
- Other Videos: `/media/daveg/Lib/Videos`

Settings → Transcoder:
- Deselect **Use hardware acceleration when available**
- Transcoder Temporary Directory: `/media/daveg/DVRcache`

DVR: mount spare 3TB hard drive named `DVRcache`. Use Files → browse to DVR drive → right-click Properties → set Create & Delete permissions for all.

After several hours of loading, restart Plex to see all content.

---

## 10. YouTube Downloader (ClipGrab)

1. Download `yt-dlp` for Linux from https://github.com/yt-dlp/yt-dlp
2. Download ClipGrab from https://clipgrab.org/download-clipgrab/

```bash
cd Downloads
chmod a+x ClipGrab-3.9.10-x86_64.AppImage
./ClipGrab-3.9.10-x86_64.AppImage   # errors first time — press Continue (not Exit)
mv yt-dlp /home/daveg/.local/share/ClipGrab/ClipGrab/
```

Save ClipGrab icon as `Downloads/ClipGrab.jpeg`, then:

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

## 11. Alternate Python Version

> **Never replace the default Python in Debian-based Linux.**
> Reference: https://ubuntuhandbook.org/index.php/2021/10/compile-install-python-3-10-ubuntu/

Install build dependencies:

```bash
sudo apt update
sudo apt install -y wget build-essential libreadline-dev libncursesw5-dev \
  libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
  libffi-dev zlib1g-dev portaudio19-dev
```

Download and compile Python 3.11.9:

```bash
# From https://www.python.org/ftp/python/
cd Downloads/
tar -Jxf Python-3.11.9.tar.xz
cd Python-3.11.9/
./configure --enable-optimizations --enable-shared
sudo make -j4 && sudo make altinstall
sudo ldconfig /usr/local/lib   # load shared libraries once

# Verify
python3.11 --version
python3.11 -m pip --version

# Uninstall (if needed)
cd Downloads/Python-3.11.9/
sudo make uninstall
```

Use `.venv` in PyCharm to set up an app with this Python version.

---

## 12. puTTY Setup

```bash
cd $HOME/Documents/GitHub/myStateOfCharge/SOC_Particle/dataReduction/putty/
# Start puTTY from launch — save a 'def' session first to create folders
# Open .._def.odt for setup steps
```

> Set font to **Free Mono 10**. Then create 'test' session from 'def'.

```bash
# Find which TTY after plugging in device:
sudo dmesg | grep tty
sudo chgrp daveg /dev/ttyACM0
```

> Save puTTY data on local drive. GUI_TestSOC may use dataReductionFolder on google-drive but **should not** stream to google-drive via puTTY.

---

## 13. Development Setup

### PyCharm

- Setup venv for Python; update pip before importing packages
- Use local dictionary: Settings → Editor → Natural Languages → Spelling
- **Caution:** Use PyCharm to install Python interpreters — deb install broke Ubuntu
- May need to start twice on first launch

### movie_Scraper

- Use `PySimpleGUI-4-foss` instead of `PySimpleGUI`
- Set DB location to `/home/daveg/google-drive/Movies Stuff` (or `/home/daveg/Documents/GitHub/myComputer`)
- Run executable build steps at top of `GUI_sqlite_scrape.py`

```bash
cat << EOF > /home/daveg/Desktop/GUI_sqlite_scrape.desktop
[Desktop Entry]
Name=GUI_sqlite_scrape
Exec=/home/daveg/Documents/GitHub/movie_Scraper/dist/GUI_sqlite_scrape/GUI_sqlite_scrape
Path=/home/daveg/Documents/GitHub/movie_Scraper/dist/GUI_sqlite_scrape
Icon=/home/daveg/Documents/GitHub/movie_Scraper/popcorn.ico
comment=app
Type=Application
Terminal=true
Encoding=UTF-8
Categories=Utility;
EOF

gio set /home/daveg/Desktop/GUI_sqlite_scrape.desktop metadata::trusted true
chmod a+x ~/Desktop/GUI_sqlite_scrape.desktop
sudo mv /home/daveg/Desktop/GUI_sqlite_scrape.desktop /usr/share/applications/
```

### myPyScreencast

- Use movie_scraper interpreter (`venv/bin/python310`)
- Insert headphones; open browser, play music on YouTube
- Use `pavucontrol`: assign browser to LoopbackAnalogStereo
- Video: `x11grab :0.0+0.0`; Audio: `pulse alsa_output.platform-snd_aloop.0.analog-stereo.monitor`

### myStateOfCharge (VS Code / SOC_Particle)

```bash
sudo apt-get install libarchive-zip-perl   # fix 'crc32 not found'
```

- VS Code: Codeium AI (login via Google), Ruff, Python, Workbench
- File → Open Folder → `Documents/GitHub/myStateOfCharge/SOC_Particle`
- File Icon → Explorer → Open Editors
- Find Icon → ellipses → include `*.h, *.cpp, *.ino` / exclude `SOC_Particle.cpp`
- Log into Particle Workbench ASAP: `davegutz@alum.mit.edu`
- Edit `local_config.h`
- First flash: guided to install USB drivers → answer `Y` → give daveg password

```bash
# Serial permission:
sudo chown daveg /dev/ttyACM0
# puTTY font: 8 any mono
```

### fwgWhisper

- Only Python versions ≥3.8, <3.12 supported; use 3.11.9 (see above)
- May need to manually remove non-openai whisper package

```bash
sudo apt-get install portaudio19-dev -y
source /home/daveg/Documents/GitHub/fwgWhisper/.venv/bin/activate
pip install pyaudio
```

Simple serial check (optional):

```bash
sudo apt install screen
sudo screen /dev/ttyACM0 230400
```

---

## 14. Cleanup

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

## 15. Network and WiFi

### Bluetooth

```bash
sudo apt install bluez bluez-tools pulseaudio-module-bluetooth
sudo systemctl restart bluetooth
bluetoothctl scan on
```

### WiFi Power Management

```bash
sudo apt install net-tools
ifconfig
sudo iwconfig wlp2s0 power off && \
  sudo sed -i 's/wifi.powersave = 3/wifi.powersave = 2/' \
  /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
```

### Forget a Saved Network

```bash
sudo ls /etc/NetworkManager/system-connections/
sudo rm /etc/NetworkManager/system-connections/ourHappyHome2.nmconnection
```

### Shared Folder (Samba)

```bash
# Browse to public folder:
thunar   # click 'Browse Network' → 'Windows Network'
# Or directly: smb://192.168.1.222/public/
# Login: daveg / J3susY0ga
```

---

## 16. Optional Tools

### Flatpak

```bash
sudo apt install -y flatpak gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
# restart
```

### MissionCenter (Task Manager)

```bash
flatpak install flathub io.missioncenter.MissionCenter
flatpak run io.missioncenter.MissionCenter
```

### Chrome Browser

```bash
sudo apt install libu2f-udev
cd Downloads
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### Desktop Clock (conky)

```bash
sudo apt install conky-all
mkdir ~/.config/conky
cat << 'EOF' > /home/daveg/.config/conky/conky.conf
conky.config = {
    background = false, update_interval = 1, double_buffer = true,
    no_buffers = true, text_buffer_size = 2048, own_window = true,
    own_window_class = 'conky', own_window_argb_visual = true,
    own_window_argb_value = 80,
    own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager',
    own_window_colour = '#252525', own_window_type = 'desktop',
    minimum_width = 250, gap_x = 100, gap_y = 200,
    use_xft = true, font = 'Noto:size=8',
};
conky.text = [[
${voffset 5}${offset 15}${font Noto:size=36}${color white}${time %e}
${goto 25}${font Noto:size=18}${color white}${voffset -30}${time %b}${color white}${offset 10}${time %Y}
${font Noto:size=12}${color white}${voffset 5}${goto 20}${time %A}${goto 153}${color white}${time %H}:${time %M}
]];
EOF
chmod +x .config/conky/conky.conf
# Add to Startup Applications: conky -c ~/.config/conky/conky.conf
```

### Better File Managers

```bash
sudo apt install nemo
sudo apt install thunar
```

---

## 17. LTSpice via Wine

```bash
sudo apt update
sudo apt-get install wine-stable
cd /tmp/
wget https://ltspice.analog.com/software/LTspice64.exe
wine LTspice64.exe
rm LTspice64.exe

# Start LTspice:
wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe

# Copy simulation files:
mkdir ~/.wine/drive_c/my_ltspice_files
cp ~/Documents/GitHub/myStateOfCharge/SOC_Particle/datasheets/pSpice/* \
   ~/.wine/drive_c/my_ltspice_files
```

---

## 18. Lessons Learned

### Dual Boot

- Install Windows first — it's more selfish about the bootloader
- Windows "Fast Startup" may prevent accessing Linux on reboot — disable it:
  Control Panel → Hardware and Sound → Power Options → Choose what power button does
- Best to install on separate physical drives
- Linux can access Windows files; Windows cannot access Linux files
- **Clock offset between Linux and Windows:** either configure Linux to use local time or configure Windows to use UTC:
  https://www.howtogeek.com/323390/how-to-fix-windows-and-linux-showing-different-times-when-dual-booting/

### General

- **Do not interrupt** a command-line upgrade — it will break the system.
- **Never upgrade/delete shipped Python.** Use `altinstall` make directive.
- **Always use `venv`** unique to each Python project.
- `pavucontrol` defaults to low volume — set to 100% for screencasting.
- Use `ffmpeg -sources pulse` to find the correct screencast source.
- `grub` reorders boot options when kernel upgrades.
- Acer monitors won't display grub — use a video capture card to see it.
- New Linux OSes default to **Wayland** — use **Xorg/X11** instead.
- Many boot problems fixable via **Ctrl+Alt+F5** TTY login.
- Ubuntu community is very supportive: StackExchange, Ubuntu Forums, Reddit, askUbuntu.
- Python's native ffmpeg is ~4× faster than system-installed.
- GitHub: don't track `dist/`, `build/`, `.idea/`, `.vscode/`, `venv/`.
- Don't install figures in GitHub — use interactive plot tools instead.
- Avoid dependence on streaming data (Particle Cloud, Blynk, Google Cloud).
- Use Python whenever possible — replaces Scilab/Matlab.
