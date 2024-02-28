# updateSafeNameRules.py

import json
import logging

def updateSafeNameRules(safenamerules):
    try:
        # SAFENAMERULES_FILE constant defined in onboard-main.py
        with open(SAFENAMERULES_FILE, "w") as f_out:
            f_out.write(json.dumps(safenamerules))
            logging.info(f"Updated safe name rules file {SAFENAMERULES_FILE}")
    except IOError:
        err_msg = f"Could not write safe name rules to file {SAFENAMERULES_FILE}."
        logging.error(err_msg)
