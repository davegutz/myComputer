# Installing Pop!_OS 24.04 (Dual Boot with Windows)

**Hardware:** HP Omen (or similar)
**OS:** Pop!_OS 24.04 with COSMIC desktop (X11/Xorg)
**Purpose:** General workstation, dual-boot alongside Windows

> Pop!_OS uses the COSMIC desktop in 24.04.
> Flatpak (COSMIC Store) sandboxes apps like VS Code and PyCharm — use `.deb` or `snap` instead.
> For Python project notes (movie_Scraper, SOC, etc.), see [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md).

---

## Table of Contents

- [1. Preparation](#1-preparation)
- [2. Boot and Install](#2-boot-and-install)
- [3. EFI Boot Menu](#3-efi-boot-menu)
- [4. Initial Setup](#4-initial-setup)
- [5. Install Applications](#5-install-applications)
- [6. VS Code](#6-vs-code)
- [7. PyCharm and Python](#7-pycharm-and-python)
- [8. Sound Configuration](#8-sound-configuration)
- [9. Google Drive (Rclone)](#9-google-drive-rclone)
- [10. Claude Code](#10-claude-code)
- [11. Dual-Boot Time Sync](#11-dual-boot-time-sync)
- [12. Cleanup](#12-cleanup)
- [13. COSMIC Desktop Tips](#13-cosmic-desktop-tips)
- [14. Utilities](#14-utilities)
- [15. Work in Progress](#15-work-in-progress)

---

## 1. Preparation

- Phone ready to approve Google requests and USB tethering if needed
- Make space for Linux using Windows Disk Management utility:
  - **Shrink Windows partition by ~350,000 MB** on a 1 TB drive
  - Note partition numbers
- Have a >4 GB thumbdrive
- On Windows: download the ISO and flash using **balenaEtcher**
- Turn off BitLocker on all drives
- Deauthorize tools like DVDfab, WinXDVD, ePubor
- Unplug second monitor and extra USB devices (may leave mouse and keyboard)
- **Create a Windows restore point**
- Save GitHub repos on Windows

---

## 2. Boot and Install

Insert ISO USB and boot:
- **F10** on HP-Omen, **F12** on Lenovo, **F7** on little_guy
- Set boot order to USB

Choose **"Try or install Ubuntu"** — allow ~3 minutes.

Partition setup (Custom / GParted):

| Partition | Size | Type | Mount |
|-----------|------|------|-------|
| p6 | 31 GB | pri/ext4 | (name: 'custom' in GParted) |
| p7 | 22 GB | swap | |
| p8 | 2 GB | EFI | `/boot` (large enough to hold both Windows and Pop) |
| p9 | remaining | ext4 | `/root` |

Username: `daveg`

Wait ~12 minutes for install. When prompted to reboot, leave USB in until prompted to remove it.

> If **"Install"** menu item is grayed out: verify FAT32 and other settings, then restart with USB still in and try again.

---

## 3. EFI Boot Menu

After first boot:

```bash
sudo apt update
sudo apt install refind   # accept all the dangerous-looking options
```

This installs the rEFInd boot manager to make the EFI boot menu work properly with dual boot.

---

## 4. Initial Setup

From Pop!_Shop install:
- `brasero`
- `caffeine` (the one with steam rising)
- `vlc` (open and turn off hardware acceleration)
- `GitHub Desktop`
- `Synaptic`
- `Notepad Next`

```bash
sudo snap install snapd
# Log out / log back in — IMPORTANT! IT WILL WORK IF YOU DO THIS
sudo apt update && sudo apt upgrade
```

**Firefox Performance:**
```
about:config
browser.sessionstore.interval = 150000
```

---

## 5. Install Applications

```bash
sudo apt install -y fuse libfuse2          # AppImage support
sudo apt install -y ffmpeg
sudo apt install -y git
sudo apt install --fix-missing -y python3-pip
sudo apt install -y python3-tk             # for PyCharm
sudo apt install -y dhcpcd5
sudo apt install dos2unix
sudo apt install xsel
sudo apt install -y thunar
sudo apt install -y nautilus
sudo apt install -y pavucontrol            # for myPyScreencast
sudo apt-get install libxkbcommon-dev      # for just

# Create missing .Xauthority file (if needed):
touch ~/.Xauthority && ls -la ~/.Xauthority
```

**PuTTY** (follow Ubuntu instructions):

```bash
# Add user to dialout group for serial access:
sudo adduser daveg dialout
# Log out and log back in
```

**Firewall:**

```bash
sudo ufw enable
sudo ufw status
```

---

## 6. VS Code

> **Do NOT install using snap or flatpak (COSMIC Store)** — these sandbox VS Code and it won't build.

```bash
# Download .deb from https://code.visualstudio.com/docs/?dv=linux64_deb
sudo gdebi ./Downloads/code_1.112.0-1773778351_amd64.deb
```

Start Code and install extensions.

---

## 7. PyCharm and Python

> Flatpak (used in Pop!_OS) causes path errors — PyCharm cannot find custom Python builds in `/usr/local/bin`.
> **Uninstall the flatpak version and use snap instead.**

```bash
# Uninstall any existing flatpak version first
sudo snap install --classic pycharm-community
```

For alternate Python version, see [INSTALL_24.04_Ubuntu](INSTALL_24.04_Ubuntu.md).

---

## 8. Sound Configuration

```bash
sudo nano /etc/modules-load.d/modules.conf
# Add:
snd-aloop

# Load for this session:
sudo modprobe snd-aloop
```

Alternatively, plug in a USB headset and adjust sound in GUI.

---

## 9. Google Drive (Rclone)

**Install Rclone:

```bash
sudo apt install rclone
rclone config
```
Follow the prompts:

        Enter n to create a new remote.
        e/n/d/r/c/s/q>  n
        name>  gdrive
        Option Storage:  find Drive (usually 18)
        client:id>  
        client_secret>  
        scope>  1
        service_account_file>  
        Edit Advanced config?
        y/n>  y
          oauth Access Token:    https://myaccount.google.com/apppasswords  name it Rclone  "epep hdvf omwc bnxy"
          auth_url>  
          token_url> 
          root_folder_id>  
          auth_owner_only>  
          use_trash>  
          copy_shortcut_content>  
          skip_gdocs>  
          skip_checksum_gphotos>  
          shared_with_me>  
          trashed_only>  
          starred_only>  
          export_formats>  
          import_formats>  
          allow_import_name_change>  
          list_chunk>  
          impersonate>  
          upload_cutoff> 1G
          chunk_size>  
          acknowledge_abuse>  
          keep_revision_forever>  
          v2_download_min_size>  
          pacer_min_sleep>  
          pacer_burst>  
          server_side_across_configs>  
          disable_http2>  
          stop_on_upload_limit>  
          stop_on_download_limit>  
          skip_shortcuts>  
          skip_dangling_shortcuts>  
          resource_key>  
          encoding>  

          Edit advanced config? blank

          Already have a token - refresh?  blank

          Use auto config?
          y/n>  y
            Complete the authentication process in your web browser, allowing Rclone access to your Google Drive.
            Return to the terminal

          Configure this as a Shared Drive (Team Drive)? n (blank)
          y/n>  n (blank)

      Keep this "gdrive" remote?
      y/e/d> y (blank)  

    Exit the configuration wizard by typing q
    e/n/d/r/c/s/q> q

**Mount Google Drive:**

```bash
mkdir ~/gdrive
rclone mount gdrive: ~/gdrive &
```

**Auto-start rclone on login:**

Add startup application: `"gdrive"` with command `"rclone mount gdrive: ~/gdrive &"`

OR

```bash
mkdir -p ~/bin
cat << EOF > ~/bin/Rclone
#!/bin/bash
# rclone mount gdrive: ~/gdrive &
rclone mount gdrive: ~/gdrive \
  --vfs-cache-mode full \
  --vfs-cache-max-size 50G \
  --vfs-cache-max-age 24h \
  --dir-cache-time 1000h \
  --drive-chunk-size 128M \
  --buffer-size 64M \
  --poll-interval 15s \
  --multi-thread-streams 4 \
  --tpslimit 5 \
  --tpslimit-burst 5 \
  --daemon \
  &
EOF
chmod +x ~/bin/Rclone

mkdir ~/.config/autostart
cat << EOF > ~/.config/autostart/rclone.desktop
[Desktop Entry]
Name=rclone
Exec=/home/daveg/bin/Rclone
Terminal=false
Type=Application
X-Desktop-File-Install-Version=0.27
EOF
chmod +x /home/daveg/.config/autostart/rclone.desktop
```

Test the autostart entry:

```bash
gio launch ~/.config/autostart/rclone.desktop
# or
sudo apt install dex
dex ./.config/autostart/rclone.desktop
```

Test the autostart entry:

```bash
gio launch ~/.config/autostart/rclone.desktop
# or
sudo apt install dex
dex ./.config/autostart/rclone.desktop
```

---

## 10. Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
claude --version   # verify
claude             # log in to Anthropic
```

---

## 11. Dual-Boot Time Sync

Fix clock discrepancy when switching between Linux and Windows:

```bash
timedatectl set-local-rtc 1 --adjust-system-clock
```

---

## 12. Cleanup

```bash
sudo passwd daveg     # ignore warnings
sudo passwd           # root
rm ~/.local/share/keyrings/login.keyring
sudo apt update
sudo apt -y upgrade
sudo apt -y autoremove
sudo apt autoremove
sudo apt autoclean
sudo apt clean
sudo apt install deborphan
sudo apt remove $(deborphan)
```

---

## 13. COSMIC Desktop Tips

### Disable trackpad

Settings → Input Devices → Keyboard → Keyboard Shortcuts → System → **"Toggle touchpad"** → assign a key (e.g., `Super+F9`).

### Ignore lid closure

```bash
sudo nano /etc/systemd/logind.conf
# Set:
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
```

Restart.

### caffeine applet for COSMIC

See https://github.com/tropicbliss/cosmic-ext-applet-caffeine and follow the README.

---

## 14. Utilities

```bash
sudo apt install fzf        # fuzzy find
sudo snap install tldr      # quick command help
sudo apt install mtr        # traceroute tool
sudo apt install ripgrep    # fast grep
```

---

## 15. Work in Progress

### Clean SOC_Particle Clone

```bash
git clone --depth 1 https://github.com/davegutz/mySolarStateOfCharge
# Re-add to GitHub Desktop:
# Repository → Add → Add existing repository
```


### GitHub CLI

```bash
gh auth login
gh auth token
```


### Git Maintenance

```bash
git gc --aggressive --prune=now
git status
git add --all
git commit
```

### Speed up Git and GitHub
 # Pack loose objects (will dramatically speed up git status/index operations)
  git -C ~/Documents/GitHub/myLifeSaver gc
  git -C ~/Documents/GitHub/mySolarStateOfCharge gc


### Reliable WiFi (DNS Fix)

If WiFi drops or DNS resolution fails (especially with competing hotspots):

```bash
sudo nano /etc/systemd/resolved.conf
# Add:
DNS=8.8.8.8 8.8.4.4
FallbackDNS=1.1.1.1 1.0.0.1
```

This ensures DNS works globally regardless of what NetworkManager does per-interface.


## GNOME and X11

https://www.reddit.com/r/pop_os/comments/1pzy02f/installing_gnome_on_pop_os_2404/

```bash
sudo apt install gnome-session gnome-shell-extension-manager
# choose gdm3 greeter.
```

Later you can change greeter to cosmic-greeter by
```bash
sudo dpkg-reconfigure cosmic-greeter
# or
sudo dpkg-reconfigure gdm3
```

There are more setup suggestions in the link if issues.  This is a bare bones.  It doesn't have an application launcher so:

```bash
sudo apt install gnome-core
```

Optionally to make the gnome-terminal as default need the following:
```bash
sudo update-alternatives --config x-terminal-emulator
```

Install Pop Theme
```bash
sudo apt install pop-theme gnome-tweaks
```

To use cosmic apps:
	Use cosmic store to install 'Tweaks'
	Launch tweaks - Color schemes - Available search Adwaita - install - refresh - Installed (last thing verifies)

Install Pop Shell
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```
Close terminal then reopen  (Important!!)
```bash
nvm install node
npm install -g typescript
cd ~/Downloads
git clone https://github.com/pop-os/shell.git
sudo apt install git node-typescript make.
cd ~/Downloads/shell
make local-install
```

Log out and log back in to cosmic.  Install extension manager.
```bash
flatpak install --user flathub com.mattjakeman.ExtensionManager
```
Launcher - search 'extens...' pick 'Extension Manager' - enable Pop Shell
*********got stuck here.  Could not get Pop Shell to work.  Looks like System 76 disabled things (unsupported)
GNOME-xorg to start a X11 session
kgx&  # gnome shell
gnome-text-editor&
Alt-F2  # run

Restart GNOME Shell: If the graphical shell becomes unresponsive, you can switch to a different TTY (text-only terminal) using Ctrl + Alt + F2, log in, and run killall -1 gnome-shell or pkill -HUP gnome-shell. The shell will automatically restart.


### speed up Drive
echo "test gdrive" >testfile
rclone copy testfile 
htop

gdrive: -P  #  Watch:
Transfer speed
CPU usage (top or htop)
Network usage (iftop)

If CPU is pegged → encryption/checksums are the bottleneck.
If network is low → concurrency/settings issue.

rclone copy testfile gdrive: --transfers 8 --checkers 16 --fast-list -P

rclone copy testfile gdrive: --transfers 16 --checkers 32 --fast-list -P

rclone copy testfile gdrive: --transfers 16 --checkers 32 --fast-list --multi-thread-streams 4 --multi-thread-cutoff 10M --drive-chunk-size 64M --buffer-size 64M -P

Other possibilities
--ignore-checksum
--bwlimit off

Logging for clues (retries, rate limiting, timeouts)
rclone copy testfile gdrive: -vv --log-file=rclone.log

# best result (avoid --fast-list, bw_limit off no effect)
rclone copy Downloads/google-chrome-stable_current_amd64.deb gdrive:  --multi-thread-streams 4 --tpslimit 5 --tpslimit-burst 5 -vv --log-file=rclone.log  -P


### Install Chrome
get the 64-bit deb file
https://www.google.com/chrome/

```bash
cd Downloads
sudo dpkg -i  google-chrome-stable_current_amd64.deb
``` 


### Chrome Remote Desktop
See [INSTALL_Chrome_Remote_Desktop](INSTALL_Chrome_Remote_Desktop.md) for Rclone setup.


### noMachine Desktop Share
See [INSTALL_noMachine](INSTALL_noMachine.md) 


### RStudio-desktop
Get the Deb
```html
https://posit.co/download/rstudio-desktop/
```
```bash
sudo gdebi ~/Downloads/rstudio-*-amd64.deb
```


## SageMath from source (recommended)
https://sagemanifolds.obspm.fr/install_ubuntu.html

Dependencies:
```bash
sudo apt install automake bc binutils bzip2 ca-certificates cliquer cmake curl ecl eclib-tools fflas-ffpack flintqs g++ gengetopt gfan gfortran git glpk-utils gmp-ecm lcalc libatomic-ops-dev libboost-dev libbraiding-dev libbz2-dev libcdd-dev libcdd-tools libcliquer-dev libcurl4-openssl-dev libec-dev libecm-dev libffi-dev libflint-dev libfreetype-dev libgc-dev libgd-dev libgf2x-dev libgiac-dev libgivaro-dev libglpk-dev libgmp-dev libgsl-dev libhomfly-dev libiml-dev liblfunction-dev liblrcalc-dev liblzma-dev libm4rie-dev libmpc-dev libmpfi-dev libmpfr-dev libncurses-dev libntl-dev libopenblas-dev libpari-dev libpcre3-dev libplanarity-dev libppl-dev libprimesieve-dev libpython3-dev libqhull-dev libreadline-dev librw-dev libsingular4-dev libsqlite3-dev libssl-dev libsuitesparse-dev libsymmetrica2-dev zlib1g-dev libzmq3-dev libzn-poly-dev m4 make nauty openssl palp pari-doc pari-elldata pari-galdata pari-galpol pari-gp2c pari-seadata patch perl pkg-config planarity ppl-dev python3-setuptools python3-venv r-base-dev r-cran-lattice singular sqlite3 sympow tachyon tar texinfo tox xcas xz-utils 

sudo apt install texlive-latex-extra texlive-xetex latexmk pandoc dvipng 

mkdir ~/SageMath
cd SageMath
git clone --branch master https://github.com/sagemath/sage.git  # this takes a long time
cd sage
make configure
./configure
```
Determine the number of cores
```bash
nproc --all
```

Put 2x result after J in following:
```bash
MAKE="make -j32" make  # 32 is number of threads which may be 2x number of cores
```

This will take a while - get coffee.

Sym link:
```bash
sudo ln -sf $(pwd)/sage /usr/local/bin
```

Run in any directory:
```
sage -n
```

Use Jupyter
```
sage -n jupyterlab
```


## End works in progress
