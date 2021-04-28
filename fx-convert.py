#############################################################
# Author: CrocoKyle
#############################################################

import os
import re
import json
import sys

def ReadEnabled(path):
    """Read the enabled resources in loadresources.cfg"""
    enabled_resources = []
    with open(path, 'r') as res:
        for line in res.readlines():
            patt = '^ensure ([\w-]*)'
            if re.match(patt, line):
                enabled_resources.append(re.match(patt, line).group(1))
    return enabled_resources

def ReadJson(path):
    """Read the JSON file for FxDK in fxproject.json"""
    with open(path, "r") as jsonFile:
        data = json.load(jsonFile)
    return data

def ModifyJson(enabled_resources, data):
    """Update the JSON file with the correct resources"""
    errors = []
    modified = []
    for res in enabled_resources:

        if res in data["resources"]:
            try:
                if not data["resources"][res]["enabled"]: modified.append(" [x] Enabled: {}".format(res))
                data["resources"][res]["enabled"] = True
            except:
                errors.append("Was not able to enable the resource {} manually. Enable it in the FxDK UI instead.".format(res))
        else:
            data["resources"][res] = {"name": res,"enabled": True,"restartOnChange": False}
            modified.append(" [>] Created: {}".format(res))

    return data, errors, modified

def WriteJson(json_data, path):
    """Write back the JSON file"""
    with open(path, "w") as jsonFile:
        json.dump(json_data, jsonFile, indent=4, sort_keys=True)

def main(args):
    # Handle path arguments
    if len(args) == 1:
        resources = 'loadresources.cfg'
        fxproject = 'fxproject.json'
    elif len(args) == 2 or len(args) > 3:
        print("\n")
        print("Converts a loadresources.cfg file into a fxproject.json file for FxDK")
        print("Usage: python3 fxproject-writer.py *Optional parameters: <path to loadresources.cfg> <path to fxproject.json>")
        print("\n")
        sys.exit("ERROR: Wrong number of arguments.")
    else:
        resources = args[0]
        fxproject = args[1]

    enabled_resources = ReadEnabled(resources)
    data = ReadJson(fxproject)
    new_json, errors, modified = ModifyJson(enabled_resources, data)
    WriteJson(new_json, fxproject)

    # Display results
    for mod in modified:
        print(mod)
    for error in errors:
        print(error)

if __name__ == '__main__':
    main(sys.argv)
