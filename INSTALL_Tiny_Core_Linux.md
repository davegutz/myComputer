# Installing Tiny Core Linux

**Hardware:** Lenovo Laptop
**OS:** Tiny Core Linux (CorePlus)
**Purpose:** Lightweight Linux, primarily in a VM

> Tiny Core is a unique, ultra-minimal distro.

---

## Table of Contents

- [1. Create Install USB](#1-create-install-usb)
- [2. Install in VirtualBox VM (Windows)](#2-install-in-virtualbox-vm-windows)
- [3. Install on Physical Machine (Linux)](#3-install-on-physical-machine-linux)

---

## 1. Create Install USB

Format USB to FAT32 on Linux:

```bash
sudo mkfs.vfat -I /dev/sda -n TINYCORE
```

Then reformat to FAT32 in Windows.

**Alternative methods (may encounter MBR access denied errors):**

- UNetbootin "Diskimage" version from http://unetbootin.github.io/
- `core2usb` from https://sourceforge.net/p/core2usb/wiki/Home/

  ```bash
  # On Windows, run core2usb-16.py (in same folder as this file)
  # with CorePlus ISO: http://tinycorelinux.net/11.x/x86/release/CorePlus-current.iso
  # Make sure 7-zip is installed on Windows to extract from .iso
  ```

**Create USB on Linux with `dd`:**

```bash
cd Downloads
lsblk   # identify the USB device
sudo dd if=CorePlus-current.iso of=/dev/sdX status=progress   # replace X with lsblk result
```

**Ventoy** is another option for Linux USB creation.

---

## 2. Install in VirtualBox VM (Windows)

### Prerequisites

Download and install:
- Python from https://www.python.org/downloads/

  ```cmd
  # As administrator:
  py -m pip install pywin32
  python.exe -m pip install --upgrade pip
  ```

- VirtualBox from https://download.virtualbox.org/virtualbox/7.1.4/
- VirtualBox Extension Pack (same URL)
- Guest Additions (same URL)

Open VirtualBox, add extensions, then create a new VM:

1. Machine → New → select the CorePlus ISO
2. Settings:
   - 4 GB RAM
   - 20 GB disk
   - 1 CPU
3. General → Advanced → Bidirectional clipboard

### Install Process

Start VM and choose: **Boot Core with X/GUI (TinyCore) + Installation Extension**

Following https://eaglepubs.erau.edu/mastering-enterprise-networks-labs/chapter/installing-tiny-core-linux/

1. Once live, click Install in LRC
2. Pick 'whole', highlight 'sda', 'install boot loader' → right arrow
3. `ext4` → right arrow
4. Boot options: type `home=sda1 opt=sda1` → right arrow
5. Choose wifi: all three boxes
6. Continue right with defaults → **Proceed** → shut down the machine

### After Install

In VM Settings: Storage → remove the ISO attachment (forces boot from virtual hard disk).

On next startup:
- Devices → Insert Guest Additions
- Choose wifi + firmware

### WiFi in terminal

```bash
wifi-menu
```

---

## 3. Install on Physical Machine (Linux)

Download CorePlus from http://tinycorelinux.net/

```bash
cd Downloads
lsblk   # identify the USB device
sudo dd if=CorePlus-current.iso of=/dev/sdX status=progress
```

**VM notes:**
- New VM with CorePlus ISO
- 20 GB hard drive, 2 GB RAM
- Boot: **Core with Wifi & Firmware**
- VirtualBox network: Attached to NAT or Bridged Adapter
