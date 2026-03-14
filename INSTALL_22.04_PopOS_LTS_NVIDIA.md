# Installing Pop!_OS 22.04 LTS with NVIDIA Drivers

**Hardware:** HP Omen 15" 2022
**OS:** Pop!_OS 22.04 LTS (X11/Xorg)
**Purpose:** General workstation with dual-boot Ubuntu

> This machine already had Ubuntu dual-boot installed. See [INSTALL_24.04_Ubuntu.md](INSTALL_24.04_Ubuntu.md).
> Pop!_OS is an Ubuntu clone. It lacks `snapd` by default — install it first.
> PyCharm Community did not work from the default install; see the snap steps below.

---

## Table of Contents

- [1. Boot and Install](#1-boot-and-install)
- [2. Restore Windows Boot Entry](#2-restore-windows-boot-entry)
- [3. Initial Setup](#3-initial-setup)
- [4. Install Applications](#4-install-applications)
- [5. fwgWhisper Setup](#5-fwgwhisper-setup)
- [6. Fan Control](#6-fan-control)
- [7. Cleanup](#7-cleanup)
- [8. Performance Tuning](#8-performance-tuning)
- [9. Remote Access](#9-remote-access)
- [10. Google Drive (Rclone)](#10-google-drive-rclone)
- [11. Fixes and Troubleshooting](#11-fixes-and-troubleshooting)

---

## 1. Boot and Install

Insert ISO USB and boot:
- **F10** on HP-Omen, **F12** on Lenovo, **F7** on little_guy
- Set boot order to USB

Choose **"Try or install Ubuntu"** — allow ~3 minutes.

During installation — Modify disks using GParted:
- Select or delete to get to empty space
- Right-click → New:
  - 1000 MB FAT32
  - Remaining space: ext4
- Apply (green check)
- On new graphic:
  - Select small FAT32 → activate as `/boot/efi`
  - Select large ext4 → activate as `/root`
  - Select **Erase and Install**
  - Note location of Windows EFI (`/dev/nvme0n1p1`)
- Remove USB before Restart

---

## 2. Restore Windows Boot Entry

After first boot:

```bash
sudo apt update
sudo mkdir /mnt/windows
sudo mount /dev/nvme0n1p1 /mnt/windows
sudo cp -r /mnt/windows/EFI/Microsoft /boot/efi/EFI
sudo ls /boot/efi/EFI
sudo nano /boot/efi/loader/loader.conf
```

Add/modify:
```
timeout 5
console-mode max
```

Restart.

---

## 3. Initial Setup

Connect online accounts:
- Google, GNOME
- Allow location services

```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt install -y snapd   # IMPORTANT!
```

Install from Pop Shop (Applications): `sqlitebrowser`, `libreoffice`, `gnucash`, `brasero`, `gnome-calculator`, `caffeine`, `vlc`

Restart.

```bash
# VS Code (.deb — not snap)
sudo apt install ./Downloads/code_1.90.1-1718141439_amd64.deb
sudo apt install -y psensor   # fan speed monitor — add to favorites
```

Then follow [INSTALL_24.04_Ubuntu.md](INSTALL_24.04_Ubuntu.md) for remaining setup.

> During VS Code / Particle Workbench install: restart after crc32 fix and OS USB fix before devices will be recognized.

---

## 4. Install Applications

```bash
sudo snap install snapd
# Log out / log back in — IMPORTANT!
```

```bash
sudo apt install snapd
sudo snap install pycharm-community
```

Install Python 3.11 (for fwgWhisper — needs ≥3.8, <3.12):

```bash
sudo apt install python3-dev portaudio19-dev ffmpeg libssl-dev python3-tk
# See INSTALL_24.04_Ubuntu.md for full Python altinstall steps
```

In PyCharm:
- Help → Change Memory Settings → 4096 MB (for openai-whisper)
- Point at Python interpreter
- Load packages: `ffmpeg-python`, `openai-whisper`, `pvrecorder`, `pvdub`, `pvaudio`
- Run `speak_write.py` — when it works, run `install.py`

---

## 5. fwgWhisper Setup

```bash
source /home/daveg/Documents/GitHub/fwgWhisper/venv/bin/activate
```

---

## 6. Fan Control

```bash
source /home/daveg/Documents/GitHub/fwgWhisper/venv/bin/activate
pip3 install amdgpu-fan
sudo /home/daveg/Documents/GitHub/fwgWhisper/venv/bin/amdgpu-fan
```

Profile for maximum performance:

```bash
system76-power profile performance
```

AMD GPU kernel parameters:

```bash
sudo kernelstub -a "amdgpu.ppfeaturemask=0xffffffff"
```

---

## 7. Cleanup

```bash
sudo apt autoremove
sudo apt autoclean
sudo apt clean
sudo apt install deborphan
sudo apt remove $(deborphan)
```

### Fix wake from suspend

```bash
sudo kernelstub -a mem_sleep_default=deep
```

---

## 8. Performance Tuning

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install gparted synaptic
sudo apt install preload

sudo apt install timeshift
# Run: rsync, back up to USB ext4 drive

sudo apt install gufw
# Open "Firewall Configuration" → Status: On

sudo apt install bleachbit
```

### SSH

```bash
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
ip addr show
```

---

## 9. Remote Access

### RDP

```bash
sudo apt install xrdp
sudo ufw allow 3389
sudo systemctl status xrdp
# Automatic login must be disabled; log off first
```

If `xrdp` status shows `errno=22`, use the xrdp installer script from www.c-nergy.be/products.html:

```bash
cd Downloads
chmod +x xrdp-installer-1.5.4.sh
./xrdp-installer-1.5.4.sh -s
sudo systemctl status xrdp
```

---

## 10. Google Drive (Rclone)

```bash
sudo apt install rclone
rclone config
```

Follow the prompts:
1. `n` → new remote
2. Name: `gdrive`
3. Storage type: `drive` (Google Drive)
4. Leave `client_id` and `client_secret` blank
5. Scope: `1` (Full access)
6. Advanced config:
   - OAuth Token: https://myaccount.google.com/apppasswords — name `Rclone`
   - `upload_cutoff`: 1G
7. `Use auto config?`: `y`
8. Authenticate in browser
9. Team Drive: `n`
10. Confirm: `y`; Exit: `q`

```bash
mkdir ~/gdrive
rclone mount gdrive: ~/gdrive &
```

Add to startup applications. Remove ocamlfuse if previously installed.

---

## 11. Fixes and Troubleshooting

### gdm3 fails on restart

```bash
# Ctrl+Alt+F5 for TTY login, then:
sudo apt install --reinstall ubuntu-session
reboot
```

### Wake from suspend

```bash
sudo kernelstub -a mem_sleep_default=deep
```

### PyCharm cannot find `/usr/local/bin`

Problem is flatpak version. Uninstall and reinstall:

```bash
sudo snap install --classic pycharm-community
```

### `/var/log` flooded with "HDY_IS_CAROUSEL_BOX (self) failed"

```bash
sudo nano /etc/xdg/autostart/io.elementary.appcenter-daemon.desktop
# Change X-GNOME-Autostart-Delay from 60 to 0
```

### Firefox Performance

```
about:config
browser.sessionstore.interval = 150000
```
