# Python Projects & Development Setup

## PyCharm

- Setup `.venv` for Python; update pip before importing packages
- Use local dictionary: Settings → Editor → Natural Languages → Spelling (uncheck "use single...")
- **Caution:** Use PyCharm to install Python interpreters — deb install broke Ubuntu
- May need to start PyCharm twice on first launch

## movie_Scraper

- Use its own `.venv`
- Use `PySimpleGUI-4-foss` instead of `PySimpleGUI`
- Set DB location to `/home/daveg/Documents/GitHub/myComputer`
- Run `install.py` and follow instructions; find it in applications and save to favorites
- If encountering `_tkinter.TclError: can't use "pyimage7" as iconphoto`, it can be safely ignored.

## myPyScreencast

- Use its own `.venv`
- May need to uninstall and reinstall `pillow` to eliminate interpreter confusion

## SOC_Particle (VS Code / Particle Workbench)

```bash
sudo apt-get install libarchive-zip-perl   # fix 'crc32 not found'
```

- VS Code extensions: Codeium AI (login via Google), Ruff, Python, Particle Workbench
- Open folder: `Documents/GitHub/myStateOfCharge/SOC_Particle`

## fwgWhisper

- Versions ≥3.8, <3.12 supported; use Python 3.11.9 (see [INSTALL_Alternate_Python](INSTALL_Alternate_Python.md))
