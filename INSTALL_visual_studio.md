# Visual Studio Code Installation & Particle Workbench Setup

## 1. Installation

### Arch / CachyOS

Install official binary from the AUR:

```bash
sudo pacman -S --needed base-devel git
sudo pacman -S perl-archive-zip  # avoid crc32 error
git clone https://aur.archlinux.org/visual-studio-code-bin.git
cd visual-studio-code-bin
makepkg -si
```

### Ubuntu / Debian / Lubuntu

> **Warning:** Do **NOT** install using `snap` (`snap install code --classic`) or Flatpak — containerized sandboxing breaks Particle build tools and compiler toolchains. Use the official `.deb` package.

```bash
# Download .deb from https://code.visualstudio.com/docs/?dv=linux64_deb
sudo gdebi ./Downloads/code_*.deb

# Provides crc32 — Particle Workbench needs it:
sudo apt install -y libarchive-zip-perl
```

---

## 2. Extensions & Workspace Setup

1. Open VS Code and install extensions:
   - **Workbench** (for Particle)
   - **Antigravity CLI Launcher** (for Gemini)
2. Open the **`SOC_PARTICLE`** folder (open the root project folder, not `src`).
3. Sign into Particle ASAP.

---

## 3. Particle CLI Configuration

In VS Code (or terminal):
- Open Particle CLI: Press `Ctrl+Shift+P` → **Particle: Launch CLI**
- Run:
  ```bash
  particle usb configure
  ```

---

## 4. USB Device Permissions & Udev Rules (Particle Devices)

If you encounter: *FAQ: Missing permissions to access the USB device.*

### Group Setup

```bash
sudo groupadd -g 46 plugdev
sudo usermod -aG plugdev,uucp $USER
```

### Udev Rules

Create `/etc/udev/rules.d/50-particle.rules`:

```bash
sudo nano /etc/udev/rules.d/50-particle.rules
```

Paste the following rules:

```udev
# Particle Devices (Photon, Electron, Argon, Boron, Xenon, Neon, etc.)
SUBSYSTEMS=="usb", ATTRS{idVendor}=="2b04", ATTRS{idProduct}=="0006", MODE="0666", GROUP="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="2b04", ATTRS{idProduct}=="0008", MODE="0666", GROUP="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="2b04", ATTRS{idProduct}=="000c", MODE="0666", GROUP="plugdev"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="2b04", ATTRS{idProduct}=="000d", MODE="0666", GROUP="plugdev"

# Particle Debugger
SUBSYSTEMS=="usb", ATTRS{idVendor}=="2b04", ATTRS{idProduct}=="0010", MODE="0666", GROUP="plugdev"
```

Reload and trigger udev rules:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Log out and log back in (or reboot) for group memberships to take effect.
