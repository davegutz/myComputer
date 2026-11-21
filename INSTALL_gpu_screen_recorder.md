# GPU Screen Recorder (Wayland Screencasting)

Traditional screencasters (such as `ffmpeg` using `x11grab` or SimpleScreenRecorder) only work on X11 and cause high CPU utilization on low-power processors. Under Wayland, standard X11 capture fails.

[GPU Screen Recorder](https://git.dec05eba.com/gpu-screen-recorder) captures directly from the GPU framebuffer via KMS (Direct Rendering Manager) or PipeWire desktop portal and encodes video with hardware acceleration (VA-API on AMD/Intel, NVENC on NVIDIA). This allows smooth 60 FPS recording with negligible CPU overhead.

---

## 1. Prerequisites

### Hardware Video Acceleration Drivers (VA-API)

- **Ubuntu / Debian / Lubuntu:**
  ```bash
  sudo apt update
  sudo apt install -y mesa-va-drivers vainfo
  vainfo   # verify driver reports VAProfileH264 / VAProfileHEVC support
  ```

- **Arch / CachyOS:**
  ```bash
  sudo pacman -S libva-utils mesa-vdpau
  vainfo
  ```

### Audio Monitoring

```bash
# Ubuntu / Debian / Lubuntu
sudo apt install -y pavucontrol

# Arch / CachyOS
sudo pacman -S pavucontrol
```

---

## 2. Installation

### Option A: Arch / CachyOS (Native Package)

```bash
sudo pacman -Sy gpu-screen-recorder
# Optional GUI wrapper:
sudo pacman -S gpu-screen-recorder-gtk
```

### Option B: Ubuntu / Debian / Lubuntu via Flatpak (Includes GUI)

Ensure `flatpak` is installed and Flathub configured:

```bash
sudo apt update
sudo apt install -y flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

Install GPU Screen Recorder system-wide (allows acquiring Polkit capture permissions):

```bash
flatpak install flathub com.dec05eba.gpu_screen_recorder
```

**Launch GUI:**
- Open **GPU Screen Recorder** from the application menu, or
- Run in terminal:
  ```bash
  flatpak run com.dec05eba.gpu_screen_recorder
  ```

---

## 3. Usage & Compositor Notes

### Encoder Selection
- Set Video Codec to **VAAPI** (or **Auto**) for AMD Radeon / Intel GPUs.
- Set Video Codec to **NVENC** for NVIDIA GPUs.

### Wayland Desktop Portals vs KMS Capture
- **KMS Direct Capture:** On startup under standard Wayland sessions, GPU Screen Recorder may prompt for root authentication (`pkexec` / Polkit) to capture directly from the KMS display plane for maximum performance.
- **COSMIC Wayland Portal (HP Omen / Hybrid Graphics):** On COSMIC desktop (`cosmic-comp`) or laptops with hybrid AMD/NVIDIA graphics, set the capture target to **`portal`** (ScreenCast portal) rather than KMS. This avoids direct KMS display plane capture which can cause atomic modesetting lockups that prevent the PC from going to sleep/suspend.

### Audio Loopback Capture
In `GUI_screencast` / `myPyScreencast`:
- Set Audio device to `alsa_output.Loopback.monitor` to cleanly record internal application audio without microphone noise.

### CLI Recording Example

```bash
# Record full screen at 60 FPS with default system audio output:
gpu-screen-recorder -w screen -f 60 -a "default_output" -o ~/Videos/screencast.mp4

# Stop recording cleanly:
# Press Ctrl + C in the terminal
```
