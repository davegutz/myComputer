# Google Drive Setup with Rclone

## 1. Install Rclone

```bash
sudo apt install rclone
rclone config
```

Follow the prompts:
1. Enter `n` to create a new remote.
2. Provide a name for your remote (e.g., `gdrive`).
3. Select `drive` from the list of storage types for Google Drive. (usually 18)
4. Accept the default `client_id` and `client_secret` by leaving them blank and pressing Enter (or supply your custom Google OAuth credentials).
5. Choose scope `1` (Full access).
6. Leave `root_folder_id` and `service_account_file` blank unless needed.
7. Edit Advanced config: `y`
   - `oauth Access Token`: leave blank or enter app password
   - `upload_cutoff`: `1G`
   - Leave other options as default
8. When asked about `Use auto config?`, type `y` and authenticate in your web browser.
9. Team Drive: `n`
10. Confirm and save (`y`), then quit the configuration wizard (`q`).

## 2. Mount Google Drive

```bash
mkdir ~/gdrive
rclone mount gdrive: ~/gdrive &
```

## 3. Auto-start Rclone on Login

Add a startup application entry for `"gdrive"` with command:
```bash
rclone mount gdrive: ~/gdrive &
```

**Or create a script and desktop autostart:**

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
  --daemon \
  &
EOF
chmod +x ~/bin/Rclone

mkdir -p ~/.config/autostart
cat << EOF > ~/.config/autostart/rclone.desktop
[Desktop Entry]
Name=rclone
Exec=/home/daveg/bin/Rclone
Terminal=false
Type=Application
X-Desktop-File-Install-Version=0.27
EOF
chmod +x ~/.config/autostart/rclone.desktop
```

**Test the autostart entry:**

```bash
gio launch ~/.config/autostart/rclone.desktop
# or
sudo apt install dex
dex ~/.config/autostart/rclone.desktop
```

## 4. Optimized Copy and Sync Commands

For large backups, transfers, and file synchronization, see [INSTALL_Google_Drive_Backup](INSTALL_Google_Drive_Backup.md).
