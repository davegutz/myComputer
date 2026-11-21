# Google Chrome Installation & Configuration

## 1. Installation

### Arch / CachyOS

Install official Google Chrome from the AUR:

```bash
paru -S google-chrome
# or
yay -S google-chrome
```

### Ubuntu / Debian / Lubuntu

```bash
sudo apt update
sudo apt install -y libu2f-udev wget
cd ~/Downloads
rm -f google-chrome-stable*.deb
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt install -f -y
```

**Uninstall Chrome (Ubuntu / Debian / Lubuntu):**

```bash
sudo apt purge -y google-chrome-stable
sudo apt autoremove -y
sudo apt autoclean && sudo apt clean
```

---

## 2. Recommended Browser Tweaks

Navigate to the following internal Chrome URLs to configure:

### Hardware Acceleration
- Open `chrome://settings/system`
- Toggle **Use graphics acceleration when available** to **ON**
- Click **Relaunch**

### Pi-hole & Local DNS Resolver Compatibility
- Open `chrome://settings/security`
- Scroll to Advanced settings
- Toggle **Use secure DNS** to **OFF** (prevents Chrome from using third-party DNS over HTTPS and bypassing local Pi-hole / local network DNS servers)
