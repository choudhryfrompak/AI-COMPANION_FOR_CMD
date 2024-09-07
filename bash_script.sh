#!/bin/bash

PYTHON_SCRIPT="/home/choudhry/projects/ai_cli/groq-ai_cli/main.py"
LOG_FILE="/tmp/ai_complete.log"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

_ai_completions()
{
    log_message "Entering _ai_completions function"
    local cur prev words cword
    _init_completion || return

    log_message "Current word: $cur"
    log_message "Previous word: $prev"
    log_message "All words: ${words[*]}"
    log_message "Current word index: $cword"

    # Remove 'ai' from the beginning if present
    if [ "${words[0]}" = "ai" ]; then
        words=("${words[@]:1}")
        ((cword--))
    fi

    log_message "Calling Python script: $PYTHON_SCRIPT ${words[*]}"
    completions=$(python3 "$PYTHON_SCRIPT" "${words[@]}" 2>> "$LOG_FILE")
    log_message "Python script output: $completions"

    COMPREPLY=($(compgen -W "$completions" -- "$cur"))
    log_message "COMPREPLY set to: ${COMPREPLY[*]}"
}

ai() {
    log_message "Entering ai function with arguments: $*"
    
    if [ $# -eq 0 ]; then
        log_message "Error: No arguments provided"
        echo "Error: No command provided"
        return 1
    fi
    
    if [ "${@: -1}" == "--assist" ]; then
        log_message "Assist mode detected"
        python3 "$PYTHON_SCRIPT" "$@"
    else
        local cmd="$*"
        log_message "Command to execute: $cmd"
        
        # Execute the command
        "$@"
        
        local exit_code=$?
        log_message "Command exit code: $exit_code"
        
        if [ $exit_code -ne 0 ]; then
            log_message "Command failed with exit code $exit_code"
        fi
    fi
}

# Set up completion
complete -F _ai_completions ai

log_message "ai-complete.sh initialized with completion"

# Test Python script
log_message "Testing Python script execution"
python3 "$PYTHON_SCRIPT" test 2>> "$LOG_FILE" || log_message "Error executing Python script"
