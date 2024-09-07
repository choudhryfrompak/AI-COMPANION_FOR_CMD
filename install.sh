#!/bin/bash

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_colored() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}$1${NC}"
}

# Check if script is run as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root"
   exit 1
fi

# Install dependencies
print_colored "Installing dependencies..."
apt install -y python3 python3-pip python3-venv git

# Ask for installation directory
read -p "Enter the directory to install the AI CLI tool (default: /opt/ai-cli): " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-/opt/ai-cli}

# Clone the repository
print_colored "Cloning the repository..."
git clone https://github.com/choudhryfrompak/groq_ai-cli.git "$INSTALL_DIR"

# Create virtual environment
print_colored "Creating virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"

# Activate virtual environment
source "$INSTALL_DIR/venv/bin/activate"

# Install requirements
print_colored "Installing Python requirements..."
pip install -r "$INSTALL_DIR/requirements.txt"

# Copy .env.example to .env
cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"

# Ask for Groq API token
read -p "Enter your Groq API token: " GROQ_API_TOKEN

# Add Groq API token to .env file
echo "GROQ_API_KEY=$GROQ_API_TOKEN" >> "$INSTALL_DIR/.env"

# Create a wrapper script
print_colored "Creating wrapper script..."
cat > /usr/local/bin/ai << EOL
#!/bin/bash
source $INSTALL_DIR/venv/bin/activate
python3 $INSTALL_DIR/main.py "\$@"
EOL

chmod +x /usr/local/bin/ai

# Add bash completion
print_colored "Setting up bash completion..."
cat > /etc/bash_completion.d/ai << EOL
#!/bin/bash

PYTHON_SCRIPT="$INSTALL_DIR/main.py"
LOG_FILE="/tmp/ai_complete.log"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] \$1" >> "\$LOG_FILE"
}

_ai_completions()
{
    log_message "Entering _ai_completions function"
    local cur prev words cword
    _init_completion || return

    log_message "Current word: \$cur"
    log_message "Previous word: \$prev"
    log_message "All words: \${words[*]}"
    log_message "Current word index: \$cword"

    # Remove 'ai' from the beginning if present
    if [ "\${words[0]}" = "ai" ]; then
        words=("\${words[@]:1}")
        ((cword--))
    fi

    log_message "Calling Python script: \$PYTHON_SCRIPT \${words[*]}"
    completions=\$(python3 "\$PYTHON_SCRIPT" "\${words[@]}" 2>> "\$LOG_FILE")
    log_message "Python script output: \$completions"

    COMPREPLY=(\$(compgen -W "\$completions" -- "\$cur"))
    log_message "COMPREPLY set to: \${COMPREPLY[*]}"
}

ai() {
    log_message "Entering ai function with arguments: \$*"

    if [ \$# -eq 0 ]; then
        log_message "Error: No arguments provided"
        echo "Error: No command provided"
        return 1
    fi

    if [ "\${@: -1}" == "--assist" ]; then
        log_message "Assist mode detected"
        python3 "\$PYTHON_SCRIPT" "\$@"
    else
        local cmd="\$*"
        log_message "Command to execute: \$cmd"

        # Execute the command
        "\$@"

        local exit_code=\$?
        log_message "Command exit code: \$exit_code"

        if [ \$exit_code -ne 0 ]; then
            log_message "Command failed with exit code \$exit_code"
        fi
    fi
}

# Set up completion
complete -F _ai_completions ai

log_message "ai-complete.sh initialized with completion"
EOL

# Update .bashrc for all users
print_colored "Updating .bashrc for all users..."
echo "source /etc/bash_completion.d/ai" >> /etc/bash.bashrc

# Add ai function to /etc/bash.bashrc
print_colored "Adding ai function to /etc/bash.bashrc..."
cat >> /etc/bash.bashrc << EOL

# AI CLI function
ai() {
    source /etc/bash_completion.d/ai
    ai "\$@"
}
EOL

print_colored "AI CLI tool has been successfully installed!"
print_colored "Please restart your terminal or run 'source /etc/bash.bashrc' to enable bash completion and the ai function."
print_colored "You can now use the 'ai' command from anywhere in the terminal."