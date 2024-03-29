
#############################################################################
#############################################################################
# getSafeName.py

import json
import logging

'''
 The design intention of this function is to automate CyberArk's
 recommended best-practices for safe naming described in this document:
 https://cyberark.my.site.com/s/article/Safe-Naming-Convention-Best-Practices

 - Name must be <= 28 characters long
 - Format: E-LOC-GRP-TEC-SUB-AT-A where:
 - E = Environment:
    Production (P), Development (D), Testing (T), Q/A (Q), etc
 - LOC = Geographical Location or domain:
    Datacenter 1 (DC1), Datacenter 2 (DC2), California Datacenter (CA), etc
 - GRP = Business Unit/Access Groups/Application:
    Security Team (SEC), Engineering Team (ENG), Support Desk (SUP), Network Team Routers (NWR), Network Team Switches (NWS), etc
 - TEC = Technology:
    Server (SVR), Workstation (WKS), Network Device (NET), Database (DB), Mainframe (MF), Domain (DOM) etc
 - SUB = Technology Subtype (flavor):
    Windows (WIN), UNIX (UNX), Linux (LNX), HP-UX (HP), Cisco (CSC), SQL Database (SQL), Oracle Database (ORC)
 - AT = Account Type:
    Local Account (LA), Domain Account (DA), Local Service Account (LS), Domain Service Account (DS), Root (RT), Enable Account (EN), SQL SA Account (SA)
 - A = Auto-Detection Enabled Safe   (required only if using auto-detection for local accounts

 Recognizing that this best-practice is just a starting point, and that it
 may not support non-human access conventions, this function supports
 adaptations of the practice per customer requirements.

 It generates a safe name based on values in the provisioning request per
  rules defined in ./json/safenamerules.json (path is relative to function
  calling this function).
'''

def getSafeName(prov_req):

  with open("./json/safenamerules.json") as sr:
      saferules = json.load(sr)["safenamerules"]

  logging.debug("================ getSafeName() ================")
  status_code = 200
  response_body = "Safe name generated."
  safe_name = ""

  # first ensure we have request values required for rules
  # get names of request keys in rules from which to compose safe name
  required_keys = [ r["keyname"] for r in saferules ]
  for idx in range(len(required_keys)):
    input_val = prov_req.get(required_keys[idx],None)
    if input_val is None:
      status_code = 400
      err_msg = f"Missing key required for safe naming: {required_keys[idx]}"
      logging.error(err_msg)
      response_body = err_msg

  # all values converted to uppercase strings for comparisons
  if status_code == 200:
    for rule in saferules:
        keyval = prov_req[rule["keyname"]]
        outval = None
        match rule["maptype"]:
            case "valuemap":
                for vmap in rule["valuemap"]:
                    upvals = [v.upper() for v in vmap["inputs"]]
                    if str(keyval).upper() in upvals:
                        outval = vmap["output"].upper()
                        break
            case "literal":
                outval = str(keyval).upper()
            case "substring":
                beg = rule["substring"]["start"]
                if beg > len(str(keyval)):
                  beg = 0             # dubious error correction
                end = rule["substring"]["end"]
                if end > len(str(keyval)):
                  end = len(str(keyval))
                outval = str(keyval)[beg:end].upper()
            case _:
                logging.error(f"Invalid maptype: {rule['maptype']}")

        if outval is not None:
            if safe_name != "":
                safe_name += "-"
            safe_name += outval
        else:
            status_code = 400
            err_msg = f"No safename mapping rule found for {keyval}"
            logging.error(err_msg)
            response_body = err_msg
            break
    response_body = f"Safe name generated: {safe_name}"

  logging.debug(f"\tstatus_code: {status_code}\n\tresponse: {response_body}")

  return_dict = {}
  return_dict["status_code"] = status_code
  return_dict["response_body"] = response_body
  return_dict["safe_name"] = safe_name
  return return_dict
