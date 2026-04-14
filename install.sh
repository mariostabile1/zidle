#!/usr/bin/env bash
set -e

echo "Installing Zidle..."

ZIDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
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

if grep -q "ZIDLE_DIR" "$ZSHRC"; then
    echo "Zidle is already installed in $ZSHRC."
else
    echo "" >> "$ZSHRC"
    echo "# Zidle Screensaver" >> "$ZSHRC"
    echo "export ZIDLE_DIR=\"$ZIDLE_DIR\"" >> "$ZSHRC"
    echo "source \"\$ZIDLE_DIR/zsh/zidle.zsh\"" >> "$ZSHRC"
    echo "Added Zidle integration to $ZSHRC"
fi

echo "Installation complete! Please restart your terminal or run 'source ~/.zshrc'."
