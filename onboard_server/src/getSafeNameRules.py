# getSafeNameRules.py

import json
import logging

def getSafeNameRules():
    try:
        # SAFENAMERULES_FILE constant is defined in onboard-main.py
        with open(SAFENAMERULES_FILE) as f_in:
            safenamerules = json.load(f_in)
    except IOError:
        err_msg = f"Could not read safe name rules from file {SAFENAMERULES_FILE}."
        logging.error(err_msg)
        safenamerules = {}
    return safenamerules
