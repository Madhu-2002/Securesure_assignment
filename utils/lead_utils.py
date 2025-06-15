# securesure_bot/utils/lead_utils.py
import os
import json

LEAD_FILE = "db/leads.json"

# Ensure directory and file exist
os.makedirs("db", exist_ok=True)
if not os.path.exists(LEAD_FILE):
    with open(LEAD_FILE, "w") as f:
        json.dump([], f)

def save_lead_to_db(lead_data):
    """
    Save car lead info to a JSON database.
    If the file is empty or corrupted, start with an empty list.
    """
    with open(LEAD_FILE, "r+") as f:
        try:
            leads = json.load(f)
            if not isinstance(leads, list):
                leads = []
        except json.JSONDecodeError:
            leads = []

        leads.append(lead_data)

        f.seek(0)
        json.dump(leads, f, indent=2)
        f.truncate()
