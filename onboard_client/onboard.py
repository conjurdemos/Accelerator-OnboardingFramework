#!/usr/bin/python3

import json
import sys
import logging
import requests
from onboard_client import *

logfile = "./logs/offboard_client.log"
loglevel = logging.INFO       # BEWARE! DEBUG loglevel can leak secrets!
logfmode = 'w'                # w = overwrite, a = append

# Constants ============================================
BASE_URL="http://localhost:8000"
NOAUTH_HEADERS = { "Content-Type": "application/json" }

# MAIN =================================================
logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel, filemode=logfmode)

# Get provisioning request from single filename argument
try:
  if len(sys.argv) != 2:
    raise IOError
  reqfile = sys.argv[1]
  with open(reqfile) as f_in:
    prov_req = json.load(f_in)
except IOError:
    err_msg = f"{sys.argv[0]}: Could not read provisioning request from filename argument."
    print(err_msg)
    logging.error(err_msg)
    sys.exit(-1)

print("Generating safe name based on provisioning request values...")
url = BASE_URL+"/getsafename"
payload = json.dumps(prov_req)
resp_dict = json.loads(requests.request("GET", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict)
prov_req["safe_name"] = resp_dict["safe_name"]
logging.info(f"safe_name: {resp_dict['safe_name']}")

print("Determining platform ID based on provisioning request values...")
url = BASE_URL+"/getplatformid"
payload = json.dumps(prov_req)
resp_dict = json.loads(requests.request("GET", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict)
prov_req["platform_id"] = resp_dict["platform_id"]
logging.info(f"platform_id: {resp_dict['platform_id']}")

print("Validating request account properties with platform properties...")
url = BASE_URL+"/validaterequest"
payload = json.dumps(prov_req)
resp_dict = json.loads(requests.request("GET", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict)
logging.info(f"Request validated with platform.")

print("Getting admin creds...")
resp_dict = getAuthnCreds()
errCheck(resp_dict)
admin_creds = resp_dict["admin_creds"]

print("Authenticating...")
url = BASE_URL+"/authncyberark"
payload = json.dumps(admin_creds)
resp_dict = json.loads(requests.request("GET", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict)
logging.info("Successfully authenticated.")
prov_req["session_token"] = resp_dict["session_token"]
prov_req["cybr_subdomain"] = admin_creds["cybr_subdomain"]

print("Creating safe...")
url = BASE_URL+"/createsafe"
payload = json.dumps(prov_req)
resp_dict = json.loads(requests.request("POST", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict, expected=[201,409])
logging.info(f"Safe {prov_req['safe_name']} was created or already existed.")

print("Adding members...")
url = BASE_URL+"/addsafemembers"
payload = json.dumps(prov_req)
resp_dict = json.loads(requests.request("POST", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict, expected=[201,409])
logging.info("Safe members such as were found, are now members of the safe.")
             
print(f"Creating account...")
url = BASE_URL+"/createaccount"
payload = json.dumps(prov_req)
resp_dict = json.loads(requests.request("POST", url, headers=NOAUTH_HEADERS, data=payload).text)
errCheck(resp_dict, expected=[201,409])
logging.info("Account exists in safe.")

sys.exit(0)
