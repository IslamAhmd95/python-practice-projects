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
# 3. Upgrade pip
# -----------------------------
`pip3 install --upgrade pip`

## Why upgrade pip inside a new venv?
    When you create a virtual environment (python3 -m venv .venv), the pip that comes with it is often outdated.

        This means it might not support the latest package installation standards (like new wheels or dependency resolvers).

        Some libraries may fail to install cleanly with an old pip.


# -----------------------------
# 4. Deactivate the Virtual Environment
# -----------------------------
`deactivate`

## What Happens When You Deactivate a Virtual Environment?
    It restores your terminal to its normal state, using the system-wide Python installation instead of the one inside .venv.

        The (.venv) prefix will disappear from your terminal.

        Any Python commands (python, pip, etc.) will now use the system-wide versions.


# -----------------------------
# 5. Freeze Current Installed Packages
# -----------------------------
# After installing a new package, I should run this command again
`pip3 freeze > requirements.txt`


# -----------------------------
# 6. Install Packages from requirements.txt
# -----------------------------
`pip3 install -r requirements.txt`
