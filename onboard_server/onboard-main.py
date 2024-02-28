# main.py

import logging
from fastapi import FastAPI, Body
from cybronboard import *

logfile = "./logs/onboard-server.log"
loglevel = logging.DEBUG       # BEWARE! DEBUG loglevel can leak secrets!
logfmode = 'w'                # w = overwrite, a = append

# Constants ============================================
PLATFORMMAP_FILE="./json/platforms.json"
SAFENAMERULES_FILE="./json/safenamerules.json"

# MAIN ============================================
logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel, filemode=logfmode)

app = FastAPI()

##############################################
# Endpoints in this section do not require authentication.
# They do not interact with CyberArk APIs.
##############################################
@app.get("/getsafenamerules")
def _getSafeNameRules():
    return getSafeNameRules()

@app.put("/updatesafenamerules")
def _updateSafeNameRules(safename_rules: dict = Body(...)):
    return updateSafeNameRules(safename_rules)

@app.put("/updateplatformmap")
def _updatePlatformMap(platform_map: dict = Body(...)):
    return updatePlatformMap(platform_map)

@app.get("/getsafename")
def _getSafeName(prov_req: dict = Body(...)):
    return getSafeName(prov_req)

@app.get("/getplatformid")
def _getPlatformId(prov_req: dict = Body(...)):
    return getPlatformId(prov_req)

@app.get("/validaterequest")
def _validateRequestWithPlatform(prov_req: dict = Body(...)):
    return validateRequestWithPlatform(prov_req)

##############################################
# Endpoints below require authentication
##############################################

@app.get("/authncyberark")
def _authnCyberark(admin_creds: dict = Body(...)):
    return authnCyberark(admin_creds)

# getPlatformMap pulls active platform info from the vault
@app.get("/getplatformmap")
def _getPlatformMap(auth_dict: dict = Body(...)):
    cybr_subdomain = auth_dict["cybr_subdomain"]
    session_token = auth_dict["session_token"]
    return getPlatformMap(cybr_subdomain, session_token)

# Source & Target stores must already exist
@app.get("/getshsourcestoreid")
def _getSHSourceStoreId(prov_req: dict = Body(...)):
    return getSHSourceStoreId(prov_req)

@app.get("/getshtargetstoreid")
def _getSHTargetStoreId(prov_req: dict = Body(...)):
    return getSHTargetStoreId(prov_req)

#================================
# State-changing endpoints
#================================
@app.post("/createsafe")
def _createSafe(prov_req: dict = Body(...)):
    return createSafe(prov_req)

@app.delete("/deletesafe")
def _deleteSafe(prov_req: dict = Body(...)):
    return deleteSafe(prov_req)

@app.post("/addsafemembers")
def _addSafeMembers(prov_req: dict = Body(...)):
    return addSafeMembers(prov_req)

@app.post("/createaccount")
def _createAccount(prov_req: dict = Body(...)):
    return createAccount(prov_req)

# Secrets Hub Filter & Policy will be created if they do not exist
@app.post("/createshfilterforsafe")
def _getSHFilterForSafe(prov_req: dict = Body(...)):
    return getSHFilterForSafe(prov_req)

@app.post("/createshsyncpolicy")
def _getSHSyncPolicy(prov_req: dict = Body(...)):
    return getSHSyncPolicy(prov_req)