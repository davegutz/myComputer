# Zoxide (Smarter `cd` Command) Setup

[Zoxide](https://github.com/ajeetdsouza/zoxide) remembers which directories you use most frequently, so you can "jump" to them in just a few keystrokes (e.g. `z Documents`).

## 1. Installation

### Arch / CachyOS
```bash
sudo pacman -S zoxide
```

### Ubuntu / Debian / Lubuntu
```bash
sudo apt update
sudo apt install -y zoxide
```

---

## 2. Shell Configuration

Initialize zoxide for your interactive Bash shell:

```bash
echo 'eval "$(zoxide init bash)"' >> ~/.bashrc
source ~/.bashrc
```

*(Note: If using `myLinux` dotfiles, zoxide initialization is automatically handled via `.bashrc`.)*

---

## 3. Training & Initial Seeding

Zoxide learns your habits automatically as you use `z` or `cd`. You can prime it immediately with common directories:

```bash
zoxide add ~/Documents
zoxide add ~/Downloads
zoxide add ~/Documents/GitHub
```

### Usage Examples:
- `z GitHub` → Jumps to `~/Documents/GitHub`
- `zi` → Interactive fuzzy selection (powered by `fzf`)
