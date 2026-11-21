# Claude Code Installation & Setup

Anthropic's official agentic command-line interface.

## 1. Installation

Run the official installation script:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Ensure `~/.local/bin` is in your `PATH`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

Verify the installation:

```bash
claude --version
```

## 2. Authentication & Login

Launch Claude Code to log in via your Anthropic account:

```bash
claude
```

Follow the browser prompt to complete OAuth authentication.
