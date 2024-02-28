# main.py

import logging
from fastapi import FastAPI, Body
from cybronboard import *

logfile = "./logs/onboard-server.log"
loglevel = logging.DEBUG       # BEWARE! DEBUG loglevel can leak secrets!
logfmode = 'w'                # w = overwrite, a = append
logging.basicConfig(filename=logfile, encoding='utf-8', level=loglevel, filemode=logfmode)

app = FastAPI()

@app.get("/getsafename")
def _getSafeName(prov_req: dict = Body(...)):
    return getSafeName(prov_req)

@app.get("/getplatformid")
def _getPlatformId(prov_req: dict = Body(...)):
    return getPlatformId(prov_req)

@app.get("/validaterequest")
def _validateRequestWithPlatform(prov_req: dict = Body(...)):
    return validateRequestWithPlatform(prov_req)

@app.get("/authncyberark")
def _authnCyberark(admin_creds: dict = Body(...)):
    return authnCyberark(admin_creds)

# Vault state-changing endpoints
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

# Secrets Hub endpoints
# Source & Target stores must already exist
@app.get("/getshsourcestoreid")
def _getSHSourceStoreId(prov_req: dict = Body(...)):
    return getSHSourceStoreId(prov_req)

@app.get("/getshtargetstoreid")
def _getSHTargetStoreId(prov_req: dict = Body(...)):
    return getSHTargetStoreId(prov_req)

# Filter & Policy will be created if they do not exist
@app.post("/createshfilterforsafe")
def _getSHFilterForSafe(prov_req: dict = Body(...)):
    return getSHFilterForSafe(prov_req)

@app.post("/createshsyncpolicy")
def _getSHSyncPolicy(prov_req: dict = Body(...)):
    return getSHSyncPolicy(prov_req)