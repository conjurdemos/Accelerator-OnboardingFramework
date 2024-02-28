#!/usr/bin/python3

'''
 Utility to retrieve platform map JSON.
 Raw json output is sent to stdout for further redirection to jq or file.
 Therefore DO NOT ADD PRINT STATEMENTS if you're piping this output to jq!!
 Use logging.info(msgs) instead.
'''

import requests
import sys
import json
import logging
from onboard_client import *

logfile = "./logs/getplatmap.log"
loglevel = logging.INFO
logfmode = 'w'  			# w = overwrite, a = append

# Constants ============================================
BASE_URL="http://localhost:8000"
NOAUTH_HEADERS = { "Content-Type": "application/json" }

# MAIN ====================================================
logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel, filemode=logfmode)

logging.info("Getting admin creds...")
resp_dict = getAuthnCreds()
errCheck(resp_dict)
admin_creds = resp_dict["admin_creds"]

logging.info("Authenticating...")
url = BASE_URL+"/authncyberark"
payload = json.dumps(admin_creds)
resp_dict = json.loads(requests.request("GET", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict)
logging.info("Successfully authenticated.")
auth_dict = {}
auth_dict["session_token"] = resp_dict["session_token"]
auth_dict["cybr_subdomain"] = admin_creds["cybr_subdomain"]

url = BASE_URL+"/getplatformmap"
payload = json.dumps(auth_dict)
response = requests.request("GET", url, headers=NOAUTH_HEADERS, data=payload)
if response.status_code == 200:
  print(response.text)
  logging.info(f"Successfully retrieved platform map.")
else:
  err_msg = f"Error retrieving platform map."
  print(err_msg)
  print(response.text)
  logging.error(err_msg)
  logging.error(response.text)
  sys.exit(-1)