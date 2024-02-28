#!/usr/bin/python3

import json
import sys
import requests
import logging
from onboard_client import *

logfile = "./logs/updatesafenamerules.log"
loglevel = logging.INFO
logfmode = 'w'  			# w = overwrite, a = append

# Constants ============================================
BASE_URL="http://localhost:8000"
NOAUTH_HEADERS = { "Content-Type": "application/json" }

# MAIN ====================================================
logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel, filemode=logfmode)

# Get safe name rules json file from single filename argument
try:
  if len(sys.argv) != 2:
    raise IOError
  rulesfile = sys.argv[1]
  with open(rulesfile) as f_in:
    safenamerules = json.load(f_in)
except IOError:
    err_msg = f"{sys.argv[0]}: Could not read safe name rules json from filename argument."
    print(err_msg)
    logging.error(err_msg)
    sys.exit(-1)

url = BASE_URL+"/updatesafenamerules"
payload = json.dumps(safenamerules)
response = requests.request("PUT", url, headers=NOAUTH_HEADERS,data=payload)
if response.status_code == 200:
  success_msg = f"Successfully updated safe name rules with file {rulesfile}."
  print(success_msg)
  logging.info(success_msg)
else:
  err_msg = f"Error updating safe name rules with file {rulesfile}"
  print(err_msg)
  logging.error(err_msg)
  logging.error(response.text)
  sys.exit(-1)