#profile.py
import json
import os
import platform
import psutil
import git
import subprocess
from datetime import datetime

def get_recent_files(directory, days=7):
    recent_files = []
    now = datetime.now()
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if (now - datetime.fromtimestamp(os.path.getmtime(file_path))).days <= days:
                recent_files.append(file_path)
    return recent_files

def get_git_info():
    try:
        repo = git.Repo(search_parent_directories=True)
        return {
            "repo_name": os.path.basename(repo.working_tree_dir),
            "current_branch": repo.active_branch.name,
            "recent_commits": [commit.message.strip() for commit in repo.iter_commits(max_count=5)]
        }
    except git.InvalidGitRepositoryError:
        return None

def collect_enhanced_user_profile():
    profile = {}

    print("Welcome! Let's set up your detailed user profile to improve AI-generated commands.")

    # User-specific questions
    profile['experience_level'] = input("1. Rate your programming experience (1-10): ")
    profile['primary_role'] = input("2. What's your primary role? (e.g., Frontend Developer, Data Scientist): ")
    profile['languages'] = input("3. List programming languages you use, separated by commas: ").split(',')
    profile['frameworks'] = input("4. List frameworks/libraries you frequently use: ").split(',')
    profile['text_editor'] = input("5. What's your primary text editor or IDE?: ")
    profile['version_control'] = input("6. What version control system do you use? (e.g., Git, SVN): ")
    profile['command_line_tools'] = input("7. List command-line tools you frequently use: ").split(',')
    profile['project_types'] = input("8. What types of projects do you typically work on?: ")
    profile['package_managers'] = input("9. List package managers you use: ").split(',')
    profile['database_systems'] = input("10. List database systems you work with: ").split(',')
    profile['cloud_services'] = input("11. List cloud services or platforms you use: ").split(',')
    profile['ci_cd_tools'] = input("12. List any CI/CD tools you use: ").split(',')
    profile['containerization'] = input("13. Do you use containerization? If yes, which technology? (e.g., Docker): ")
    profile['testing_frameworks'] = input("14. List testing frameworks you're familiar with: ").split(',')
    profile['terminal_emulator'] = input("15. What's your preferred terminal emulator?: ")
    profile['shell'] = input("16. What shell do you primarily use? (e.g., bash, zsh): ")
    profile['output_preference'] = input("17. Do you prefer verbose or concise command output? (Verbose/Concise): ")
    profile['code_style'] = input("18. Do you follow any specific code style guide? (e.g., PEP8 for Python): ")
    profile['accessibility_needs'] = input("19. Do you have any accessibility needs for command output?: ")
    profile['preferred_language'] = input("20. Preferred language for command explanations: ")

    # Machine-specific information
    profile['os'] = platform.system()
    profile['os_release'] = platform.release()
    profile['cpu'] = platform.processor()
    profile['ram'] = f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
    profile['python_version'] = platform.python_version()

    # Current directory and work analysis
    current_dir = os.getcwd()
    profile['current_directory'] = current_dir
    profile['recent_files'] = get_recent_files(current_dir)
    profile['git_info'] = get_git_info()

    # Additional system information
    try:
        profile['installed_packages'] = subprocess.check_output("pip list", shell=True).decode().split('\n')
    except subprocess.CalledProcessError:
        profile['installed_packages'] = []

    try:
        profile['environment_variables'] = dict(os.environ)
    except Exception:
        profile['environment_variables'] = {}

    # Save the profile
    with open('enhanced_user_profile.json', 'w') as f:
        json.dump(profile, f, indent=2)

    print("Enhanced profile saved successfully!")
    return profile

def get_or_create_enhanced_user_profile():
    if os.path.exists('enhanced_user_profile.json'):
        with open('enhanced_user_profile.json', 'r') as f:
            return json.load(f)
    else:
        print("Creating new user profile...")
        return collect_enhanced_user_profile()