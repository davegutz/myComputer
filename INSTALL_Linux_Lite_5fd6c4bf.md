# Installing Linux Lite (Archived Version)

**Hardware:** Lenovo Laptop
**OS:** Linux Lite (Xfce desktop, X11/Xorg)

> This is an earlier/archived version of the Linux Lite install notes.
> For the current and more complete version, see [INSTALL_Linux_Lite.md](INSTALL_Linux_Lite.md).
> Linux Lite is based on Ubuntu. It lacks `snapd` by default.
> For most software, refer to [INSTALL_24.04_Ubuntu.md](INSTALL_24.04_Ubuntu.md) ("I..").

---

## Table of Contents

- [1. Boot and Install](#1-boot-and-install)
- [2. Initial Setup](#2-initial-setup)
- [3. Install Applications](#3-install-applications)
- [4. Serial Check](#4-serial-check)
- [5. Cleanup](#5-cleanup)

---

## 1. Boot and Install

Insert ISO USB and boot:
- **F12** on Lenovo (rapid), **F10** on HP-Omen, **F7** on little_guy
- Set boot order to USB

Choose **"Direct install Linux Live"**

During installation:
- Do not install 3rd-party drivers (requires Secure Boot, may be disabled from Ubuntu install)
- Choose complete install (3rd choice beginning "Reinstall Ubuntu")
- Initial password: `p`
- Restart will prompt to remove USB

After restart:
- Install Updates and reboot
- Install drivers (none may be available)
- Create restore point in Timeshift
- Skip to "select dark theme" step
- Then try to Upgrade

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
- Connect Google Drive (check email for "google drive stuff")

---

## 3. Install Applications

For VS Code, GitHub, Plex, and PyCharm, see [INSTALL_24.04_Ubuntu.md](INSTALL_24.04_Ubuntu.md).

---

## 4. Serial Check

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
