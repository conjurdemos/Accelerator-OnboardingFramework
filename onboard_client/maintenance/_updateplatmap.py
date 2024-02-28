#!/usr/bin/python3

import requests
import json
import sys
import logging
from onboard_client import *

logfile = "./logs/updateplatmap.log"
loglevel = logging.INFO
logfmode = 'w'  			# w = overwrite, a = append

# Constants ============================================
BASE_URL="http://localhost:8000"
NOAUTH_HEADERS = { "Content-Type": "application/json" }

# MAIN ====================================================
logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel, filemode=logfmode)

# Get local safe name rules json file from single filename argument
try:
  if len(sys.argv) != 2:
    raise IOError
  platformsfile = sys.argv[1]
  with open(platformsfile) as f_in:
    platmap = json.load(f_in)
except IOError:
  err_msg = f"Could not read platform map json from filename argument."
  print(err_msg)
  logging.error(err_msg)
  sys.exit(-1)

# send to server to update rules there
url = BASE_URL+"/updateplatformmap"
payload = json.dumps(platmap)
response = requests.request("PUT", url, headers=NOAUTH_HEADERS,data=payload)
if response.status_code == 200:
  success_msg = f"Successfully updated platform map with file {platformsfile}."
  print(success_msg)
  logging.info(success_msg)
else:
  err_msg = f"Error updating platform map with file {platformsfile}"
  print(err_msg)
  logging.error(err_msg)
  logging.error(response.text)
  sys.exit(-1)