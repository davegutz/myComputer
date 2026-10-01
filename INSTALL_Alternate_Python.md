# Alternate Python Version (Compile from Source)

> **Never replace the default Python in Debian-based Linux.**

## 1. Install Build Dependencies

```bash
sudo apt update
sudo apt install -y wget build-essential libreadline-dev libncursesw5-dev \
  libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev \
  libffi-dev zlib1g-dev portaudio19-dev
```

## 2. Download and Compile Python 3.11.9

```bash
# From https://www.python.org/ftp/python/
cd Downloads/
tar -Jxf Python-3.11.9.tar.xz
cd Python-3.11.9/
./configure --enable-optimizations --enable-shared
sudo make -j4 && sudo make altinstall
sudo ldconfig /usr/local/lib
```

## 3. Verify

```bash
python3.11 --version
python3.11 -m pip --version
```

## 4. Usage in PyCharm

Use `.venv` in PyCharm pointing to `/usr/local/bin/python3.11` to set up projects with this Python version.

## 5. Uninstall (if needed)

```bash
cd Downloads/Python-3.11.9/
sudo make uninstall
```
