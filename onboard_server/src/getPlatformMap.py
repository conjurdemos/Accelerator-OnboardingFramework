# getPlatformMap.py

import json
import logging
import requests

'''
  The intent of this function is to return a platform map of all
  currently active platforms, with search pairs from the existing
  platform map (to avoid having to rewrite those manually).
  The user can then update search pairs as needed and submit the
  new map via updatePlatformMap().

  - Reads existing platform map from file
    - if error returns empty map.
  - Pulls currently active platform info from the vault
    - if error return existing map.
  - Parses each platform into a platform map dictionary
  - Merges search pairs from existing platform map into new map.
  - Returns new map.
'''

def getPlatformMap(cybr_subdomain, session_token):
  # Get existing platform map
  try:
    # PLATFORMMAP_FILE constant is defined in onboard-main.py
    with open(PLATFORMMAP_FILE) as f_in:
      old_platmap = json.load(f_in)
  except IOError:
      err_msg = f"Could not read platform map from file {PLATFORMMAP_FILE}."
      logging.error(err_msg)
      platformmap = {}
      return platformmap

  newplatmap = {}
  # Get currently active platforms
  url = f"https://{cybr_subdomain}.privilegecloud.cyberark.cloud/passwordvault/api/platforms?active=true"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {session_token}",
  }
  response = requests.request("GET", url, headers=headers)
  if response.status_code == 200:
    # Parse the JSON response into a platform map dictionary
    plats = response.json()["Platforms"]
    platmap = {}
    for p in plats:
      plat_id = p['general']['id']
      platmap[plat_id] = {}          # create dictionary entry named for platform ID
      platmap[plat_id]['id'] = plat_id
      platmap[plat_id]['systemtype'] = p['general']['systemType'].replace(" ","+")
      platmap[plat_id]['searchpairs'] = {}
      platmap[plat_id]['required'] = []
      platmap[plat_id]['allkeys'] = ['SECRET']
      for reqd in p['properties']['required']:
        prop_name = reqd['name'].upper()
        platmap[plat_id]['required'].append(prop_name)
        platmap[plat_id]['allkeys'].append(prop_name)
      for optl in p['properties']['optional']:
        prop_name = optl['name'].upper()
        platmap[plat_id]['allkeys'].append(prop_name)

    # Merge search pairs from existing platform map
    newplatmap = platmap.copy() # avoids changing dictionary while iterating
    for plat_id in platmap:
      old_plat = old_platmap.get(plat_id,None)
      if old_plat is not None:
        newplatmap[plat_id]['searchpairs'] = old_plat['searchpairs']
  else:
    newplatmap = old_platmap

  return newplatmap