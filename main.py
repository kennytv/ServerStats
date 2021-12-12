from datetime import date
import schedule
import time
import json
import requests
import argutil


def loadJson(url):
    return requests.get(url).json()


def getData(softwareId, chartId):
    return loadJson("https://bstats.org/api/v1/plugins/{}/charts/{}/data".format(softwareId, chartId))


def getServers(softwareId):
    return loadJson("https://bstats.org/api/v1/plugins/{}/charts/servers/data/?maxElements=1".format(softwareId))[0][1]


def do():
    software = {"paper": 580, "bukkit": 1, "purpur": 5103}

    data = {}
    for name, sId in software.items():
        # Different names for old software, yay
        if sId == 1:
            mcVersionKey = "minecraftVersion"
        else:
            mcVersionKey = "minecraft_version"

        # Grab server count just to have it, even though only version data will be used
        data[name] = {"servers": getServers(sId),
                      "minecraft_version": getData(sId, mcVersionKey)}

    fileName = date.today().strftime("data/%Y-%m-%d.json")
    with open(fileName, "w") as file:
        json.dump(data, file)
        print("Saved data to", fileName)


if argutil.hasArg("now", shortArg="n"):
    do()
else:
    schedule.every().day.at("18:00").do(do)
    while True:
        schedule.run_pending()
        time.sleep(300)
