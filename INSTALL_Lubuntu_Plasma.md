# Moving from GNOME / X to Plasma / Wayland (Lubuntu)

> **Hardware Recommendation:** Moving to KDE Plasma is recommended for **powerful PCs only**. Specifically, do **NOT** install this on resource-constrained machines like Lenovo 4 GiB RAM laptops; maintain the lightweight default LXQt environment on those machines to avoid memory exhaustion.

Migrating from GNOME or LXQt under X11 to KDE Plasma on Wayland provides modern display protocol benefits, tear-free rendering, smoother scaling, and native hardware-accelerated screencasting (via KMS and PipeWire).

## 1. Install Plasma & Wayland Packages

Install the KDE Plasma desktop, Wayland session compositor integration, SDDM configuration modules, and Wayland clipboard utilities:

```bash
sudo apt update
sudo apt install -y plasma-desktop plasma-workspace-wayland
sudo apt install -y kde-config-sddm sddm-kcm
sudo apt install -y wl-clipboard  # replaces xclip / xsel for terminal clipboard (wl-copy, wl-paste)
```

## 2. Configure SDDM for Wayland

Switch the default display manager from GDM3 to SDDM, and configure SDDM to run natively on Wayland rather than launching an X11 server for the login greeter:

```bash
# Set SDDM as the system default display manager:
sudo dpkg-reconfigure sddm
# Select 'sddm' when prompted

# Disable gdm3 to prevent dual display manager service conflicts:
sudo systemctl disable gdm3

# Create SDDM Wayland drop-in configuration:
sudo mkdir -p /etc/sddm.conf.d
sudo nano /etc/sddm.conf.d/10-wayland.conf
```

Add the following configuration:
```ini
[General]
DisplayServer=wayland
GreeterEnvironment=QT_WAYLAND_SHELL_INTEGRATION=layer-shell

[Wayland]
CompositorCommand=kwin_wayland --no-lockscreen
```

Restart SDDM (or reboot) to load the Wayland greeter:
```bash
sudo systemctl restart sddm
# Or reboot:
sudo reboot
```

*(Optional)* Configure automatic login to Plasma Wayland:
```bash
sudo nano /etc/sddm.conf
```
```ini
[Autologin]
User=daveg
Session=plasmawayland
```

## 3. Display Management & HDMI Reset (`kscreen-doctor` vs `xrandr`)

Under X11, `xrandr` was used to wake up or cycle modes on HDMI displays:
```bash
# X11 old method (does NOT change native modes under Wayland):
DISPLAY=:0 xrandr --output HDMI-A-1 --mode 1024x768; sleep 1; DISPLAY=:0 xrandr --output HDMI-A-1 --auto
```

Under Wayland, `xrandr` only affects Xwayland client surfaces. Use KDE's CLI display tool **`kscreen-doctor`**:

```bash
# List all connected outputs and available mode numbers/resolutions:
kscreen-doctor -o

# Force display cycle / mode re-sync on HDMI-A-1:
kscreen-doctor output.HDMI-A-1.mode.1024x768@60; sleep 1; kscreen-doctor output.HDMI-A-1.mode.auto
```

### Reconfiguring KScreen & Restarting Plasma Shell (without reboot)
If the desktop shell or display daemon needs a reload:
```bash
# Restart Plasma Shell:
systemctl --user restart plasma-plasmashell.service

# Trigger KScreen reconfigure via D-Bus:
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
qdbus org.kde.kded5 /kded org.kde.kded5.loadModule kscreen
SSH_AUTH_SOCK="" qdbus org.kde.KScreen /org/kde/KScreen reconfigure
```

## 4. Wayland-Native Screen Recording

Legacy X11 grab tools (`ffmpeg -f x11grab`, `SimpleScreenRecorder`) fail under Wayland. Use Wayland-native recorders:

```bash
# GPU Screen Recorder (recommended for hardware VA-API / NVENC capture):
sudo apt install -y gpu-screen-recorder
# Or install via Flatpak:
flatpak install flathub com.dec05eba.gpu_screen_recorder

# wf-recorder (lightweight CLI recorder for Wayland/PipeWire):
sudo apt install -y wf-recorder
```
*See [INSTALL_gpu_screen_recorder](INSTALL_gpu_screen_recorder.md) for detailed setup and usage.*

## 5. Session Verification & Environment Variables

Verify your running session:
```bash
echo $XDG_SESSION_TYPE       # Should return 'wayland'
echo $WAYLAND_DISPLAY        # Usually 'wayland-0'
echo $XDG_CURRENT_DESKTOP    # Should return 'KDE'
ls /run/user/$(id -u) | grep wayland
```

To ensure Qt and GTK applications prefer native Wayland rather than falling back to Xwayland, ensure the following are set in `~/.bashrc` or `/etc/environment`:
```bash
export QT_QPA_PLATFORM="wayland;xcb"
export GDK_BACKEND="wayland,x11"
export MOZ_ENABLE_WAYLAND=1
```

Make sure Lib mounts on boot
```bash
echo "UUID=e8fdea26-3474-417c-a1cf-73b7c2725a92 /media/daveg/Lib ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab
```

## 6. Power Management, Screen Locking & Shortcuts

- **Screen Locking:** Replace X11-dependent tools (`xsecurelock`, `xautolock`, `xscreensaver`) with Plasma's native screen lock. Configure in **System Settings → Screen Locking** (`kscreenlocker`).
- **Keyboard Mappings:** `xmodmap` does not affect native Wayland applications. For custom keys (such as backlight toggle on Scroll Lock), configure shortcuts via **System Settings → Shortcuts** or create `udev` / `hwdb` rules.
- **Session Cleanup:**
  ```bash
  # Terminate any lingering user session when switching managers:
  sudo loginctl terminate-user $USER
  ```
