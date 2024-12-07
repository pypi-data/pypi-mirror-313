import os
import sys

"""
Runs the daily note processing script from obsidian_workflow for the selected file
"""

SCRIPT_NAME = "OW:DailyNote"


def log(message):
    print(f"{SCRIPT_NAME}:{message}")


python_script = sys.argv[0]
file_path = sys.argv[2]
vault_path = sys.argv[1]

if not file_path:
    log("No file path provided.")
    sys.exit(1)

file_path = os.path.abspath(os.path.join(vault_path, file_path))

log(f"Processing file: {file_path}")


def process_daily_note(daily_note_path):
    """Processes a single daily note."""
    try:
        from obsidian_workflow.daily import process_daily_note
    except ImportError:
        print("Error: Could not import process_daily_note from obsidian_workflow.daily")
        sys.exit(1)
