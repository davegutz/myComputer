#!/usr/bin/env python3
"""
Video Downloader for Linux
Downloads videos (Vimeo, YouTube, etc.) to ~/Music using yt-dlp and ffmpeg.

Usage:
    python3 download_video.py <URL> [URL2 ...]
    python3 download_video.py urls.txt

Example:
    python3 download_video.py "https://vimeo.com/1247854664/bce305e34c?fl=pl&fe=ti"
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

MUSIC_DIR = Path.home() / "Music"

def check_dependencies():
    """Verify that yt-dlp and ffmpeg are installed."""
    missing = []
    if not shutil.which("yt-dlp"):
        missing.append("yt-dlp")
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg")

    if missing:
        print(f"[Error] Required tools missing: {', '.join(missing)}")
        print("Install them on Ubuntu / Lubuntu with:")
        print(f"  sudo apt install -y {' '.join(missing)}")
        sys.exit(1)

def collect_urls(args):
    """Parse command line arguments or prompt user for URLs."""
    urls = []
    for arg in args:
        arg_path = Path(arg)
        if arg_path.is_file():
            # Read URLs from a text file (one per line)
            with open(arg_path, "r", encoding="utf-8") as f:
                for line in f:
                    cleaned = line.strip()
                    if cleaned and not cleaned.startswith("#"):
                        urls.append(cleaned)
        elif arg.startswith("http://") or arg.startswith("https://"):
            urls.append(arg)

    if not urls:
        print("Video Downloader")
        print("Usage: python3 download_video.py <URL1> [URL2 ...]\n")
        user_input = input("Enter video URL: ").strip()
        if user_input:
            urls.append(user_input)

    return urls

def download_video(url, output_dir):
    """Download a video using yt-dlp with best quality merged into MP4."""
    output_template = str(output_dir / "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--format", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "--output", output_template,
        "--no-mtime",
        "--console-title",
        url
    ]

    print(f"\n=======================================================")
    print(f" Fetching: {url}")
    print(f" Target:   {output_dir}")
    print(f"=======================================================\n")

    result = subprocess.run(cmd)
    return result.returncode == 0

def main():
    check_dependencies()
    MUSIC_DIR.mkdir(parents=True, exist_ok=True)

    urls = collect_urls(sys.argv[1:])
    if not urls:
        print("[!] No URLs provided. Exiting.")
        sys.exit(0)

    print(f"Found {len(urls)} video(s) to download into: {MUSIC_DIR}")

    successful = 0
    failed = []

    for idx, url in enumerate(urls, 1):
        print(f"\n[{idx}/{len(urls)}] Processing: {url}")
        if download_video(url, MUSIC_DIR):
            successful += 1
        else:
            failed.append(url)

    print("\n-------------------------------------------------------")
    print(f"Downloads Complete: {successful}/{len(urls)} successful")
    if failed:
        print(f"Failed ({len(failed)}):")
        for f in failed:
            print(f"  • {f}")
    print(f"Files saved in: {MUSIC_DIR}")
    print("-------------------------------------------------------")

if __name__ == "__main__":
    main()
