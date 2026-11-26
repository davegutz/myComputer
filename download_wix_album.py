#!/usr/bin/env python3
r"""
Universal Wix Music Album / Playlist Downloader
Cross-platform: Windows, macOS, and Linux.

Usage:
    python3 download_wix_album.py <URL>

Examples:
    python3 download_wix_album.py "https://www.speakingmusic.com/about-3"
    python3 download_wix_album.py "https://www.speakingmusic.com/about-1"
    python3 download_wix_album.py "https://www.speakingmusic.com/day-night-download"
"""

import os
import sys
import re
import json
import ssl
import zipfile
import pathlib
import urllib.request
import urllib.error
from urllib.parse import urlparse

# Ensure UTF-8 output on Windows Command Prompt / PowerShell
if sys.platform.startswith("win"):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CDN_AUDIO_BASE = "https://music.wixstatic.com/preview/"

def get_ssl_context():
    """Create an SSL context, falling back if system certificates are missing (common on macOS)."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass
    try:
        return ssl.create_default_context()
    except Exception:
        return ssl._create_unverified_context()

def safe_urlopen(req, timeout=30):
    """Open a URL with automatic fallback for macOS certificate issues."""
    ctx = get_ssl_context()
    try:
        return urllib.request.urlopen(req, context=ctx, timeout=timeout)
    except urllib.error.URLError as e:
        err_str = str(e).lower()
        if "certificate" in err_str or "ssl" in err_str:
            unverified_ctx = ssl._create_unverified_context()
            return urllib.request.urlopen(req, context=unverified_ctx, timeout=timeout)
        raise

def clean_filename(name):
    """
    Sanitize string for cross-platform filesystem compatibility (Windows, macOS, Linux).
    Enforces Windows reserved name checks and removes forbidden characters.
    """
    # Remove forbidden characters across Windows/POSIX: \ / * ? : " < > |
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    
    # Windows forbids trailing dots and trailing spaces
    cleaned = cleaned.rstrip(". ")

    # Windows reserved filenames check (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
    reserved = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    base = cleaned.split(".")[0].upper()
    if base in reserved:
        cleaned = f"_{cleaned}"

    return cleaned or "Untitled"

def get_default_music_dir():
    """Returns a valid Music directory across Windows, macOS, and Linux."""
    home = pathlib.Path.home()
    music_dir = home / "Music"
    try:
        music_dir.mkdir(parents=True, exist_ok=True)
        return music_dir
    except Exception:
        # Fallback to current working directory if home/Music is unwritable
        return pathlib.Path.cwd()

def fetch_page_html(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    with safe_urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="ignore"), url

def extract_album_details(html, page_url):
    path_slug = urlparse(page_url).path.strip("/")
    
    # 1. Find the pageJsonFileName from the site's routing map
    page_json_file = None
    if path_slug:
        m_page = re.search(r'\{[^{}]*\"pageUriSEO\":\s*\"' + re.escape(path_slug) + r'\"[^{}]*\}', html)
        if m_page:
            try:
                page_json_file = json.loads(m_page.group(0)).get("pageJsonFileName")
            except Exception:
                pass

    if not page_json_file:
        m_curr = re.search(r'\"pageJsonFileName\":\s*\"([^\"]+)\"', html)
        if m_curr:
            page_json_file = m_curr.group(1)

    if not page_json_file:
        raise ValueError(f"Could not find Wix page structure for '{path_slug}'.")

    # 2. Locate the Wix Thunderbolt features bundle URL for this page
    feat_match = re.search(
        r'(https?://siteassets\.parastorage\.com/pages/pages/thunderbolt\?[^"\'\s<>]*pageId=' +
        re.escape(page_json_file) + r'\.json[^"\'\s<>]*)',
        html
    )
    if not feat_match:
        raise ValueError(f"Could not locate page features configuration for {page_json_file}.")
    
    feat_url = feat_match.group(1)

    # 3. Extract site metaSiteId from the bundle URL
    m_meta = re.search(r'[?&]metaSiteId=([0-9a-f\-]+)', feat_url)
    meta_site_id = m_meta.group(1) if m_meta else None

    # 4. Fetch the page features JSON to obtain the albumId
    req_feat = urllib.request.Request(feat_url, headers={"User-Agent": "Mozilla/5.0"})
    with safe_urlopen(req_feat) as resp:
        feat_raw = resp.read().decode("utf-8", errors="ignore")

    m_alb = re.search(r'\"wmp::albumId\":\s*(?:\{\s*\"value\":\s*\"([0-9a-f\-]+)\"|\"([0-9a-f\-]+)\")', feat_raw)
    if not m_alb:
        m_alb = re.search(r'\"albumId\":\s*(?:\{\s*\"value\":\s*\"([0-9a-f\-]+)\"|\"([0-9a-f\-]+)\")', feat_raw)

    album_id = (m_alb.group(1) or m_alb.group(2)) if m_alb else None
    if not album_id:
        raise ValueError("No Wix Music album widget found on this page.")

    # 5. Fetch collection JSON
    candidate_urls = []
    if meta_site_id:
        candidate_urls.append(f"https://collections.wixstatic.com/collections/{meta_site_id}_{album_id}.json")
    candidate_urls.append(f"https://collections.wixstatic.com/collections/376c3b9b-d144-4f5a-af4a-1b8f4666418b_{album_id}.json")
    candidate_urls.append(f"https://collections.wixstatic.com/collections/{album_id}.json")

    col_data = None
    for cu in candidate_urls:
        try:
            req_c = urllib.request.Request(cu, headers={"User-Agent": "Mozilla/5.0"})
            with safe_urlopen(req_c) as r:
                col_data = json.loads(r.read().decode("utf-8"))
                break
        except Exception:
            continue

    if not col_data or "collection" not in col_data:
        raise ValueError(f"Could not retrieve album collection metadata (Album ID: {album_id}).")

    return col_data["collection"]

def download_album(collection, output_base_dir):
    props = collection.get("public_properties", {})
    raw_album_name = props.get("albumName", collection.get("title", "Album")).strip()
    artist_name = props.get("artistName", "Unknown Artist").strip()
    items = collection.get("items", [])

    safe_album_name = clean_filename(raw_album_name)
    folder_name = safe_album_name.replace(" ", "_")
    target_dir = pathlib.Path(output_base_dir) / folder_name
    zip_path = pathlib.Path(output_base_dir) / f"{folder_name}.zip"

    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f" Album:  {raw_album_name}")
    print(f" Artist: {artist_name}")
    print(f" Tracks: {len(items)}")
    print(f" Output: {target_dir}")
    print(f" Zip:    {zip_path}")
    print(f"=======================================================\n")

    downloaded_files = []

    for idx, item in enumerate(items, 1):
        item_props = item.get("public_properties", {})
        title = item_props.get("trackName", item.get("title", f"Track_{idx}")).strip()
        duration = item_props.get("trackDuration", "??:??")
        track_slug = item_props.get("trackURL")

        if not track_slug:
            print(f"[{idx:02d}/{len(items)}] Skipping '{title}' (no track audio slug)")
            continue

        clean_track_title = clean_filename(title)
        filename = f"{idx:02d} - {clean_track_title}.mp3"
        filepath = target_dir / filename
        download_url = CDN_AUDIO_BASE + track_slug

        print(f"[{idx:02d}/{len(items)}] Downloading: {filename} ({duration})...")

        try:
            req_audio = urllib.request.Request(
                download_url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with safe_urlopen(req_audio) as r_in, open(filepath, "wb") as f_out:
                f_out.write(r_in.read())
            # Use forward slashes inside ZIP archive for cross-platform compatibility
            archive_entry_name = f"{folder_name}/{filename}"
            downloaded_files.append((filepath, archive_entry_name))
        except Exception as e:
            print(f"   [ERROR] Failed to download {filename}: {e}")

    # Build ZIP archive
    if downloaded_files:
        print(f"\nPackaging {len(downloaded_files)} tracks into zip archive: {zip_path}...")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for full_path, arc_name in downloaded_files:
                zipf.write(full_path, arc_name)

        print("\nAll tasks completed successfully!")
        print(f"  - Folder:  {target_dir}")
        print(f"  - Archive: {zip_path}")
    else:
        print("\nNo tracks were downloaded.")

def main():
    interactive_launch = len(sys.argv) < 2
    if interactive_launch:
        print("Universal Wix Music Album Downloader")
        print("Usage: python3 download_wix_album.py <URL>\n")
        url_input = input("Enter Wix page URL: ").strip()
        if not url_input:
            sys.exit(1)
    else:
        url_input = sys.argv[1].strip()

    music_dir = get_default_music_dir()

    print(f"Fetching page: {url_input}...")
    try:
        html, resolved_url = fetch_page_html(url_input)
        collection = extract_album_details(html, resolved_url)
        download_album(collection, music_dir)
    except KeyboardInterrupt:
        print("\n\nDownload canceled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[Error] {e}")
        sys.exit(1)
    finally:
        # If user double-clicked the script on Windows/macOS without a terminal open,
        # pause before closing so they can read the results.
        if interactive_launch and sys.stdin.isatty():
            try:
                input("\nPress Enter to exit...")
            except (EOFError, KeyboardInterrupt):
                pass

if __name__ == "__main__":
    main()
