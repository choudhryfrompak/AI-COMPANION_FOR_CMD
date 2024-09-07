import sys
import os
from prompts import generate_prompt
from profile import get_or_create_enhanced_user_profile
from api import query_groq
from utils import get_environment_info, get_command_history, get_current_directory_contents
from ai_assist import ai_assist

def generate_completions(partial_command, user_profile):
    env_info = get_environment_info()
    command_history = get_command_history()
    directory_contents = get_current_directory_contents()

    context = {
        "user_profile": user_profile,
        "env_info": env_info,
        "command_history": command_history,
        "directory_contents": directory_contents,
        "task": f"Suggest completions for the partial command: {partial_command}"
    }

    prompt = generate_prompt(context)
    suggestions = query_groq(prompt)
    return suggestions.split('\n')

if __name__ == "__main__":
    user_profile = get_or_create_enhanced_user_profile()
    
    if len(sys.argv) > 1 and sys.argv[-1] == "--assist":
        input_text = " ".join(sys.argv[1:-1])
        ai_assist(input_text)
    else:
        partial_command = " ".join(sys.argv[1:])
        completions = generate_completions(partial_command, user_profile)
        print(" ".join(completions))