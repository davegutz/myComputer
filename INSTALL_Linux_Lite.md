# Installing Linux Lite

**Hardware:** Lenovo Laptop
**OS:** Linux Lite (Xfce desktop, X11/Xorg)
**Purpose:** General workstation

> Linux Lite is based on Ubuntu. It lacks `snapd` by default — install it first.
> PyCharm Community did not work from the default install; see the snap install steps below.
> For most software, refer to [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md) ("I..").

---

## Table of Contents

- [1. Boot and Install](#1-boot-and-install)
- [2. Initial Setup](#2-initial-setup)
- [3. Install Applications](#3-install-applications)
- [4. Serial / USB Setup](#4-serial--usb-setup)
- [5. Cleanup](#5-cleanup)
- [6. HDMI Audio](#6-hdmi-audio)

---

## 1. Boot and Install

Insert ISO USB and boot:
- **F12** on Lenovo (rapid), **F10** on HP-Omen, **F7** on little_guy
- Set boot order to USB

Choose **"Direct install Linux Live"**

During installation:
- Do not install 3rd-party drivers (requires Secure Boot, which may be disabled from Ubuntu install)
- Choose complete install (3rd choice in list beginning "Reinstall Ubuntu")
- Initial password: `p`
- Restart will prompt to remove USB

After restart:
- Install Updates and reboot
- Install drivers (none may be available on Lenovo)
- Create restore point in Timeshift

---

## 2. Initial Setup

```bash
sudo apt update
sudo apt upgrade
sudo apt autoremove
sudo apt install -y firefox
sudo apt install -y ubuntu-restricted-extras
```

- Remove Chrome launcher from panel
- Linux Lite installs by default: LibreOffice, VLC

**Connect Google Drive (online accounts):**
- Check email for subject "google drive stuff" to bootstrap
- Menu → Settings → Session and Startup → Application Autostart → Add: `~/bin/start_google-drive-ocamlfuse`

Select dark theme (skip down to this step early on, before final upgrade).

Then try to upgrade:

```bash
sudo apt update
sudo do-release-upgrade
```

---

## 3. Install Applications

For VS Code, PyCharm, GitHub, Plex, and puTTY, see [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md).

```bash
sudo apt install -y python3-tk   # required for PyCharm (no restart needed)
```

**puTTY serial permissions:**

```bash
sudo nano /etc/udev/rules.d/01-ttyusb.rules
# Add:
SUBSYSTEMS=="usb-serial", TAG+="uaccess"
```

**Screen timeout:** Settings → Power

Reboot.

---

## 4. Serial / USB Setup

Simple serial check (optional, for debugging):

```bash
sudo apt install screen
sudo screen /dev/ttyACM0 230400
```

---

## 5. Cleanup

```bash
sudo apt autoremove
sudo apt autoclean
sudo apt clean
sudo apt install deborphan
sudo apt remove $(deborphan)
```

Set passwords (per [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md)):

```bash
sudo passwd daveg
sudo passwd   # root
rm ~/.local/share/keyrings/login.keyring
```

**Timeshift:** Turn off scheduled backups or they will eat your disk:
- Menu → Timeshift → Settings → Schedule → also restore/delete any already created

---

## 6. HDMI Audio

```bash
pactl load-module module-alsa-sink device=hw:0,3
sudo nano /etc/pulse/default.pa
# Add at end:
pactl load-module module-alsa-sink device=hw:0,3

# Manually unmute:
sudo alsamixer   # F6 → default → unmute S/PDIF

sudo alsactl --file ~/.config/asound.state store
sudo nano ~/.bashrc
# Add at end:
alsactl --file ~/.config/asound.state restore
```
