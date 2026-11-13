# Git Version Control & Commit Automation Tool

A terminal-based Python CLI tool designed to automate local Git workflows, generate realistic commit histories, and push changes directly to GitHub. Whether you want to set up your Git profile quickly, generate a batch of local commits, or populate commit activity across a custom date range, this script handles it through a simple interactive menu.

---

## How to Use

### 1. Prerequisites
Make sure you have **Python 3** and **Git** installed on your system:
```bash
git --version
python3 --version
```

### 2. Run the Script
Run the script directly from your terminal inside your project folder (or any folder—it will initialize a Git repository for you if one doesn't exist):
```bash
python3 main.py
```
*(Replace `main.py` with whatever you named the script file.)*

### 3. Follow the Interactive Menu
Once launched, choose from four options:

1. **Config (Necessary for new users):** Sets your global `user.name` and `user.email` so Git knows who is making the commits.
2. **Direct push file to GitHub:** Connects your local repository to a GitHub remote URL, generates a chosen number of commits (1–100), authenticates via your username and Personal Access Token (PAT), and pushes to your active branch.
3. **Only commit:** Generates 1–100 commits locally without pushing anything to a remote server.
4. **Selective commits (Target specific dates):** Lets you enter a custom start date, end date (`YYYY-MM-DD`), and daily commit range (e.g., `3-5`), generating commits distributed naturally across that timeline.

> **Tip:** You can type `q` and press **Enter** at any prompt to exit the program immediately.

---

## Key Features & How It Works

### Automated Commit Simulation
When generating commits, the script appends realistic developer notes and code comments to a local file (`txt.txt`) and pairs each change with varied, authentic-sounding commit messages (e.g., *"Refactor core logic"*, *"Fix parsing bug"*, *"Optimize processing loop"*).

### Custom Date & Timeline Shaping (Option 4)
Instead of dumping all commits at the exact current timestamp, the **Selective Commits** mode modifies Git's environment variables (`GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`) for each commit:
* **Natural Workday Hours:** Starts daily activity randomly between **9:00 AM and 11:00 AM**.
* **Realistic Spacing:** Spaces subsequent commits on the same day by random intervals between **30 minutes and 2 hours**.
* **Flexible Daily Volume:** Supports ranges like `0-4` or `3 to 5`, randomly picking how many commits occur on each day within your chosen date window.

### Safe Credential Handling for Pushing
When pushing to GitHub via HTTPS (Option 2):
* Password/Token input is masked using `getpass` so it never appears on screen.
* Special characters in your token are URL-encoded automatically to prevent authentication errors.
* After the push finishes, the script immediately strips your credentials from the local Git remote URL so your token isn't left stored in `.git/config`.

---

## Troubleshooting & Notes

* **GitHub Authentication:** GitHub no longer accepts standard account passwords for Git operations over HTTPS. When prompted for `Password/Token`, paste a **GitHub Personal Access Token (PAT)** with `repo` permissions.
* **Empty Repositories:** If you are pushing to a brand-new repository on GitHub, leave it empty (do not initialize it with a README or license on GitHub first) to avoid merge conflicts on the initial push.
* **File Generated:** The script creates and modifies `txt.txt` in the current directory to register file changes for each commit.
