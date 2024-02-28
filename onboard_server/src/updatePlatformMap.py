# updatePlatformMap.py

import json
import logging

def updatePlatformMap(platform_map):
    try:
        # PLATFORMMAP_FILE constant defined in onboard-main.py
        with open(PLATFORMMAP_FILE, "w") as f_out:
            f_out.write(json.dumps(platform_map))
            logging.info(f"Updated platform map file {PLATFORMMAP_FILE}")
    except IOError:
        err_msg = f"Could not write platform map to file {PLATFORMMAP_FILE}."
        logging.error(err_msg)
