# main.py

import logging
from fastapi import FastAPI, Body
from cybronboard import *

logfile = "./logs/onboard-server.log"
loglevel = logging.INFO       # BEWARE! DEBUG loglevel can leak secrets!
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