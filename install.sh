#!/usr/bin/env bash
set -e

echo "Installing Zidle..."

ZIDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Security: the resolved path is frozen into ~/.zshrc and re-sourced at
# every shell start. Refuse world-writable-creatable locations (e.g. /tmp):
# once the original tree is removed, any local user can re-create the same
# path and gain code execution in every future shell of this account.
_p="$ZIDLE_DIR"
while true; do
    if [ -n "$(find "$_p" -maxdepth 0 -perm -0002 2>/dev/null)" ]; then
        echo "ERROR: refusing to install from world-writable location '$_p'." >&2
        echo "Move the zidle directory to a private location (e.g. under \$HOME) and re-run ./install.sh." >&2
        exit 1
    fi
    if [ "$_p" = "/" ]; then
        break
    fi
    _p="$(dirname "$_p")"
done
unset _p
CONFIG_DIR="$HOME/.config/zidle"

echo "1. Creating config directory..."
mkdir -p "$CONFIG_DIR"

echo "2. Copying default config..."
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cp "$ZIDLE_DIR/config/config.json" "$CONFIG_DIR/"
else
    echo "Config already exists, skipping."
fi

echo "3. Adding Zsh integration..."
ZSHRC="$HOME/.zshrc"

# Ensure ~/.zshrc exists before grep when running with set -e
touch "$ZSHRC"

# Key the idempotency gate on the exact frozen path for this location:
# re-running install.sh from a new place must refresh the .zshrc reference,
# not report "already installed" while a stale path keeps dangling.
if grep -qF "export ZIDLE_DIR=\"$ZIDLE_DIR\"" "$ZSHRC"; then
    echo "Zidle is already installed in $ZSHRC."
else
    echo "" >> "$ZSHRC"
    echo "# Zidle Screensaver" >> "$ZSHRC"
    echo "export ZIDLE_DIR=\"$ZIDLE_DIR\"" >> "$ZSHRC"
    echo "source \"\$ZIDLE_DIR/zsh/zidle.zsh\"" >> "$ZSHRC"
    echo "Added Zidle integration to $ZSHRC"
fi

echo "Installation complete! Please restart your terminal or run 'source ~/.zshrc'."
