# Troubleshooting Claude Desktop MCP Server

If you have added your MCP server configuration to `claude_desktop_config.json` but Claude Desktop is not detecting it, the issue is almost always related to **environment variable paths**. 

GUI applications on macOS (like Claude Desktop) do not inherit the `$PATH` variable from your terminal (`.zshrc` or `.bash_profile`). Because of this, when you specify `"command": "uv"`, Claude Desktop expects `uv` to be in system default binaries (like `/usr/bin`), and fails when it isn't.

Here is the step-by-step solution to fix this issue.

## Step 1: Update the config with the absolute path to `uv`

Instead of just `uv`, we must give Claude Desktop the full absolute path to where `uv` is installed on your machine. 

In your case, `uv` is installed at: `/Users/sarveshkishortalele/.local/bin/uv`.

Open your `claude_desktop_config.json` file and change `"command": "uv"` to `"command": "/Users/sarveshkishortalele/.local/bin/uv"`.

**Corrected Configuration:**
```json
{
  "preferences": {
    "quickEntryDictationShortcut": {
      "accelerator": "Alt+C"
    },
    "coworkScheduledTasksEnabled": true,
    "ccdScheduledTasksEnabled": true,
    "sidebarMode": "code",
    "coworkWebSearchEnabled": true
  },
  "mcpServers": {
    "personal-finance": {
      "command": "/Users/sarveshkishortalele/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/Users/sarveshkishortalele/Downloads/Practice/mcp/personal-finance-mcp",
        "personal-finance-mcp"
      ]
    }
  }
}
```

## Step 2: Fully Restart Claude Desktop

Claude Desktop caches its configurations on boot. Merely clicking the "X" (closing the window) does not fully quit the application.

1. Click on the **Claude** item in your macOS top menu bar and select **Quit Claude** (Alternatively, use the keyboard shortcut `Cmd + Q`).
2. Re-open Claude Desktop.
3. Check the "Plug" icon (MCP Settings) to verify `personal-finance` is now connected and glowing green.

## Step 3: Checking the Logs (If it still fails)

If the server still doesn't appear or connect, it means the python code is erroring when it starts up. You can view exactly what went wrong by checking Claude's MCP logs.

Run this command in your terminal to see the latest errors:
```bash
tail -n 50 ~/Library/Logs/Claude/mcp*.log
```

**Common errors logged here:**
- `uv not found`: You mistyped the absolute path in your config.
- `ModuleNotFoundError`: The `personal-finance-mcp` package isn't installing its dependencies properly when `uv run` executes.
- `SyntaxError` / Python exceptions: There is a bug in the code of your server.
