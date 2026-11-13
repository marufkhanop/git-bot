import os
import sys
import time
import random
import subprocess
import urllib.parse
from getpass import getpass
from datetime import datetime, timedelta

# Realistic commit data shared across functions
COMMIT_MESSAGES = [
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

FILE_CONTENTS = [
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

def run_git_command(command, custom_env=None):
    """Executes a git command, allowing custom environment variables for date spoofing."""
    try:
        env = os.environ.copy()
        if custom_env:
            env.update(custom_env)
            
        result = subprocess.run(command, capture_output=True, text=True, env=env)
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
    
    run_git_command(['git', 'config', '--global', 'user.name', name])
    run_git_command(['git', 'config', '--global', 'user.email', email])
    
    print("\nConfiguration saved successfully!")

def generate_commits(commit_amount):
    """Handles standard authentic-looking file changes and commits."""
    file_name = "txt.txt"
    print(f"\nProcessing {commit_amount} commits...")

    for i in range(1, commit_amount + 1):
        try:
            current_message = random.choice(COMMIT_MESSAGES)
            current_text = random.choice(FILE_CONTENTS)

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

def prompt_date(text):
    """Prompts for a date and enforces the YYYY-MM-DD format."""
    while True:
        val = prompt_input(text)
        try:
            dt = datetime.strptime(val, "%Y-%m-%d")
            return dt
        except ValueError:
            print("Invalid format. Please strictly use YYYY-MM-DD (e.g., 2026-01-21).")

def generate_selective_commits():
    """Handles targeted backdating/forecasting of commits across a date range."""
    file_name = "txt.txt"
    print("\n--- Selective Commits ---")
    
    while True:
        start_date = prompt_date("Enter start date (YYYY-MM-DD): ")
        end_date = prompt_date("Enter end date (YYYY-MM-DD): ")
        
        if start_date <= end_date:
            break
        print("Error: Start date must be before or equal to the end date.")

    while True:
        try:
            range_input = prompt_input("Enter commit range per day (e.g., 3-5 or 3 to 5): ")
            # Basic parsing to handle "3-5", "3 to 5", "3 5"
            parts = range_input.replace("to", "-").replace(" ", "").split("-")
            
            if len(parts) != 2:
                raise ValueError
            
            min_c = int(parts[0])
            max_c = int(parts[1])
            
            if 0 <= min_c <= max_c:
                break
            print("Invalid range. Minimum must be less than or equal to the maximum.")
        except ValueError:
            print("Invalid format. Please enter a valid range like '3-5'.")

    current_date = start_date
    total_days = (end_date - start_date).days + 1

    print(f"\nProcessing timeline across {total_days} days...")

    while current_date <= end_date:
        daily_commits = random.randint(min_c, max_c)
        date_str = current_date.strftime("%Y-%m-%d")
        
        if daily_commits == 0:
            print(f"[{date_str}] Skipping (0 commits rolled)")
            current_date += timedelta(days=1)
            continue
            
        print(f"[{date_str}] Generating {daily_commits} commits...")
        
        # Simulate a natural workday starting between 9 AM and 11 AM
        current_time = current_date.replace(hour=random.randint(9, 11), minute=random.randint(0, 59))
        
        for i in range(1, daily_commits + 1):
            try:
                # Format time perfectly for Git
                git_date_format = current_time.strftime("%Y-%m-%d %H:%M:%S")
                env_vars = {
                    'GIT_AUTHOR_DATE': git_date_format,
                    'GIT_COMMITTER_DATE': git_date_format
                }
                
                current_message = random.choice(COMMIT_MESSAGES)
                current_text = random.choice(FILE_CONTENTS)

                with open(file_name, "a") as f:
                    f.write(current_text)

                success_add, err_add = run_git_command(['git', 'add', file_name])
                if not success_add:
                    print(f"Error adding file: {err_add}")
                    sys.exit(1)

                success_commit, err_commit = run_git_command(['git', 'commit', '-m', current_message], custom_env=env_vars)
                if not success_commit:
                    print(f"Error committing: {err_commit}")
                    sys.exit(1)
                
                print(f"  ✓ [{current_time.strftime('%H:%M')}] Committed: {current_message}")
                
                # Advance time by a natural interval (30 minutes to 2 hours) for the next commit
                current_time += timedelta(minutes=random.randint(30, 120))

            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
                sys.exit(1)
                
        current_date += timedelta(days=1)

def main():
    while True:
        print("\n===============================")
        print("   Version Control Interface   ")
        print("===============================")
        print("Type 'q' and press Enter at any prompt to exit.\n")
        print("1. Config (Necessary for new users)")
        print("2. Direct push file to GitHub")
        print("3. Only commit")
        print("4. Selective commits (Target specific dates)")

        choice = prompt_input("\nSelect an option (1, 2, 3, or 4): ")

        if choice == '1':
            configure_git()
            
        elif choice == '2':
            ensure_repository()
            
            while True:
                repo_link = prompt_input("GitHub Repository Link: ")
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
            sys.exit(0)

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
            sys.exit(0)

        elif choice == '4':
            ensure_repository()
            generate_selective_commits()
            print("\nTimeline operations completed. You can now push these via Option 2 or your terminal.")
            sys.exit(0)
            
        else:
            print("Invalid selection. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    git_installed, _ = run_git_command(['git', '--version'])
    if not git_installed:
        print("Error: Git is not installed or not recognized by the system.")
        print("Please install Git first.")
        sys.exit(1)
        
    main()
