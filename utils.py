#utils.py
import os
import platform

def get_environment_info():
    return {
        "current_directory": os.getcwd(),
        "os_info": f"{platform.system()} {platform.release()}",
        "shell": os.getenv("SHELL", "unknown shell"),
    }

def get_command_history(limit=10):
    shell = os.environ.get('SHELL', '')
    if 'bash' in shell:
        history_file = os.path.expanduser('~/.bash_history')
    elif 'zsh' in shell:
        history_file = os.path.expanduser('~/.zsh_history')
    else:
        return "Unable to determine shell history file."

    try:
        with open(history_file, 'r') as f:
            history = f.readlines()
        return '\n'.join(history[-limit:])
    except Exception as e:
        return f"Error reading command history: {str(e)}"

def get_current_directory_contents():
    try:
        contents = os.listdir(os.getcwd())
        return [item for item in contents if not item.startswith('.')]  # Exclude hidden files
    except Exception as e:
        return f"Error reading directory contents: {str(e)}"