#!/usr/bin/python3

'''
 This is a utility that pulls current safe name rules.

 Raw json output is sent to stdout for further redirection to jq or file.
 Therefore DO NOT ADD PRINT STATEMENTS if you're piping this output to jq!!
 Use logging.info(msgs) instead.
'''

import requests
import json
import sys
import logging
from onboard_client import *

logfile = "./logs/getsafenamerules.log"
loglevel = logging.INFO
logfmode = 'w'  			# w = overwrite, a = append

# Constants ============================================
BASE_URL="http://localhost:8000"
NOAUTH_HEADERS = { "Content-Type": "application/json" }

# MAIN ====================================================
logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel, filemode=logfmode)

url = BASE_URL+"/getsafenamerules"
response = requests.request("GET", url, headers=NOAUTH_HEADERS)
if response.status_code == 200:
  print(response.text)
  logging.info(f"Successfully retrieved safe name rules.")
else:
  err_msg = f"Error retrieving safe name rules."
  print(err_msg)
  print(response.text)
  logging.error(err_msg)
  logging.error(response.text)
  sys.exit(-1)