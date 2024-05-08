from datetime import date
import schedule
import time
import json
import requests
import argutil


def load_json(url):
    return requests.get(url).json()


def get_data(software_id, chart_id):
    return load_json("https://bstats.org/api/v1/plugins/{}/charts/{}/data".format(software_id, chart_id))


def get_servers(software_id):
    return load_json("https://bstats.org/api/v1/plugins/{}/charts/servers/data/?maxElements=1".format(software_id))[0][1]


def do():
    software = {"paper": 580, "bukkit": 1, "purpur": 5103, "folia": 18084}

    data = {}
    for name, software_id in software.items():
        # Different names for old software, yay
        if software_id == 1:
            mcVersionKey = "minecraftVersion"
        else:
            mcVersionKey = "minecraft_version"

        # Grab server count just to have it, even though only version data will be used
        data[name] = {"servers": get_servers(software_id),
                      "minecraft_version": get_data(software_id, mcVersionKey)}

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
