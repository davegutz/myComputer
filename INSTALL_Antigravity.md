# Antigravity (gemini-cli) Installation & Setup

## 1. CLI Installation

```bash
sudo apt update
sudo apt purge -y nodejs npm
sudo apt autoremove -y
sudo apt install curl nodejs npm -y
sudo npm install -g @google/gemini-cli
node -v

# Install Antigravity CLI
# https://antigravity.google/
curl -fsSL https://antigravity.google/cli/install.sh | bash

# Add to PATH in ~/.bashrc:
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc

# Verify installation:
agy --version
agy --cli
```

## 2. VS Code Integration

Install launcher extension:
- In VS Code → Extensions → Search for **Antigravity CLI Launcher** → Install
- Close and restart the Antigravity terminal inside VS Code.

## 3. PyCharm Integration

- In PyCharm → Settings → Plugins → Marketplace → Search for **Antigravity Companion** → Install
- A lightning bolt icon appears in the top right → Launch → Yes → Wait to log in via browser URL (scroll down below hyperlink to find code entry area if needed).
- JetBrains AI (Swirl icon): Settings → AI Assistant → Agents → Google Antigravity.

## 4. Configuration (YOLO Mode)

Edit or create `/home/daveg/.gemini/antigravity-cli/settings.json`:

```json
{
  "allowNonWorkspaceAccess": true,
  "auto_accept": true,
  "colorScheme": "dark",
  "enableTelemetry": false,
  "enableTerminalSandbox": false,
  "permissions": {
    "allow": [
      "command(*)",
      "write_file(*)",
      "read_file(*)",
      "mcp(*)",
      "unsandboxed(*)"
    ],
    "deny": [
      "command(sudo)"
    ]
  },
  "trustedWorkspaces": [
    "/home/daveg/Documents/GitHub/mySOC/SOC_Particle/pyStateOfCharge",
    "/home/daveg/Documents/GitHub/mySOC/SOC_Particle"
  ]
}
```
