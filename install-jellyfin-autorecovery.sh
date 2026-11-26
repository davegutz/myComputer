#!/usr/bin/env bash
set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run with sudo: sudo bash $0"
  exit 1
fi

echo "Installing Jellyfin auto-recovery service and udev rules..."

# 1. Create the recovery helper script
cat << 'EOF' > /usr/local/bin/recover-jellyfin-lib.sh
#!/usr/bin/env bash

# If the library directory is healthy and readable, nothing to do
if ls -d "/media/daveg/Lib/Movies" >/dev/null 2>&1; then
    exit 0
fi

# Wait briefly for udev to finish registering the device and UUID symlinks
sleep 1

# Lazy unmount the dead mount point and any accidental Lib1 mount
/bin/umount -l /media/daveg/Lib 2>/dev/null || true
/bin/umount /media/daveg/Lib1 2>/dev/null || true

# Mount the drive cleanly according to /etc/fstab
if /bin/mount /media/daveg/Lib; then
    /bin/systemctl restart jellyfin
    logger -t recover-jellyfin-lib "Successfully remounted /media/daveg/Lib and restarted Jellyfin"
else
    logger -t recover-jellyfin-lib "Failed to remount /media/daveg/Lib"
fi
EOF

chmod +x /usr/local/bin/recover-jellyfin-lib.sh

# 2. Create the systemd one-shot service
cat << 'EOF' > /etc/systemd/system/remount-jellyfin-lib.service
[Unit]
Description=Recover and remount Jellyfin Library drive on USB reconnect
After=local-fs.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/recover-jellyfin-lib.sh

[Install]
WantedBy=multi-user.target
EOF

# 3. Create the udev rules
cat << 'EOF' > /etc/udev/rules.d/99-jellyfin-lib.rules
# Prevent desktop automounter (udisks2) from creating /media/daveg/Lib1
SUBSYSTEM=="block", ENV{ID_FS_UUID}=="e8fdea26-3474-417c-a1cf-73b7c2725a92", ENV{UDISKS_IGNORE}="1"

# When the partition is detected, trigger the auto-recovery service
ACTION=="add", SUBSYSTEM=="block", ENV{ID_FS_UUID}=="e8fdea26-3474-417c-a1cf-73b7c2725a92", TAG+="systemd", ENV{SYSTEMD_WANTS}="remount-jellyfin-lib.service"
EOF

# 4. Reload systemd and udev
systemctl daemon-reload
udevadm control --reload-rules
udevadm trigger

echo "Setup complete! The auto-recovery service is active."
