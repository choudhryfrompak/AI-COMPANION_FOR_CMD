#ai_assist.py
import os
from dotenv import load_dotenv
from groq import Groq
from utils import get_environment_info
from prompts import generate_assist_prompt
from api import query_groq

load_dotenv()

def generate_command(input_text):
    env_info = get_environment_info()
    prompt = generate_assist_prompt(input_text, env_info)
    
    try:
        command = query_groq(prompt)
        return command.strip()
    except Exception as e:
        print(f"Error generating command: {e}")
        return None

def execute_command(command):
    print(f"\033[92m{command}\033[0m")
    confirm = input("Press 'Enter' to execute the command or 'n' to cancel: ")
    if confirm.lower() != "n":
        os.system(command)
    else:
        print("Command execution cancelled.")

def ai_assist(input_text):
    command = generate_command(input_text)
    if command:
        execute_command(command)
    else:
        print("Failed to generate a command.")