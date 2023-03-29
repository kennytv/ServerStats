import json
import os
import argutil

minVersion = 8
expandVersions = ["1.19"]


def handle(appendTo, fName, full=False):
    with open("data/" + fName) as f:
        currentData = json.load(f)

    dataObject = {}
    appendTo.append({"date": fName.replace(".json", ""), "data": dataObject})

    for software in softwareList:
        if software not in currentData:
            # :eyes:
            dataObject[software] = {}
            continue

        softwareData = currentData[software]
        versionData = {}
        dataObject[software] = versionData
        for o in softwareData["minecraft_version"]:
            if full:
                versionData[o["name"]] = o["y"]
                continue

            # Collect 1.x.y as 1.x
            ver = o["name"]

            # Ignore the custom garbage
            if not ver.startswith("1."):
                continue

            try:
                index = ver.index(".", 2)
                shortVer = ver[0:index]
                try:
                    if int(shortVer[2:]) < minVersion:
                        continue
                except Exception:
                    # Dum version
                    continue

                if shortVer in expandVersions:
                    # Exempted
                    versionData[ver] = o["y"]
                    continue

                if shortVer not in versionData:
                    versionData[shortVer] = o["y"]
                else:
                    versionData[shortVer] = versionData[shortVer] + o["y"]
            except ValueError:
                versionData[ver] = o["y"]

    # Now we have to subtract dum stuff from the Bukkit numbers, yay!
    booketData = dataObject["bukkit"]
    for software, removeFromBukkit in softwareList.items():
        if not removeFromBukkit:
            continue

        for ver, y in dataObject[software].items():
            if booketData.__contains__(ver):
                booketData[ver] = booketData[ver] - y


hasVer = argutil.hasArg("date")
softwareList = {"paper": True, "bukkit": False}

if os.path.isfile("servers.json"):
    with open("servers.json", "r") as file:
        servers = json.load(file)
        if hasVer:
            data = servers["data"]
else:
    with open("servers-template.json", "r") as file:
        servers = json.load(file)
        if hasVer:
            data = servers["data"]

if hasVer:
    # Append the single data file
    handle(data, argutil.getArg("date") + ".json")
else:
    # List entire data directory
    data = []
    servers["data"] = data
    for fileName in sorted(os.listdir("data")):
        if fileName.endswith(".json"):
            handle(data, fileName)

with open("servers.json", "w") as file:
    json.dump(servers, file)
