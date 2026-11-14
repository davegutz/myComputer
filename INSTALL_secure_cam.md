# Security camera

############################################################################################
 
                     Look |  Look
                          v
 This whole procedure has been superceded by install_secure_cam in the repository myLinux

############################################################################################



## 0. Plug in the camera and make sure it is detected:
```bash
ls -l /dev/video*
```

## 1. Install motion

```bash
sudo apt update && sudo apt install motion
sudo apt install pipx  # To install motioneye
pipx install motioneye
sudo apt update
sudo apt --no-install-recommends install -y ca-certificates curl python3-venv motion ffmpeg v4l-utils
sudo python3 -m venv --upgrade-deps /opt/motioneye
sudo /opt/motioneye/bin/pip install motioneye
# motionEye wraps around motion and provides an interactive web dashboard 
curl -fsSL https://tailscale.com/install.sh | sh  # the web dashboard

mkdir /home/daveg/camera_captures

# Generate mask
python3 -c "from PIL import Image, ImageDraw; img = Image.new('L', (1280, 720),
0); draw = ImageDraw.Draw(img); draw.rectangle([427, 0, 1280, 720], fill=255);
img.save('/home/daveg/.local/mask.pgm')"

cat << EOF > /home/daveg/.local/secure_cam.conf
# Input device
video_device /dev/video0
width 1280
height 720
framerate 2

# Motion detection & capture rate
threshold 1500
minimum_motion_frames 1
event_gap 3

# Picture capture (saves frames at 2 fps while motion is active)
picture_output on
picture_filename %Y%m%d_%H%M%S-%q

# Movie capture
movie_output on
movie_codec mp4
movie_filename %Y%m%d_%H%M%S

# Destination directory
target_dir /home/daveg/camera_captures

# Mask to stop spurious trips
mask_file /home/daveg/.local/mask.pgm
EOF

# symlink meyectl so the system and service can find it
sudo ln -sf /opt/motioneye/bin/meyectl /usr/local/bin/meyectl

# initialize
sudo /opt/motioneye/bin/motioneye_init
```

## 2. Start it
```bash
motion -c ~/.local/secure_cam.conf 
```

## 3. Stop it
```bash
sudo systemctl stop motion
sudo systemctl disable motion
```

## 4. Review photos - Fast Desktop Thumbnail & Flipbook Viewer (feh)
#  feh is extremely fast, lightweight, and purpose-built for browsing directories with
#  thousands of photos.

```bash
# Install feh:
    sudo apt install feh

# Open as a visual thumbnail grid:
    feh -t -E 180 -y 120 -W 1200 ~/camera_captures/

      # Displays an interactive sheet of thumbnails. Clicking any thumbnail opens the
      full photo.

#Play back captures like a flipbook/slideshow:
    feh -d -F -D 0.5 --auto-zoom ~/camera_captures/

      # Plays captures at 2 frames per second (-D 0.5).
      #Use Left/Right arrow keys to step frame-by-frame, or Spacebar to advance quickly.
      
# Generate a Quick Daily Timelapse Video (ffmpeg)
    ffmpeg -framerate 10 -pattern_type glob -i '/home/daveg/camera_captures/*.jpg' -c:v libx264 -pix_fmt yuv420p ~/camera_captures/review_today.mp4

  # Plays through the motion events at 5× speed (10 fps).
  # You can open review_today.mp4 in any video player and scrub backward/forward through the timeline in seconds.

```

# 5. Dedicated Web NVR: motionEye

  # If you want a full security DVR interface in your browser (with a calendar
  # timeline, event playback, and camera controls):

```bash
sudo tailscale up

```

# 3. Allow port 8765 through the firewall (if UFW is enabled)
#  If you have Ubuntu's firewall (ufw) active and you are accessing http://venus-littleguy:8765 from a
#  different laptop or phone on your network, open port 8765:
```bash
sudo ufw allow 8765/tcp
```
# Once the service is active, reload http://venus-littleguy:8765 in your browser.


# Check that the service is active and listening on port 8765:
```bash
systemctl status motioneye
ss -tulpn | grep 8765
```

# View
```html
http://venus-littleguy:8765
# user admin <pwdFromBitwarden>
# first time enter admin user with blank password then create new password
```

# To record and review only detected motion events, follow these steps in your motionEye web interface:
```text
  ──────
  ### Step 1: Configure Motion-Only Recording

  1. Open the left sidebar by clicking the wrench/gear icon (Settings) in the top-left corner.
  2. Ensure your camera is selected in the dropdown at the top.
  3. Configure the following sections:

  #### A. Motion Detection


email:
davegutz2006@gmail.com
password enter 16-character app password for 'motionEye' at https://myaccount.google.com/apppasswords  otmw xfce rmhb jpjs
smtp.gmail.com
Use TLS ON

  • Switch Motion Detection to ON.
  • (Optional) Turn on Show Frame Changes temporarily—this draws a box around moving objects in the live
  preview so you can see what motion triggers it.

  #### B. Movies (Video Clips)
  • Switch Movies to ON.
  • Set Recording Mode to Motion Triggered (do not choose "Continuous").
  • Set Movie Format to H.264 (.mp4) for best compatibility with phones and browsers.
  • (Recommended) Set Maximum Movie Length (e.g., 300 seconds / 5 mins) and Preserve Movies (e.g., 7 Days
  or 30 Days to automatically manage disk space).
  #### C. Still Images (Snapshots)
  • If you want a photo captured every time motion happens:
      • Switch Still Images to ON and set Capture Mode to Motion Triggered.
  • If you only want video clips, switch Still Images to OFF.

  4. Click the yellow Apply button at the top to save changes.
  ──────
  ### Step 2: How to View the Recorded Events

  Once motion is triggered and recorded:

  1. Hover your mouse over the camera feed (or tap it on mobile).
  2. Look at the icons in the top-right corner of the video frame:
      • Click the Pictures / Filmstrip icon (or the folder icon).
  3. A timeline/media browser drawer will open displaying:
      • All recorded clips and snapshots grouped by Date and Time.
      • You can click any event to play the video directly in your browser, download it, or delete it.

  ──────
  ### Helpful Tuning Tips

 Load the file motioneye-config.tar.gz using the General Settings - Restore

Client secret:
bc4c969c2b461cb4768b8cb8c7ba693da8e572be33c30f169c99d2af93180007
Not sure what this is used for
```

# on phone
To allow another person on an Android phone to view the live camera and event recordings, follow these
  steps:
  
  install tailscale
  sign in as davegutz2006@gmail.com with that password
  add their address to the monitor app Setup (comma-separated addresses in notification)
  ──────
  ### Step 1: Give Them a "Viewer-Only" Account (Recommended)

  In motionEye, you can give them a viewer account so they can watch live video and browse recordings
  without having access to change settings or break configurations:
  1. Open motionEye on your PC and click the Wrench/Gear icon (Settings).
  2. Under General Settings:
      • Note the Surveillance Username (default is user).
      • Set a Surveillance Password for them.
  3. Click Apply.
  4. Give them the username user and the password you just set.
  ──────
  ### Step 2: Connect Their Phone to the Machine
  Depending on where they are:

  #### Option A: At Home (Same Wi-Fi Network) — Simplest
  1. Connect their Android phone to your home Wi-Fi.
  2. Open Chrome on their phone and go to:
    http://192.168.5.205:8765


  #### Option B: Away from Home (Cellular Data or Outside Wi-Fi)
  1. Install Tailscale on their Android phone from the Google Play Store.
  2. Log in (either using your Tailscale account or by sharing the venus-littleguy machine to their
  Tailscale user via the Tailscale admin console).
  3. Connect Tailscale on their phone.
  4. Open Chrome on their phone and go to:
    http://100.122.174.21:8765
  (or http://venus-littleguy:8765)
  ──────
  ### Step 3: How They View the Videos on Android

  1. When the page opens, log in with username user and their password.
  2. Open Media Viewer:
      • Tap anywhere on the live video stream to display the overlay controls.
      • Tap the filmstrip / movie icon in the top-right corner of the video frame.
  3. Play & Download:
      • The media browser opens showing clips grouped by date.
      • Tap any event thumbnail to stream the .mp4 video directly in the mobile browser.
      • Tap the download arrow on any clip to save it to their phone's camera roll/downloads.


  │ Tip
  │ Make it look like a native App: In Chrome on Android, tap the three-dot menu (⋮) in the top-right and
  │ choose "Add to Home screen" (or "Install app"). This places a motionEye shortcut icon right on their
  │ Android home screen for one-tap access.


