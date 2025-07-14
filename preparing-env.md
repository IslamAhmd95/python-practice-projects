# -----------------------------
# 1. Create a Virtual Environment (recommended for each project)
# -----------------------------
`python3 -m venv .venv`


# -----------------------------
# 2. Activate the Virtual Environment
# -----------------------------
`source .venv/bin/activate`

## What Does Activating a Virtual Environment Mean?
    When you activate a virtual environment (venv), you are telling your terminal to use the Python and dependencies installed inside that environment instead of the system-wide Python installation.

        Each virtual environment has its own isolated Python interpreter and installed packages.

        When activated, commands like python and pip will refer to the versions inside .venv, not the system-wide ones.

        This helps avoid conflicts between different projects with different dependencies.


# -----------------------------
# 3. Deactivate the Virtual Environment
# -----------------------------
`deactivate`

## What Happens When You Deactivate a Virtual Environment?
    It restores your terminal to its normal state, using the system-wide Python installation instead of the one inside .venv.

        The (.venv) prefix will disappear from your terminal.

        Any Python commands (python, pip, etc.) will now use the system-wide versions.


# -----------------------------
# 4. Freeze Current Installed Packages
# -----------------------------
# After installing a new package, I should run this command again
`pip freeze > requirements.txt`


# -----------------------------
# 5. Install Packages from requirements.txt
# -----------------------------
`pip install -r requirements.txt`
