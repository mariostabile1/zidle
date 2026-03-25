# Zinit / Oh-My-Zsh entry point
export ZIDLE_DIR="${ZIDLE_DIR:-${${(%):-%x}:A:h}}"
source "${ZIDLE_DIR}/zsh/zidle.zsh"
