import os
import sys
import time
import random
import subprocess
import urllib.parse
from getpass import getpass

def run_git_command(command):
    """Executes a git command and correctly checks its success status."""
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, result.stdout.strip()
    except FileNotFoundError:
        return False, "Git command not found"
    except Exception as e:
        return False, str(e)

def prompt_input(text, is_password=False):
    """Handles user input with a universal 'q' escape mechanism."""
    try:
        if is_password:
            val = getpass(text)
        else:
            val = input(text)
            
        if val.strip().lower() == 'q':
            print("\nExiting program...")
            sys.exit(0)
        return val.strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting program...")
        sys.exit(0)

def ensure_repository():
    """Initializes a repository silently if one does not exist."""
    is_repo, _ = run_git_command(['git', 'rev-parse', '--is-inside-work-tree'])
    
    if not is_repo:
        run_git_command(['git', 'init'])
        run_git_command(['git', 'branch', '-M', 'main'])
        print("Initialized empty Git repository.")

def configure_git():
    """Handles the first-time Git configuration."""
    print("\n--- Git Configuration ---")
    name = prompt_input("Enter your Git Display Name (e.g., John Doe): ")
    email = prompt_input("Enter your Git Email (e.g., john@example.com): ")
    
    # Apply globally so the user doesn't have to do it again for other projects
    run_git_command(['git', 'config', '--global', 'user.name', name])
    run_git_command(['git', 'config', '--global', 'user.email', email])
    
    print("\nConfiguration saved successfully!")

def generate_commits(commit_amount):
    """Handles the creation of authentic-looking file changes and commits."""
    file_name = "txt.txt"
    
    commit_messages = [
        "Update documentation",
        "Refactor core logic",
        "Fix minor typo in definitions",
        "Clean up trailing whitespace",
        "Optimize processing loop",
        "Add error handling for edge cases",
        "Update configuration values",
        "Remove deprecated variables",
        "Fix parsing bug",
        "Tweak file formatting",
        "Resolve merge conflict",
        "Add developer comments to complex block",
        "Patch security vulnerability in dependencies"
    ]

    file_contents = [
        "// Refactored the main loop for better memory efficiency.\n",
        "# TODO: Verify these changes on the staging environment before production.\n",
        "// Fixed a potential memory leak located in the parsing function.\n",
        "/* Updated local dependencies to match the latest stable release. */\n",
        "// Temporary workaround applied; schedule a proper fix for the next sprint.\n",
        "# Added verbose logging for debugging incoming data streams.\n",
        "// Cleaned up the syntax and standardized the formatting rules.\n",
        "/* Note: Review edge cases regarding null inputs before next major release. */\n",
        "// Optimized the query response time by restructuring the data payload.\n"
    ]

    print(f"\nProcessing {commit_amount} commits...")

    for i in range(1, commit_amount + 1):
        try:
            current_message = random.choice(commit_messages)
            current_text = random.choice(file_contents)

            with open(file_name, "a") as f:
                f.write(current_text)

            success_add, err_add = run_git_command(['git', 'add', file_name])
            if not success_add:
                print(f"Error adding file: {err_add}")
                sys.exit(1)

            success_commit, err_commit = run_git_command(['git', 'commit', '-m', current_message])
            if not success_commit:
                print(f"Error committing: {err_commit}")
                print("Hint: If you haven't configured Git, please restart and choose Option 1.")
                sys.exit(1)
            
            print(f"  ✓ [{i}/{commit_amount}] Committed: {current_message}")
            time.sleep(0.1) 

        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            sys.exit(1)

def main():
    while True:
        print("\n===============================")
        print("   Version Control Interface   ")
        print("===============================")
        print("Type 'q' and press Enter at any prompt to exit.\n")
        print("1. Config (Necessary for new users)")
        print("2. Direct push file to GitHub")
        print("3. Only commit")

        choice = prompt_input("\nSelect an option (1, 2, or 3): ")

        if choice == '1':
            configure_git()
            # The loop continues, returning to the main menu
            
        elif choice == '2':
            ensure_repository()
            
            while True:
                repo_link = prompt_input("GitHub Repository Link: ")
                # Check for either http or https to prevent silent failures
                if (repo_link.startswith("https://") or repo_link.startswith("http://")) and repo_link.endswith(".git"):
                    break
                print("Format is not correct.")
                print("Example: https://github.com/Username/Repository.git")
            
            run_git_command(['git', 'remote', 'remove', 'origin']) 
            success_remote, _ = run_git_command(['git', 'remote', 'add', 'origin', repo_link])
            if success_remote:
                print("Successfully connected to the server.")
            else:
                print("Failed to add remote origin.")
                sys.exit(1)

            while True:
                try:
                    amount_str = prompt_input("How many commits do you want to generate? (1-100): ")
                    commit_amount = int(amount_str)
                    if 1 <= commit_amount <= 100:
                        break
                    print("Please enter a number between 1 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            generate_commits(commit_amount)

            success_branch, active_branch = run_git_command(['git', 'branch', '--show-current'])
            if not success_branch or not active_branch:
                active_branch = 'main'

            print("\nAuthentication required for remote push.")
            username = prompt_input("Username: ")
            password = prompt_input("Password/Token: ", is_password=True) 

            safe_password = urllib.parse.quote(password, safe='')
            
            # Dynamically replace the correct protocol (fixes the infinite freeze bug)
            if repo_link.startswith("https://"):
                auth_url = repo_link.replace("https://", f"https://{username}:{safe_password}@")
            else:
                auth_url = repo_link.replace("http://", f"http://{username}:{safe_password}@")
            
            run_git_command(['git', 'remote', 'set-url', 'origin', auth_url])
            
            print(f"Pushing to remote repository on branch '{active_branch}'...")
            success_push, err_push = run_git_command(['git', 'push', '-u', 'origin', active_branch])
            
            run_git_command(['git', 'remote', 'set-url', 'origin', repo_link])

            if success_push:
                print("Successfully done.")
            else:
                print("\nError: Failed to push to the repository.")
                print(f"Git Response: {err_push}")
                print("Please ensure your credentials are correct and the remote repository exists.")
            sys.exit(0) # Exit cleanly after pushing

        elif choice == '3':
            ensure_repository()
            
            while True:
                try:
                    amount_str = prompt_input("How many commits do you want to generate? (1-100): ")
                    commit_amount = int(amount_str)
                    if 1 <= commit_amount <= 100:
                        break
                    print("Please enter a number between 1 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            generate_commits(commit_amount)
            print("\nOperations completed.")
            sys.exit(0) # Exit cleanly after committing
            
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    git_installed, _ = run_git_command(['git', '--version'])
    if not git_installed:
        print("Error: Git is not installed or not recognized by the system.")
        print("Please install Git first.")
        sys.exit(1)
        
    main()