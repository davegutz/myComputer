# Installing Windows 11 on Venus

**Hardware:** MINISFORUM Venus Series UM773 Lite Mini PC
- Processor: AMD Ryzen 7 7735HS with Radeon Graphics × 16
- Memory: DDR5-4800 32 GB
- Storage: 1 TB PCIe 4.0 SSD
- Graphics: Radeon 680M
- Ports: 2×4K HDMI, 1×8K USB4, 2.5 Gbps LAN
- Purchase: 2/18/2024 (Amazon)
- Manufacturer: Micro Computer (HK) Tech Limited
- BIOS: F7 (repeatedly)

**OS:** Windows 11 Home (Product ID: 00356-07420-83374-AAOEM)

---

## Table of Contents

- [1. Preparation](#1-preparation)
- [2. Install Windows 11](#2-install-windows-11)
- [3. Cleanup and Settings](#3-cleanup-and-settings)
- [4. Applications](#4-applications)
- [5. License Keys](#5-license-keys)
- [6. DVD / ISO Burning](#6-dvd--iso-burning)
- [7. VS Code for Arduino](#7-vs-code-for-arduino)
- [8. Performance Tuning](#8-performance-tuning)
- [9. Troubleshooting Windows Update Errors](#9-troubleshooting-windows-update-errors)
- [10. Tools and Utilities](#10-tools-and-utilities)
- [11. LTSpice Setup](#11-ltspice-setup)
- [12. Overheating Fixes](#12-overheating-fixes)

---

## 1. Preparation

- Deauthorize licenses before reinstalling:
  - DVDFab: deauthorize `davegutz@alum.mit.edu`
  - WinXDVD: remove license
  - ePubor: Tools → License Manager → Deregister
- Unplug Seagate backup drive and USB backup stick

---

## 2. Install Windows 11

Create install media:
- https://www.microsoft.com/en-us/software-download/windows10 → Download Now
- Double-click media creation tool → Create USB media for another PC

Boot times (reference: HP-OMEN 2022, 8-core 4 GHz 64 GB):

| Time | Step |
|------|------|
| 00:08 | F9 → Custom install. Pick Pro, use Pro key (`8BTNH-9VCJM-B29XV-8KFFB-43KTR`) when flagged |
| 00:08 | Allow network discovery — `OurHappyHomeGuest5g` |
| 00:15 | Computer name: `DavesHP-OMEN` / `davegutz@alum.mit.edu` |
| 00:27 | Firefox: sign in |
| 00:41 | Check for updates — install and reboot until clean |
| 01:00 | HP Support Assistant 9 (optional) |
| 01:07 | AMD Adrenaline app (optional) |
| 01:14 | GeForce Experience app (optional) |
| 01:24 | Check for updates again; do not accept optional Windows drivers |
| 01:32 | Create a restore point |

For Win11: choose to install **Pro**.

---

## 3. Cleanup and Settings

- Manage Advanced Sharing Settings: turn on all including non-guest
- Use `ourHappyHome5g` (not guest) so file sharing works
- Startup apps: cleanup (remove unnecessary entries)
- Uninstall Microsoft OneDrive (leave path for OneNote)
- Quit Teams (from system tray)
- Power Options: Turn off hard disk — **Never** (both battery and plugged in)
- Downloads: View Extensions, Show Hidden files
- Start → Run `netplwiz` → Advanced → Ctrl+Alt+Del

**Omen Gaming Hub:** Ctrl+Shift+Esc → Startup → set to autostart.

---

## 4. Applications

```
notepad++
7-zip
OBS
zoom                  sign in using Google
cygwin                vt, just defaults
caffeine (PowerToys)  look for free version online
python 3.12.2         non-admin install, add to PATH, don't disable path length limit
ffmpeg                → C:\ffmpeg
```

**Environment Variables** — add to user PATH:
```
C:\ffmpeg\bin
```

Restart for environment variables to take effect.

```
github                sign in online; clone myStateOfCharge and fwgWhisper
git                   all defaults
libreoffice
google drive
vb-audio virtual cable   (no restart required)
jetbrains pycharm community   quit JetBrains Toolbox from tray; remove from startup
R + RStudio
noMachine             https://www.nomachine.com/
```

**Default apps:** Firefox, VLC, paint.net, Sketchup

**puTTY setup:** per `myStateOfCharge/SOC_Particle/putty/sessions/*.odt`

**pyCharm - screencast:** get to run

**pyCharm - movie-scraper:**
- Use `PySimpleGUI-4-foss` instead of `PySimpleGUI`

**pyCharm - SOC_Particle:**
- `SOC_Particle\py\GUI...` get to run
- VS Code: Codeium AI (login via Google), Ruff, Python, Workbench

Create another restore point.

---

## 5. License Keys

**Epubor Ultimate:**
- Licensed email: `davegutz@alum.mit.edu`
- Download: https://download.epubor.com/epubor_ultimate.exe
- Registration code: `RFVTLU7-7ZT3KW-9C5D69-4FSHUS-S5EZDQ7`
- Let Epubor install Kindle for PC

**DVDFab:** `davegutz@alum.mit.edu` / `ste_` (no need to contact them)

**WinXDVD:** `davegutz@alum.mit.edu` / `AAQPS-JODOK-U66T2-CCQSU` (contact them if unable to deauthorize before reinstall)

Other software:
- `vlc`
- `LTspice` (upgrading to version 24)
- `kindle`
- `jre`
- `sketchupmake 2017`
- `sharex` (from Store, for screenshots)
- `clipgrab` from https://clipgrab.org/
- `paint.net` from https://www.dotpdn.com/downloads/pdn.html

Optional (for laptop with Rigol): `ultrasigma`, `ultrascope`
- https://www.rigolna.com/download/ → UltraSigma Instrument Connectivity Driver

---

## 6. DVD / ISO Burning

ISO burning disappeared from right-click menu — restore it:

1. Right-click the file → Open With → Choose another app → More apps
2. Scroll to bottom → Look for another app on this PC
3. Browse to `C:\Windows\System32` and select `isoburn.exe`
4. Click Open → select **Always** to remember

---

## 7. VS Code for Arduino

See https://forum.allaboutcircuits.com/threads/how-to-setup-and-use-vs-code-windows-for-arduino-programming.193422/

Install **Arduino Community Edition** extension (circle with Arduino in middle).

```bash
# Plug in a board and restart VS Code
# Select Programmer in bottom bar (Nano is a SAM board)
# Use Arduino IDE to install libraries — VS Code finds them automatically
```

Install `mingw` from https://www.msys2.org/ for C++ compilation:

```bash
gcc --version   # verify
# RESTART VS Code
```

**VSCodium** (alternative):
- https://dev.to/abdullah_alazmi_12/how-to-install-vscodevscodium-166h
- Install `tdm-gcc-64`
- Use `clangd` C++ extension (700k+ installs)
- Also: `C/C++ Runner`, `CodeLLDB`, `C/C++ Compile Run`, `clangd:CMake integration`

**Arduino CLI:**

```bash
sudo snap install arduino-cli
arduino-cli config dump
arduino-cli config init
arduino-cli lib list
```

In Arduino Community Edition settings → `Arduino:Path` → path to CLI.

---

## 8. Performance Tuning

### DNS Speed

Turn off automatic DNS for WiFi (IPv4 and IPv6):
- IPv4: `8.8.8.8` (preferred), `8.8.4.4` (alternate)
- IPv6: `2001:4860:4860::8888`, `2001:4860:4860::8844`
- Apply and restart WiFi

**Firefox tweaks** (`about:config`):
```
layers.acceleration.force-enabled = true
gfx.webrender.all = true
browser.sessionstore.interval = 150000
```

**Chrome tweaks** (`chrome://settings/system`):
- Toggle on "Use hardware acceleration when available" → Relaunch

### Windows Background Services

Disable unnecessary services to boost performance:
https://www.xda-developers.com/disable-windows-background-services-boost-performance/

### Disable Search Indexer (battery life)

`Win+R` → `services.msc` → Windows Search → Properties → Startup: Disabled → Stop → Restart

Then install:
- **Everything** (fast file search)
- **grepwin**
- **pdfsam basic** from https://pdfsam.org/download-pdfsam-basic/

### Windows Explorer Add-ons

- **TeraCopy** — https://www.codesector.com/downloads (freeware)
- **Peek** (PowerToys) — `Ctrl+Space`
- **Dropit**
- **Image Resizer** (PowerToys)
- **Power Rename** (PowerToys)

On laptop: fractionally scale display to 125%.

### MS Services (optional disable list)

https://www.xda-developers.com/disable-windows-background-services-boost-performance/

### Wintoys

Run and check settings.

### Crystal Disk Info

https://sourceforge.net/projects/crystaldiskinfo/

### Bootracer

https://greatis.com/bootracer/download.htm

Disabled services and observed boot times:
- Baseline: ~35 s
- After disabling print spooler: ~70 s (regression — not recommended)
- After disabling mobile hotspot: ~47 s
- After disabling error reporting: ~44 s
- After disabling SysMain (Superfetch): ~53 s

---

## 9. Troubleshooting Windows Update Errors

### Error 0x80070002

**Method 1: Windows Update Troubleshooter**

Settings → System → Troubleshoot → Other Troubleshooters → Windows Update → Run

**Method 2: Reset Windows Update Components** *(worked 8/2025)*

Run Command Prompt as Administrator:

```cmd
net stop wuauserv
net stop cryptSvc
net stop bits
net stop msiserver
ren C:\Windows\SoftwareDistribution SoftwareDistribution.old
ren C:\Windows\System32\catroot2 catroot2.old
net start wuauserv
net start cryptSvc
net start bits
net start msiserver
```

**Method 3: Check Date and Time**

Settings → Time & Language → Date & Time → Toggle on auto time zone and auto time → Sync now

**Method 4: DISM and SFC**

```cmd
DISM /Online /Cleanup-Image /RestoreHealth
sfc /scannow
```

**Method 5: Manual Update Download** *(worked for 24H2 update)*

Settings → Windows Update → Update History → find KB number → search Microsoft Update Catalog → download and install

**Method 6: Registry Configuration**

`Win+R` → `regedit` → Navigate to:
`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings`

Check/modify:
- `FlightSettingsMaxAttemptCount` → set to ~3
- `FlightSettingsMaxFailures` → set to ~2

Back up keys before modifying (File → Export).

### Enable BSOD Fix Tool

Settings → Recovery → Quick Machine Recovery

---

## 10. Tools and Utilities

**DupeGuru** — https://dupeguru.voltaicideas.net/

**Affinity (Photoshop replacement)** — https://www.affinity.studio/

**fix movie_Scraper** (if Cinemagoer breaks due to IMDb changes):

```bash
pip install git+https://github.com/cinemagoer/cinemagoer
```

Open terminal console in PyCharm (looks like `>_`) and run this command.

---

## 11. LTSpice Setup

Install **LTSpice v24**: https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html

### Installing TI OPA333 Model

1. Copy `OPAx333.LIB` to:
   ```
   C:\Users\daveg\AppData\Local\LTspice\lib\sub
   ```

2. In LTspice: File → Open → navigate to `OPAx333.LIB` → select "All Files"

3. Find the `.SUBCKT OPAx333` line → right-click → **Create Symbol**

4. Save symbol to:
   ```
   C:\Users\YourUserName\Documents\LTspiceXVII\lib\sym\AutoGenerated\
   ```

5. Restart LTspice → open schematic → F2 → find in AutoGenerated folder

**Alternative:** Place a generic `opamp2` symbol, add `.lib OPAx333.LIB` SPICE directive, right-click the symbol → change Value to the subcircuit name.

**TI OPA333 resource:** https://www.ti.com/product/OPA333

---

## 12. Overheating Fixes

The HP Omen liked to overheat and throw Error 41 BSODs. In addition to fan cooling schedule changes:

- Power Options → Advanced → Processor Power Management:
  - Maximum processor state (plugged in): **99%**
  - Maximum processor state (battery): **95%**
- Use **Balanced** power plan

Reference: https://www.makeuseof.com/i-finally-fixed-my-noisy-overheating-laptop-with-this-simple-change/
