# Jellyfin Media Server Installation & Setup (Lubuntu)

> **Note:** Better to have NO media server on a 4 GB Lenovo laptop.

---

## 1. Jellyfin Media Player (Client - Optional)

```bash
sudo apt install -y flatpak gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
# reboot
flatpak install flathub com.github.iwalton3.jellyfin-media-player
flatpak run com.github.iwalton3.jellyfin-media-player
ifconfig  # copy ip string for inet from wlp2s0  e.g. 192.168.5.205  (http://192.168.5.205:8096/web/#/home.html)
# answer jellyfin_..._pkg by cut and paste from previous

# Remove:
flatpak remove com.github.iwalton3.jellyfin-media-player
```

---

## 2. Install Jellyfin Server

```bash
curl -s https://repo.jellyfin.org/install-debuntu.sh | sudo bash
sudo usermod -a -G daveg jellyfin
# Visit http://localhost:8096
sudo chown -R jellyfin /media/daveg
```

### Initial Access & Configuration
1. Open Firefox and browse to: `http://localhost:8096` (or from bookmarks).
2. Default initial user setup: `jellyfin`

---

## 3. Persistent USB Drive Auto-Recovery

If the external media drive momentarily disconnects or glitches on USB, Linux can create a ghost mount that breaks Jellyfin until manually unmounted. You can teach Linux to cleanly self-heal whenever this drive reconnects by pairing a udev rule with a systemd service.

```bash
sudo /home/daveg/Documents/GitHub/myComputer/install-jellyfin-autorecovery.sh
```

### How Auto-Recovery Works

Whenever the WD Elements drive (UUID `e8fdea26-3474-417c-a1cf-73b7c2725a92`) is plugged in or reconnected:

1. **`udisks2` ignores it** (prevents `/media/daveg/Lib1` naming conflicts).
2. **Lazily detaches** (`umount -l`) the dead ghost mount point.
3. **Mounts the drive cleanly** back to `/media/daveg/Lib` according to `/etc/fstab`.
4. **Restarts Jellyfin** so its file descriptors and directory watches immediately latch onto the restored drive.
