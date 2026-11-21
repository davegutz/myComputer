# myComputer

GitHub repository to share installation instructions across many devices.
Created: Dave Gutz, 2024-Dec-25

> **Note:** For Google Drive (ocamlfuse) setup, the command requires a secret stored in davegutz2006 Gmail — search for "google-drive-ocamlfuse".

---

## Installation Guides

### Linux — Ubuntu / Pop!_OS / Lubuntu

| Guide | Hardware | OS | Purpose |
|-------|----------|----|---------|
| [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md) | HP Omen 15" 2022 | Ubuntu 24.04 LTS | Primary reference guide; Plex server |
| [INSTALL_24.04_PopOS_Dual_Boot](INSTALL_24.04_PopOS_Dual_Boot.md) | HP Omen 15" 2022 | Pop!_OS 24.04 COSMIC | Dual-boot with Windows |
| [INSTALL_24.04_Lubuntu](INSTALL_24.04_Lubuntu.md) | Lenovo Laptop | Lubuntu 24.04 | General workstation; LXQt desktop |
| [INSTALL_Ubuntu_Venus_Dual_Boot](INSTALL_Ubuntu_Venus_Dual_Boot.md) | Venus UM773 Lite | Ubuntu 22.04 LTS | Dual-boot with Windows 11 |
| [INSTALL_Windows_11_Venus](INSTALL_Windows_11_Venus.md) | Venus UM773 Lite | Windows 11 | Windows setup and apps |

### Linux — Other Distros

| Guide | Hardware | OS | Purpose |
|-------|----------|----|---------|
| [INSTALL_Linux_Lite](INSTALL_Linux_Lite.md) | Lenovo Laptop | Linux Lite | General workstation; Xfce desktop |
| [INSTALL_Linux_Lite_5fd6c4bf](INSTALL_Linux_Lite_5fd6c4bf.md) | Lenovo Laptop | Linux Lite | Archived earlier version |
| [INSTALL_Tiny_Core_Linux](INSTALL_Tiny_Core_Linux.md) | Lenovo Laptop / VM | Tiny Core Linux | Lightweight; primarily VirtualBox VM |

### Other

| Guide | Hardware | OS | Purpose |
|-------|----------|----|---------|
| [INSTALL_Ubuntu_Android](INSTALL_Ubuntu_Android.md) | Android device | Ubuntu | Ubuntu on Android environment |

### Feature & Application Guides

| Guide | Purpose |
|-------|---------|
| [INSTALL_secure_cam](INSTALL_secure_cam.md) | Security camera setup, motion detection, and motionEye web NVR |
| [INSTALL_Antigravity](INSTALL_Antigravity.md) | Google Antigravity CLI, IDE integration, and YOLO mode |
| [INSTALL_Chrome_Remote_Desktop](INSTALL_Chrome_Remote_Desktop.md) | Remote desktop access via Chrome |
| [INSTALL_noMachine](INSTALL_noMachine.md) | Remote desktop sharing via noMachine |
| [INSTALL_Google_Drive_Rclone](INSTALL_Google_Drive_Rclone.md) | Google Drive mounting via Rclone |
| [INSTALL_Google_Drive_Backup](INSTALL_Google_Drive_Backup.md) | Automated backup to Google Drive |
| [INSTALL_PuTTY](INSTALL_PuTTY.md) | PuTTY serial communication and terminal setup |
| [INSTALL_Alternate_Python](INSTALL_Alternate_Python.md) | Compiling alternate Python versions from source |
| [INSTALL_Python_Projects](INSTALL_Python_Projects.md) | Python development environment and venvs |
| [INSTALL_Lubuntu_Plasma](INSTALL_Lubuntu_Plasma.md) | KDE Plasma on Wayland migration & display management for Lubuntu |
| [INSTALL_pihole](INSTALL_pihole.md) | Pi-hole DNS ad-blocking server deployment via Docker |
| [INSTALL_visual_studio](INSTALL_visual_studio.md) | Visual Studio Code, Particle Workbench setup, extensions, and USB permissions |
| [INSTALL_gpu_screen_recorder](INSTALL_gpu_screen_recorder.md) | GPU Screen Recorder hardware-accelerated screencasting on Wayland |
| [INSTALL_chrome](INSTALL_chrome.md) | Google Chrome installation (AUR & deb) and performance/DNS tweaks |
| [INSTALL_claude_code](INSTALL_claude_code.md) | Claude Code CLI installation and Anthropic login |
| [INSTALL_Arduino](INSTALL_Arduino.md) | Arduino IDE, SAMD boards, libraries, and dark theme |
| [INSTALL_zoxide](INSTALL_zoxide.md) | Zoxide smart directory jumper installation and shell integration |

---

## Quick Reference

- **Starting fresh on Ubuntu?** → [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md)
- **Pop!_OS with COSMIC desktop?** → [INSTALL_24.04_PopOS_Dual_Boot](INSTALL_24.04_PopOS_Dual_Boot.md)
- **Lenovo laptop?** → [INSTALL_Lubuntu_24.04](INSTALL_Lubuntu_24.04.md)
- **Venus Mini PC?** → [INSTALL_Ubuntu_Venus_Dual_Boot](INSTALL_Ubuntu_Venus_Dual_Boot.md)
- **Windows setup?** → [INSTALL_Windows_11_Venus](INSTALL_Windows_11_Venus.md)

---

## Unified Linux Configuration Manager

To standardize shell configurations, terminal styling (Alacritty), dark themes, and aliases across Linux builds (Lubuntu, Ubuntu, Pop!_OS, CachyOS), see the **[myLinux Configuration Guide](../myLinux/README.md)**.
Initialize a new Linux build:
```bash
~/Documents/GitHub/myLinux/scripts/bootstrap.sh
```
