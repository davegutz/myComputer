# Run an Optimized Copy/Backup Command to Google Drive

To handle large data efficiently, use the rclone `copy` command paired with performance flags:

```bash
rclone copy /path/to/local/folder gdrive:BackupFolder \
  --drive-chunk-size 512M \
  --max-age 2026-09-01 \  # or --max-age 7d (files modified within the last 7 days) or --max-age 3M (files modified within the last 3 months)
  --transfers 4 \
  --checkers 8 \
  --retries 3 \
  --stats 1s \
  --verbose
```

### Preview rclone command
```bash
rclone lsf /path/to/local  --max-age 2026-09-01
```

### Sync
```bash
rclone sync /media/daveg/Lib/Movies/ gdrive:Movies \
  --max-age 2026-09-08 \
  --min-age 2026-09-17 \
  --tpslimit 8 \
  --transfers 2 \
  --checkers 4 \
  --drive-chunk-size 512M \
  -vv --log-file rclone-error.log \
  --dry-run
  
rclone sync /media/daveg/Lib/Movies/ gdrive:Movies \
  --max-age 2026-09-08 \
  --min-age 2026-09-30 \
  --tpslimit 8 \
  --transfers 2 \
  --checkers 4 \
  --drive-chunk-size 512M \
  --stats 5s \
  --verbose \
  -vv --log-file rclone-error.log

rclone sync /media/daveg/Lib/Movies/ gdrive:Movies \
  --tpslimit 8 \
  --transfers 2 \
  --checkers 4 \
  --drive-chunk-size 512M \
  --stats 5s \
  -vv --log-file rclone-error.log

rclone sync /path/to/local remote:path -vv --log-file rclone-error.log
```

### Key Flags Explained
- `--drive-chunk-size 512M`: Uploads large files in 512MB chunks, which maximizes throughput and reduces failure rates on massive files.
- `--transfers 4`: Number of files to copy in parallel. Set to 1 if you are uploading a single massive file.
- `--retries 3`: Automatically restarts the transfer if network errors occur.
- `--verbose`: Prints active transfer statistics so you can monitor progress in real time.
