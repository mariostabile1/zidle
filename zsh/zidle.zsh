# Zidle - Zsh Terminal Screensaver
export ZIDLE_DIR="${ZIDLE_DIR:-${${(%):-%x}:A:h:h}}"

# Auto-initialize config folder for Zinit zero-config installs
if [[ ! -f "$HOME/.config/zidle/config.json" ]]; then
    mkdir -p "$HOME/.config/zidle"
    cp "$ZIDLE_DIR/config/config.json" "$HOME/.config/zidle/config.json" 2>/dev/null || true
fi

__zidle_load_timeout() {
    local config_file="$HOME/.config/zidle/config.json"
    if [[ -f "$config_file" ]]; then
        # Parse JSON with python instead of regex for better reliability
        local timeout_val
        timeout_val=$(python3 -c '
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    timeout = data.get("timeout", 60)
    timeout = int(timeout)
    print(timeout if timeout >= 0 else 60)
except Exception:
    print(60)
' "$config_file" 2>/dev/null)
        if [[ -n "$timeout_val" ]]; then
            if [[ "$timeout_val" -eq 0 ]]; then
                unset TMOUT
            else
                export TMOUT=$timeout_val
            fi
        else
            export TMOUT=60
        fi
    else
        export TMOUT=60
    fi
}

__zidle_load_timeout

function TRAPALRM() {
    # TMOUT triggers TRAPALRM when idle at the prompt.
    # We trigger the Python screensaver logic here without exiting Zsh.
    
    python3 "$ZIDLE_DIR/core/main.py"
    
    # Reload timeout configuration safely in case it changed
    __zidle_load_timeout
    
    # Force a redraw of the prompt so the terminal restores instantly
    if zle >/dev/null 2>&1; then
        zle reset-prompt 2>/dev/null || true
    fi
    return 0
}

zidle() {
    if [[ "$1" == "start" ]]; then
        python3 "$ZIDLE_DIR/core/main.py"
    elif [[ "$1" == "stop" ]]; then
        unset TMOUT
        echo "Zidle is disabled for this session."
    elif [[ "$1" == "reload" ]]; then
        __zidle_load_timeout
        echo "Zidle configuration reloaded (TMOUT=${TMOUT:-disabled})."
    else
        echo "Usage: zidle [start|stop|reload]"
    fi
}
